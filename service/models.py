"""
Models for YourResourceModel

All of the models are stored in this module
"""
# pylint: disable=too-many-instance-attributes
import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Product.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Product(db.Model):
    """
    Class that represents a Product
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    price = db.Column(db.Float(), nullable=False)
    category = db.Column(db.String(63), nullable=False)
    inventory = db.Column(db.Integer(), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    created_date = db.Column(db.Date(), nullable=False, default=date.today())
    modified_date = db.Column(db.Date())
    like = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Empty ID field!")
        db.session.commit()

    def delete(self):
        """Removes a YourResourceModel from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "inventory": self.inventory,
            "available": self.available,
            "created_date": self.created_date.isoformat(),
            "modified_date": self.modified_date.isoformat(),
            "like": self.like if self.modified_date is not None else None,
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.price = data["price"]
            self.category = data["category"]
            self.inventory = data["inventory"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
            self.created_date = date.fromisoformat(data["created_date"])
            self.modified_date = date.fromisoformat(data["modified_date"])

            if not isinstance(data["like"], int):
                raise DataValidationError(
                    "Invalid type for int [like]: " + str(type(data["like"]))
                )
            if data["like"] < 0:
                raise DataValidationError(
                    "Invalid value for like. Like should be a non-negative value."
                )
            self.like = data["like"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data - "
                "Error message: " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.drop_all()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the YourResourceModels in the database"""
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a YourResourceModel by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name

        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Products in a category

        :param category: the category of the Products you want to match
        :type category: str

        :return: a collection of Products in that category
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)
