from django.urls import path, include

from . import views

app_name = 'trades'

urlpatterns = (
    path('', views.home, name='home'),
    path('parse_nasdaq', views.parse_nasdaq, name='parse_nasdaq'),
    path(
        '<slug:company>/delta',
        views.ticker_delta, name='ticker_delta'),
    path(
        '<slug:company>/delta/<api>',
        views.ticker_delta, name='ticker_delta_api'),
    path(
        '<slug:company>/analytics',
        views.ticker_analytics, name='ticker_analytics'),
    path(
        '<slug:company>/analytics/<api>',
        views.ticker_analytics, name='ticker_analytics_api'),
    path(
        '<slug:company>/insider/<name>',
        views.insider_name, name='insider_name'
    ),
    path(
        '<slug:company>/insider/<name>/<api>',
        views.insider_name, name='insider_name'
    ),
    path('<slug:company>/insider', views.insider, name='insider'),

    path('<slug:company>/insider/<api>', views.insider, name='insider_api'),
    path('<slug:company>', views.ticker, name='ticker'),
    path('<slug:company>/<api>', views.ticker, name='ticker_api'),
)
