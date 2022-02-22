from django.urls import path
from .views import PowerGenView

urlpatterns = [
    path('get_top_n_plants', PowerGenView.get_top_n_plants, name='get_top_n_plants'),
    path('filter_by_state', PowerGenView.filter_by_state, name='filter_by_state'),
    path('get_plant_details', PowerGenView.get_plant_details, name='get_plant_details'),
    path('get_plants_annual_generation', PowerGenView.get_plants_annual_generation, name='get_plants_annual_generation'),
    path('get_states_annual_generation', PowerGenView.get_states_annual_generation, name='get_states_annual_generation'),
    path('get_plant_details', PowerGenView.get_plant_details, name='get_plant_details'),
]