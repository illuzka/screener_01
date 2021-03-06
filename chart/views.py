from django.shortcuts import render
from django.views.generic import View
from chart.backend.models.creation import ModelsCreation
from chart.backend.models.processing import ModelsDataProcessing, DataFilters
from .models import ChartTicker, ChartItem, ChartItemData, News
from datetime import datetime
from django.db.models import Q
from chart.backend.scrapping.tables import MainTable
from django.core.paginator import Paginator
from background_task import background
import requests


@background(schedule=50)
def get_market_news():
    key = '1de25ecebeecbd8918f258fb09d4333c50f6d855c3107a5e98650d65868c99dd'
    url_request = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key=' + key
    data = requests.get(url_request).json()

    News.objects.all().delete()

    try:
        for i in range(5):
            News.objects.bulk_create([
            News(date=datetime.utcfromtimestamp(data['Data'][i]['published_on']).strftime('%Y-%m-%d %H:%M:%S'),
                 url=data['Data'][i]['url'],
                 title=data['Data'][i]['title'],
                 body=data['Data'][i]['body'],
                )
        ])
    except (ConnectionError, KeyError):
        News.objects.bulk_create([
            News(date=datetime.now(),
                 url='Error',
                 title='Error',
                 body='Error',
                 )
        ])


class HomeView(View):
    # #
    ChartTicker.objects.all().delete()
    ChartItem.objects.all().delete()
    ChartItemData.objects.all().delete()
    # # # # # # # #
    ModelsCreation().ticker_creation()
    ModelsCreation().items_creation()
    ModelsCreation().chart_item_data_creation()
    """
    # Scrapping
    # """
    if MainTable().gainers_losers() and MainTable().dom_vol_marcap() != None:
        mt_gainers_losers = MainTable().gainers_losers()
        mt_dom_vol_marcap = MainTable().dom_vol_marcap()
    else:
        mt_gainers_losers = ['None', 'None']
        mt_dom_vol_marcap = ['None', 'None', 'None']

    """
    News data    
    """
    news = News.objects.all()

    def get(self, request):
        tickers_list = ChartTicker.objects.all()
        # Search
        query = request.GET.get('q')
        if query:
            search_result = tickers_list.filter(Q(name__icontains=query) | Q(full_name__icontains=query))
        else:
            search_result = None

        paginator = Paginator(tickers_list, 16)
        page = request.GET.get('page')
        tickers = paginator.get_page(page)

        sort_by_volume = DataFilters().sort_by_volume(tickers)
        sort_by_gainers_losers = DataFilters().sort_by_gainers_losers(tickers)
        sort_by_unusual_volume = DataFilters().sort_by_unusual_volume(tickers)

        nr_of_tickers = len(tickers_list)


        context = {
            'tickers': tickers,
            'search_result': search_result,
            'sort_by_volume': sort_by_volume,
            'sort_by_gainers_losers': sort_by_gainers_losers,
            'sort_by_unusual_volume': sort_by_unusual_volume,
            'mt_gainers_losers': self.mt_gainers_losers,
            'mt_dom_vol_marcap': self.mt_dom_vol_marcap,
            'nr_of_tickers': nr_of_tickers,
            'news': self.news,

        }
        return render(request, 'chart/templates/HomeView.html', context)


class ChartView(View):

    def get(self, request, pk=None):
        models_data = ModelsDataProcessing()

        """
        Main chart items context.
        """
        ticker = ChartTicker.objects.get(pk=pk)
        prices_margins = models_data.price_margin(ticker.labels)
        items = ticker.chartitem_set.all()
        volumes = ticker.chartitem_set.values_list('volume', flat=True)
        max_min_vol = models_data.volume_max_min_values(volumes)
        mar_left_values = ticker.chartitem_set.values_list('margin_left_value', flat=True)
        volume_hm = models_data.volume_heights_margins(volumes, mar_left_values)
        dates = ticker.chartitem_set.values_list('date', flat=True)
        dates_margins = models_data.dates_margins_dict(dates)

        """
        Additional chart context.  
        """
        today = datetime.now().strftime('%b-%d')
        last_item_values = models_data.last_item_values(pk)

        context = {
            'items': items,
            'ticker': ticker,
            'prices_margins': prices_margins,
            'volumes': volumes,
            'max_min_vol': max_min_vol,
            'volume_hm': volume_hm,
            'dates_margins': dates_margins,
            'today': today,
            'last_item_values': last_item_values,
        }

        return render(request, 'chart/templates/ChartView.html', context)