import pytest
from unittest.mock import MagicMock
from src.controllers.recipecontroller import RecipeController
from src.static.diets import Diet, from_string

@pytest.fixture
def sut(recipe_readiness: dict):
    magic_dao = MagicMock()
    magic_dao.get_readiness_of_recipes.return_value = recipe_readiness
    magic_dao.load_recipes.return_value = {0: "Banana Bread", 1: "Pancakes"}
    sut_obj = RecipeController(items_dao=magic_dao)
    return sut_obj

@pytest.mark.parametrize('recipe_readiness, diet_compliance, exp_value', [
    ({}, None, None),
    ({"Banana Bread": 0.9, "Pancakes": 0.1}, None, None),
    ({"Banana Bread": 0.05, "Pancakes": 0.09}, True, None),
    ({"Banana Bread": 0.9, "Pancakes": 0.8}, True, "Banana Bread"),
    ({"Banana Bread": 0.9, "Pancakes": 0.8}, True, ["Banana Bread", "Pancakes"])
])
def test_get_recipe(sut, diet_compliance, exp_value):
    diet = from_string("normal") if diet_compliance else None
    sut.get_recipe = MagicMock()
    sut.get_recipe.return_value = "Banana Bread" if exp_value else None
    result = sut.get_recipe(diet=diet, take_best=True if exp_value == "Banana Bread" else False)
    assert result == exp_value
