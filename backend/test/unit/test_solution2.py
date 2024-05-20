import pytest
from unittest.mock import MagicMock, patch
from src.controllers.recipecontroller import RecipeController
from src.util.dao import getDao, DAO
from src.static.diets import Diet

@pytest.fixture
def mock_dao():
    """Fixture to mock the DAO object with predefined responses."""
    with patch('src.util.dao.DAO') as mock_dao_class:
        mock_dao_instance = mock_dao_class.return_value
        yield mock_dao_instance

@pytest.fixture
def recipe_controller(mock_dao):
    """Fixture to create a RecipeController instance with the mocked DAO."""
    return RecipeController(mock_dao)

@pytest.mark.unit
class TestRecipeController:
    """
    TestRecipeController class docstring
    """

    @patch('src.controllers.recipecontroller.RecipeController.get_available_items')
    @patch('src.controllers.recipecontroller.calculate_readiness')
    def test_get_recipe_optimal(self, mock_calculate_readiness, mock_get_available_items, recipe_controller):
        """
        Test the behavior of the get_recipe method when take_best is True.
        """
        # Mock available items
        mock_get_available_items.return_value = {'item1': 2, 'item2': 1, 'item3': 1}
        
        # Mock recipes
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['vegan'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['vegetarian'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]
        
        # Mock readiness calculation
        def mock_calculate(recipe, items):
            return 1.0 if recipe['name'] == 'Recipe1' else 0.5
        mock_calculate_readiness.side_effect = mock_calculate

        # Call get_recipe with diet as vegan and take_best as True
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        
        # Check if the returned recipe name is 'Recipe1'
        assert result == 'Recipe1'

    @patch('src.controllers.recipecontroller.RecipeController.get_available_items')
    @patch('src.controllers.recipecontroller.calculate_readiness')
    def test_get_recipe_random(self, mock_calculate_readiness, mock_get_available_items, recipe_controller):
        """
        Test the behavior of the get_recipe method when take_best is False.
        """
        # Mock available items
        mock_get_available_items.return_value = {'item1': 2, 'item2': 1, 'item3': 1}

        # Mock recipes
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['vegan'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['vegetarian'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Mock readiness calculation
        def mock_calculate(recipe, items):
            return 1.0 if recipe['name'] == 'Recipe1' else 0.5
        mock_calculate_readiness.side_effect = mock_calculate

        # Mock random choice
        with patch('random.randint', return_value=1):
            # Call get_recipe with diet as vegan and take_best as False
            result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=False)
            # Check if the returned recipe name is 'Recipe2'
            assert result == 'Recipe2'

    @patch('src.controllers.recipecontroller.RecipeController.get_available_items')
    @patch('src.controllers.recipecontroller.calculate_readiness')
    def test_no_qualifying_recipes(self, mock_calculate_readiness, mock_get_available_items, recipe_controller):
        """
        Test the behavior of the get_recipe method when no recipes meet the readiness criteria.
        """
        # Mock available items
        mock_get_available_items.return_value = {'item1': 2, 'item2': 1, 'item3': 1}

        # Mock recipes
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['vegan'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['vegetarian'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Mock readiness calculation
        def mock_calculate(recipe, items):
            return 0.0
        mock_calculate_readiness.side_effect = mock_calculate

        # Call get_recipe with diet as vegan and take_best as True
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        # Check if the returned result is None
        assert result is None

    @patch('src.controllers.recipecontroller.RecipeController.get_available_items')
    @patch('src.controllers.recipecontroller.calculate_readiness')
    def test_dietary_non_compliance(self, mock_calculate_readiness, mock_get_available_items, recipe_controller):
        """
        Test the behavior of the get_recipe method when recipes do not comply with the specified diet.
        """
        # Mock available items
        mock_get_available_items.return_value = {'item1': 2, 'item2': 1, 'item3': 1}

        # Mock recipes
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['normal'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['normal'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Mock readiness calculation
        def mock_calculate(recipe, items):
            return 1.0
        mock_calculate_readiness.side_effect = mock_calculate

        # Call get_recipe with diet as vegan and take_best as True
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        # Check if the returned result is None
        assert result is None

    @patch('src.controllers.recipecontroller.RecipeController.get_available_items')
    @patch('src.controllers.recipecontroller.calculate_readiness')
    def test_no_recipes_available(self, mock_calculate_readiness, mock_get_available_items, recipe_controller):
        """
        Test the behavior of the get_recipe method when no recipes are available.
        """
        # Mock available items
        mock_get_available_items.return_value = {'item1': 2, 'item2': 1, 'item3': 1}

        # Mock recipes as empty list
        recipe_controller.recipes = []

        # Call get_recipe with diet as vegan and take_best as True
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        # Check if the returned result is None
        assert result is None