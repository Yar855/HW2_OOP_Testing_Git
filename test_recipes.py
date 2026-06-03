import pytest 
from recipes import *

ing = Ingredient("Мука", 100, "г")

def test_ing_init():
    assert ing.name == "Мука"
    assert ing.quantity == 100.0
    assert ing.unit == "г"

def test_ing_str():
    assert str(ing) == "Мука: 100.0 г"

@pytest.mark.parametrize("other_ing, expected", [
    (Ingredient("Мука", 50, "г"), True),
    (Ingredient("Сахар", 100, "г"), False),
    (Ingredient("Мука", 100, "кг"), False)
])
def test_ing_eq(other_ing, expected):
    assert(ing==other_ing) == expected

def test_rec_init():
    ingredients = [ing, Ingredient("Сахар", 200, "г")]
    recipe = Recipe("Хрючево", ingredients)
    assert recipe.title == "Хрючево"
    assert recipe.ingredients == ingredients

def test_rec_add_new():
    ingredients = [ing, Ingredient("Сахар", 200, "г")]
    recipe = Recipe("Хрючево", ingredients)
    recipe.add_ingredient(Ingredient("Мука", 4, "кг"))
    assert len(recipe) == 3

def test_rec_add_ex():
    ingredients = [ing, Ingredient("Сахар", 200, "г")]
    recipe = Recipe("Хрючево", ingredients)
    recipe.add_ingredient(Ingredient("Сахар", 150, "г"))
    assert len(recipe) == 2
    assert recipe.ingredients[1].quantity == 350

def test_rec_scale():
    ingredients = [ing, Ingredient("Сахар", 200, "г")]
    recipe = Recipe("Хрючево", ingredients)
    new = recipe.scale(2)
    assert new is not recipe
    assert new.title == recipe.title
    assert recipe.ingredients[0].quantity == 100
    assert new.ingredients[0].quantity == 200
    assert recipe.ingredients[1].quantity == 200
    assert new.ingredients[1].quantity == 400
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_rec_len():
    ingredients = [ing, Ingredient("Мука", 200, "г")]
    recipe = Recipe("Хрючево", ingredients)
    assert len(recipe) == 1
    recipe.add_ingredient(Ingredient("Мука", 150, "г"))
    assert len(recipe) == 1


    