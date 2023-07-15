import requests
from rest_framework.views import APIView
from .models import Pokemon
from django.shortcuts import render

class BattleAPIView(APIView):
    def get_pokemon_data(self, pokemon_name):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    def get_pokemon_id(self,pokemon_data):
        pokemon_id = pokemon_data['id']
        if not pokemon_id:
            raise Exception("This Pokemon ID is not found")
        return pokemon_id
    def calculate_stat_change(self, pokemon_data):
        stats = pokemon_data['stats']
        total_stat_change = sum(stat['base_stat'] for stat in stats)
        return total_stat_change

    def get(self, request):
        return render(request, 'battle.html')

    def post(self, request):
        pokemon1_name = request.POST.get('pokemon1')
        pokemon2_name = request.POST.get('pokemon2')

        if not pokemon1_name or not pokemon2_name:
            return render(request, 'battle.html', {'error': 'Both Pokémon names are required.'})

        pokemon1_data = self.get_pokemon_data(pokemon1_name)
        pokemon2_data = self.get_pokemon_data(pokemon2_name)

        if not pokemon1_data or not pokemon2_data:
            return render(request, 'battle.html', {'error': 'Pokémon data not found.'})

        pokemon1_stat_change = self.calculate_stat_change(pokemon1_data)
        pokemon2_stat_change = self.calculate_stat_change(pokemon2_data)

        pokemon1_id = self.get_pokemon_id(pokemon1_data)
        pokemon2_id = self.get_pokemon_id(pokemon2_data)

        pokemon1 = Pokemon(name=pokemon1_name, stats_change=pokemon1_stat_change,show_id=pokemon1_id)
        pokemon2 = Pokemon(name=pokemon2_name, stats_change=pokemon2_stat_change,show_id = pokemon2_id)

        winner = None
        if pokemon1_stat_change > pokemon2_stat_change:
            winner = pokemon1
        elif pokemon1_stat_change < pokemon2_stat_change:
            winner = pokemon2

        response_data = {
            "pokemon1": {
                "id": pokemon1_id,
                "name": pokemon1.name,
                "stats_change": pokemon1.stats_change,
            },
            "pokemon2": {
                "id": pokemon2_id,
                "name": pokemon2.name,
                "stats_change": pokemon2.stats_change,
            },
            "winner": winner.name if winner else "Tie",
        }
        return render(request, 'battle.html', response_data)
