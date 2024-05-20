import pytest
from unittest.mock import MagicMock, patch
from src.controllers.recipecontroller import RecipeController
from src.util.dao import getDao, DAO

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

    # TC1: All Requirements Met
    def test_get_available_items_all_criteria_met(self, recipe_controller, mock_dao):
        """
        Test the behavior of the get_available_items method when all items meet the criteria.
        """
        mock_dao.find.return_value = [
            {"name": "Apple", "quantity": 10.0, "unit": "kg"},
            {"name": "Banana", "quantity": 5.0, "unit": "kg"}
        ]
        result = recipe_controller.get_available_items(minimum_quantity=1)
        assert len(result) == 2
        assert "Apple" in result
        assert "Banana" in result

    # TC2: No Items Meet Minimum Quantity
    def test_get_available_items_no_items_meet_criteria(self, recipe_controller, mock_dao):
        """
        Test the behavior of the get_available_items method when no items meet the criteria.
        """
        mock_dao.find.return_value = [
            {"name": "Apple", "quantity": 10.0, "unit": "kg"},
            {"name": "Banana", "quantity": 5.0, "unit": "kg"}
        ]
        result = recipe_controller.get_available_items(minimum_quantity=11)
        assert len(result) == 0

    # TC3: Incorrect Data Type
    def test_get_available_items_with_incorrect_data_type(self, recipe_controller, mock_dao):
        """
        Test the behavior of the get_available_items method with incorrect data type.
        """
        mock_dao.find.return_value = [
            {"name": "Apple", "quantity": 10.0, "unit": "kg"},
            {"name": "Banana", "quantity": '5', "unit": "kg"}  # Quantity as string
        ]
        with pytest.raises(TypeError):
            recipe_controller.get_available_items(minimum_quantity=1)

    # TC4: Data Type and Quantity Mismatch
    def test_get_available_items_data_type_and_quantity_mismatch(self, recipe_controller, mock_dao):
        """
        Test the behavior of the get_available_items method with incorrect data type and items meeting the quantity.
        """
        mock_dao.find.return_value = [
            {"name": "Apple", "quantity": '10.0', "unit": "kg"},  # Quantity as string
            {"name": "Banana", "quantity": 5.0, "unit": "kg"}
        ]
        with pytest.raises(TypeError):
            recipe_controller.get_available_items(minimum_quantity=1)

    # TC5: Missing Fields
    def test_get_available_items_missing_fields(self, recipe_controller, mock_dao):
        """
        Test the behavior of the get_available_items method with missing fields.
        """
        mock_dao.find.return_value = [
            {"name": "Apple"},
            {"name": "Banana", "quantity": 5.0, "unit": "kg"}
        ]
        with pytest.raises(KeyError):
            recipe_controller.get_available_items(minimum_quantity=1)