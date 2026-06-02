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
    (Ingredient("Сахар", 50, "г"), False),
    (Ingredient("Мука", 50, "кг"), False)
])
def test_ing_eq(other_ing, expected):
    assert(ing==other_ing) == expected