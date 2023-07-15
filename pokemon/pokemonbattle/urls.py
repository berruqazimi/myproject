from django.urls import path
from .views import BattleAPIView

urlpatterns = [
    path('battle/', BattleAPIView.as_view(), name='battle'),

]