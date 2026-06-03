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

    


