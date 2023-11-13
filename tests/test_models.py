"""
Test cases for Product Model

"""
import os
import logging
import unittest
from datetime import date
from service import app
from service.models import Product, DataValidationError, db
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "")


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYProduct(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="shirt",
            price=6,
            category="clothes",
            inventory=1,
            available=True,
            created_date=date.today(),
            modified_date=date.today(),
        )
        self.assertEqual(str(product), "<Product shirt id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "shirt")
        self.assertEqual(product.price, 6)
        self.assertEqual(product.category, "clothes")
        self.assertEqual(product.inventory, 1)
        self.assertEqual(product.available, True)
        self.assertEqual(product.created_date, date.today())
        self.assertEqual(product.modified_date, date.today())

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(
            name="shirt",
            price=6,
            category="clothes",
            inventory=1,
            created_date=date.today(),
            modified_date=date.today(),
        )
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_update_a_product(self):
        """It should Update an existing Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        logging.debug(product)
        self.assertIsNotNone(product.id)
        # Change it an save it
        product.price = 3
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.price, 3)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].price, 3)

    def test_update_no_id(self):
        """It should not Update a Product with no id"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category)
        self.assertIn("inventory", data)
        self.assertEqual(data["inventory"], product.inventory)
        self.assertIn("available", data)
        self.assertEqual(data["available"], product.available)
        self.assertIn("created_date", data)
        self.assertEqual(date.fromisoformat(data["created_date"]), product.created_date)
        self.assertIn("modified_date", data)
        self.assertEqual(
            date.fromisoformat(data["modified_date"]), product.modified_date
        )
        self.assertIn("like", data)
        self.assertEqual(data["like"], product.like)
        self.assertIn("disable", data)
        self.assertEqual(data["disable"], product.disable)

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.category, data["category"])
        self.assertEqual(product.price, data["price"])
        self.assertEqual(product.inventory, data["inventory"])
        self.assertEqual(product.created_date, date.fromisoformat(data["created_date"]))
        self.assertEqual(
            product.modified_date, date.fromisoformat(data["modified_date"])
        )
        self.assertEqual(product.like, data["like"])
        self.assertEqual(product.disable, data["disable"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {"id": 1, "name": "diet coke", "category": "beverage"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad available attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["available"] = "False"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_product(self):
        """It should Find a Product by ID"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 5)
        # find the 2nd product in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.price, products[1].price)
        self.assertEqual(product.like, products[1].like)
        self.assertEqual(product.disable, products[1].disable)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)
