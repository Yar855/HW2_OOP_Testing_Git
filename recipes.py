class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self):
        return f"{self.name}: {self._quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient('{self.name}', {self._quantity}, '{self.unit}')"
    
    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title: str, ingredients: list[Ingredient]):
        self.title = title
        self.ingredients = []
        for ing in ingredients:
            self.add_ingredient(ing)
    
    def add_ingredient(self, ing: Ingredient):
        for existing in self.ingredients:
            if ing == existing:
                existing.quantity += ing.quantity
                break

        else:
            self.ingredients.append(ing)
    
    @staticmethod
    def is_valid_ratio(ratio):
        return (isinstance(ratio, float) or isinstance(ratio, int)) and ratio > 0
    
    def scale(self, ratio: float):
        if self.is_valid_ratio(ratio):
            new_recipe = []
            for existing in self.ingredients:
                new_recipe.append(Ingredient(existing.name, existing.quantity*ratio, existing.unit))
            return Recipe(self.title, new_recipe)
        else:
            raise ValueError("Множитель должен быть положительным")
        
    def __len__(self):
        return len(self.ingredients)
    
    def __str__(self):
        str_ingredients = ', '.join(str(n) for n in self.ingredients)
        return f"{self.title}, ингредиенты: {str_ingredients}"

class ShoppingList:
    def __init__(self):
        self._items = []
    
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        for ing in recipe.scale(portions).ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [pair for pair in self._items if pair[1] != title]
    
    def get_list(self):
        dict_ing = {}
        for pair in self._items:
            key = (pair[0].name, pair[0].unit)
            if key in dict_ing:
                dict_ing[key] += pair[0].quantity
            else:
                dict_ing[key] = pair[0].quantity
        res = []
        for (name, unit), quantity in dict_ing.items():
            res.append(Ingredient(name, quantity, unit))
        res.sort(key = lambda ing: ing.name)
        return res
    
    def __add__(self, other: ShoppingList):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
    
class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list[Ingredient]):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        new_recipe = super().scale(ratio)
        return DietaryRecipe(new_recipe.title, self.diet_type, new_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"