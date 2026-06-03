import pytest 
from recipes import *

@pytest.fixture
def ing():
    return Ingredient("Мука", 100, "г")

def test_ing_init(ing):
    assert ing.name == "Мука"
    assert ing.quantity == 100.0
    assert ing.unit == "г"

def test_ing_str(ing):
    assert str(ing) == "Мука: 100.0 г"

@pytest.mark.parametrize("other_ing, expected", [
    (Ingredient("Мука", 50, "г"), True),
    (Ingredient("Сахар", 100, "г"), False),
    (Ingredient("Мука", 100, "кг"), False)
])
def test_ing_eq(ing, other_ing, expected):
    assert(ing==other_ing) == expected

def test_ing_quantity_err():
    with pytest.raises(ValueError):
        Ingredient("Мука", 0, "г")

    with pytest.raises(ValueError):
        Ingredient("Мука", -1, "г")    

@pytest.fixture
def ingredients(ing):
    return [ing, Ingredient("Сахар", 200, "г")]

@pytest.fixture
def recipe(ingredients):
    return Recipe("Хрючево", ingredients)

def test_rec_init(recipe, ingredients):
    assert recipe.title == "Хрючево"
    assert recipe.ingredients == ingredients

def test_rec_add_new(recipe):
    recipe.add_ingredient(Ingredient("Мука", 4, "кг"))
    assert len(recipe) == 3

def test_rec_add_ex(recipe):
    recipe.add_ingredient(Ingredient("Сахар", 150, "г"))
    assert len(recipe) == 2
    assert recipe.ingredients[1].quantity == 350

def test_rec_valid_ratio():
    assert Recipe.is_valid_ratio(2)
    assert Recipe.is_valid_ratio(0.5)

    assert not Recipe.is_valid_ratio(0)
    assert not Recipe.is_valid_ratio(-1)
    assert not Recipe.is_valid_ratio("abc")

def test_rec_scale(recipe):
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

def test_rec_len(ing):
    ingredients = [ing, Ingredient("Мука", 200, "г")]
    recipe = Recipe("Хрючево", ingredients)
    assert len(recipe) == 1
    recipe.add_ingredient(Ingredient("Мука", 150, "г"))
    assert len(recipe) == 1

@pytest.fixture
def shplist(recipe):
    shplist = ShoppingList()
    shplist.add_recipe(recipe,1)
    return shplist

def test_shplist_add(shplist):
    assert len(shplist._items) == 2
    
    ing1, title1 = shplist._items[0]
    assert ing1.name == "Мука"
    assert ing1.quantity == 100
    assert ing1.unit == "г"
    assert title1 == "Хрючево"
    
    ing2, title2 = shplist._items[1]
    assert ing2.name == "Сахар"
    assert ing2.quantity == 200
    assert ing2.unit == "г"
    assert title2 == "Хрючево"
    
def test_shplist_add_err(shplist, recipe):    
    with pytest.raises(ValueError):
        shplist.add_recipe(recipe, 0)
    with pytest.raises(ValueError):
        shplist.add_recipe(recipe, -1)

def test_shplist_rm(shplist):
    bf = shplist._items.copy()
    shplist.remove_recipe("Пицца")
    assert shplist._items == bf
    shplist.remove_recipe("Хрючево")
    assert shplist._items == []

def test_shplist_get(shplist):
    rec = Recipe("Вкуснсть", [Ingredient("Сахар", 350, "г"), Ingredient("Масло", 100, "г")])
    shplist.add_recipe(rec,2)
    res = shplist.get_list()
    assert len(res) == 3
    assert res[0].name == "Масло"
    assert res[0].quantity == 200
    assert res[0].unit == "г"
    assert res[1].name == "Мука"
    assert res[1].quantity == 100
    assert res[1].unit == "г"
    assert res[2].name == "Сахар"
    assert res[2].quantity == 900
    assert res[2].unit == "г"

def test_shplist_sum(shplist):
    rec = Recipe("Вкуснсть", [Ingredient("Сахар", 350, "г"), Ingredient("Масло", 100, "г")])
    new_list = ShoppingList()
    new_list.add_recipe(rec,1)
    old1 = shplist._items
    old2 = new_list._items
    sum_of_lists = shplist + new_list
    assert sum_of_lists._items == shplist._items + new_list._items
    assert old1 == shplist._items
    assert old2 == new_list._items