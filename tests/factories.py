"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyInteger
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Coke", "Milk", "Apple", "Kale"])
    price = FuzzyFloat(10, 60)
    category = FuzzyChoice(choices=["beverage", "dairy", "fruit", "vegetable"])
    inventory = FuzzyInteger(0, 40)
    created_date = date(2023, 1, 1)
    modified_date = date(2023, 1, 2)
