from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from PowerGenApp.models import PowerPlants
import pandas as pd
import json

"""
Class to handle api requests
"""


class PowerGenView:
    """
    Net generation of each plant in the US
    """

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_plants_annual_generation(request):
        power_plants = PowerPlants.objects.all().values('state', 'name', 'net_generation')

        if power_plants.exists():
            power_plants_df = pd.DataFrame(list(power_plants))
            power_plants_df = power_plants_df.groupby(['name'])['net_generation'].sum().reset_index()
            power_plants_df = power_plants_df.drop_duplicates()
            power_plants_json = power_plants_df.to_json(orient='records')

            return Response({
                'success': True,
                'data': json.loads(power_plants_json)
            })
        else:
            return Response({
                'success': False,
                'data': 'No records found'
            })

    """
    Net generation of states
    """

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_states_annual_generation(request):
        power_plants = PowerPlants.objects.all().values('state', 'net_generation')

        if power_plants.exists():
            power_plants_df = pd.DataFrame(list(power_plants))
            power_plants_df = power_plants_df.groupby(['state'])['net_generation'].sum().reset_index()
            power_plants_df = power_plants_df.drop_duplicates()
            power_plants_json = power_plants_df.to_json(orient='records')

            return Response({
                'success': True,
                'data': json.loads(power_plants_json)
            })
        else:
            return Response({
                'success': False,
                'data': 'No records found'
            })

    """
    Top n power plants in the US
    """

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_top_n_plants(request):
        n = int(request.GET.get('n', 10))

        power_plants_df = pd.DataFrame(list(PowerPlants.objects.all().values('state', 'name', 'net_generation')))

        if power_plants_df is not None:

            power_plants_df = power_plants_df.groupby(['state', 'name'])['net_generation'].sum().reset_index()
            power_plants_df = power_plants_df.drop_duplicates()

            power_plants_df = power_plants_df.nlargest(n, 'net_generation', keep='all')
            power_plants_json = power_plants_df.to_json(orient='records')

            return Response({
                'success': True,
                'data': json.loads(power_plants_json)
            })
        else:
            return Response({
                'success': False,
                'data': 'No records found'
            })

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def filter_by_state(request):
        state = request.GET.get('state')

        if state is not None:

            power_plants = PowerPlants.objects.filter(state=state.upper()).values('name', 'net_generation')

            if power_plants.exists():

                power_plants_df = pd.DataFrame(list(power_plants))
                power_plants_df = power_plants_df.groupby(['name'])['net_generation'].sum().reset_index()
                power_plants_df = power_plants_df.drop_duplicates()
                power_plants_json = power_plants_df.to_json(orient='records')

                return Response({
                    'success': True,
                    'data': json.loads(power_plants_json)
                })

            else:
                return Response({
                    'success': False,
                    'data': 'No records found.'
                })
        else:
            return Response({
                'success': False,
                'data': 'Please specify state.'
            })

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_plant_details(request):
        plant = request.GET.get('plant')

        if plant is not None:
            # Get the plant details
            power_plant = PowerPlants.objects.filter(name=plant).values('state', 'name', 'net_generation')

            if power_plant.exists():
                power_plant_first = power_plant.first()
                state = power_plant_first['state'] # fetch the state

                # fetch the federal state net generation
                power_plants_state = PowerPlants.objects.filter(state=state).values('state', 'net_generation')
                power_plants_state_df = pd.DataFrame(list(power_plants_state))
                power_plants_state_df = power_plants_state_df.groupby(['state'])['net_generation'].sum().reset_index()
                power_plants_state_df = power_plants_state_df.drop_duplicates()

                state_row = power_plants_state_df.iloc[0]
                state_generation = state_row.net_generation

                # Fetch power plant net generation
                power_plants_df = pd.DataFrame(list(power_plant))
                power_plants_df = power_plants_df.groupby(['name'])['net_generation'].sum().reset_index()
                power_plants_df = power_plants_df.drop_duplicates()

                plant_row = power_plants_df.iloc[0]
                plant_generation = plant_row.net_generation

                # Calculate the plant's contribution to its federal state
                plant_contribution = plant_generation / state_generation * 100

                return Response({
                    'success': True,
                    'data': {
                        'name': plant,
                        'state': state,
                        'annual_net_generation': float(plant_generation),
                        'state_contribution': str(round(float(plant_contribution), 2)) + "%"
                    }
                })

            else:
                return Response({
                    'success': False,
                    'data': 'Incorrect plant name.'
                })
        else:
            return Response({
                'success': False,
                'data': 'Please specify plant.'
            })
