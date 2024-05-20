import pytest
from unittest.mock import patch
from src.controllers.recipecontroller import RecipeController
from src.static.diets import Diet

@pytest.fixture
def recipe_controller():
    """
    Fixture to create a RecipeController instance.
    This allows each test to use a fresh instance of RecipeController.
    """
    return RecipeController(None)

@pytest.mark.unit
class TestRecipeController:
    """
    TestRecipeController class for testing the get_recipe method.
    Each test method in this class tests a specific scenario for the get_recipe method.
    """

    @patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
    def test_get_recipe_optimal(self, mock_get_readiness_of_recipes, recipe_controller):
        """
        Test the behavior of the get_recipe method when take_best is True.
        The method should return the recipe with the highest readiness value.
        """
        # Mock the get_readiness_of_recipes method to return predefined readiness values
        mock_get_readiness_of_recipes.return_value = {'Recipe1': 1.0, 'Recipe2': 0.5}

        # Define the recipes in the recipe controller
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['vegan'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['vegetarian'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Call the get_recipe method and assert that it returns the optimal recipe
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        assert result == 'Recipe1'

    @patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
    def test_get_recipe_random(self, mock_get_readiness_of_recipes, recipe_controller):
        """
        Test the behavior of the get_recipe method when take_best is False.
        The method should return a random recipe that meets the dietary criteria.
        """
        # Mock the get_readiness_of_recipes method to return predefined readiness values
        mock_get_readiness_of_recipes.return_value = {'Recipe1': 1.0, 'Recipe2': 0.5}

        # Define the recipes in the recipe controller
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['vegan'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['vegetarian'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Mock the random.randint function to control the random choice
        with patch('random.randint', return_value=1):
            result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=False)
            assert result == 'Recipe2'

    @patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
    def test_no_qualifying_recipes(self, mock_get_readiness_of_recipes, recipe_controller):
        """
        Test the behavior of the get_recipe method when no recipes meet the readiness criteria.
        The method should return None in this case.
        """
        # Mock the get_readiness_of_recipes method to return no qualifying recipes
        mock_get_readiness_of_recipes.return_value = {}

        # Define the recipes in the recipe controller
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['vegan'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['vegetarian'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Call the get_recipe method and assert that it returns None
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        assert result is None

    @patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
    def test_dietary_non_compliance(self, mock_get_readiness_of_recipes, recipe_controller):
        """
        Test the behavior of the get_recipe method when recipes do not comply with the specified diet.
        The method should return None in this case.
        """
        # Mock the get_readiness_of_recipes method to return no qualifying recipes
        mock_get_readiness_of_recipes.return_value = {}

        # Define the recipes in the recipe controller
        recipe_controller.recipes = [
            {'name': 'Recipe1', 'diets': ['normal'], 'ingredients': {'item1': 1, 'item2': 2}},
            {'name': 'Recipe2', 'diets': ['normal'], 'ingredients': {'item1': 2, 'item3': 3}}
        ]

        # Call the get_recipe method and assert that it returns None
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        assert result is None

    @patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
    def test_no_recipes_available(self, mock_get_readiness_of_recipes, recipe_controller):
        """
        Test the behavior of the get_recipe method when no recipes are available.
        The method should return None in this case.
        """
        # Mock the get_readiness_of_recipes method to return no qualifying recipes
        mock_get_readiness_of_recipes.return_value = {}

        # Define an empty list of recipes in the recipe controller
        recipe_controller.recipes = []

        # Call the get_recipe method and assert that it returns None
        result = recipe_controller.get_recipe(diet=Diet.VEGAN, take_best=True)
        assert result is None