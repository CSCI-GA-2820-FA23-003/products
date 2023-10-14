"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest
from service.models import Product, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceModel(unittest.TestCase):
    """Test Cases for YourResourceModel Model"""

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
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """It should always be true"""
        self.assertTrue(True)

    def test_create_a_pet(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="macbook",
            category="electronics",
            available=True,
            description="Macbook M2 512G",
        )
        # self.assertEqual(str(pet), "<Pet Fido id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "macbook")
        self.assertEqual(product.category, "electronics")
        self.assertEqual(product.available, True)
        product = Product(
            name="macbook",
            category="electronics",
            available=False,
            description="Macbook M1 256G",
        )
        self.assertEqual(product.available, False)
        self.assertEqual(product.description, "Macbook M1 256G")
