from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from .models import Pokemon

class BattleAPIViewTests(TestCase):
    def setUp(self):
        self.url = reverse('pokemonbattle')

    def test_battle_api_view_with_valid_data(self):
        pokemon1_name = 'charizard'
        pokemon2_name = 'pikachu'

        with patch('battle.views.requests.get') as mock_get:
            mock_get.return_value.status_code = status.HTTP_200_OK
            mock_get.return_value.json.return_value = {
                'name': pokemon1_name,
                'stats': [
                    {'base_stat': 10},
                    {'base_stat': 20},
                    {'base_stat': 30},
                ]
            }

            response = self.client.post(self.url, {'pokemon1': pokemon1_name, 'pokemon2': pokemon2_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'battle.html')

        pokemon1 = response.context['pokemon1']
        pokemon2 = response.context['pokemon2']
        winner = response.context['winner']

        self.assertEqual(pokemon1.name, pokemon1_name)
        self.assertEqual(pokemon1.stats_change, 60)

        self.assertEqual(pokemon2.name, pokemon2_name)
        self.assertEqual(pokemon2.stats_change, 0)

        self.assertEqual(winner, pokemon1.name)

    def test_battle_api_view_with_invalid_data(self):
        response = self.client.post(self.url, {'pokemon1': '', 'pokemon2': 'pikachu'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'battle.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Both Pokémon names are required.')

    def test_battle_api_view_with_pokemon_data_not_found(self):
        with patch('battle.views.requests.get') as mock_get:
            mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
            response = self.client.post(self.url, {'pokemon1': 'charizard', 'pokemon2': 'pikachu'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'battle.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Pokémon data not found.')

    def test_pokemon_model(self):
        pokemon = Pokemon(name='charizard', stats_change=100)

        self.assertEqual(str(pokemon), 'charizard')
        self.assertEqual(pokemon.name, 'charizard')
        self.assertEqual(pokemon.stats_change, 100)
