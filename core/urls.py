from django.urls import path
# from django.conf.urls import handler500, handler404

from .views import (
    IndexView,
)


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]

# handler404 = 'base.views.custom_404'
# handler500 = 'base.views.custom_500'
# handler403 = 'base.views.custom_403'
# handler400 = 'base.views.custom_400'
