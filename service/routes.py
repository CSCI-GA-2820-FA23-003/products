"""
Product Service

Paths:
PUT /products/{product_id} - Updates a Product record in the database
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Product

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products"""
    app.logger.info("Request for product list")
    products = []
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_name(name)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# ADD A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)

    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    app.logger.info("Product with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
#  LIKE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>/like", methods=["PUT"])
def like_product(product_id):
    """
    Like a Product

    This endpoint will like a product given the id
    """
    app.logger.info("Request to like product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )
    product.like += 1
    product.update()
    app.logger.info("Like count of product with id [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
#  ADJUST A PRODUCT INVENTORY
######################################################################
@app.route("/products/<int:product_id>/adjust_inventory", methods=["PUT"])
def adjust_inventory(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to adjust inventory with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    data = request.get_json()
    if "inventory_change" not in data:
        abort(status.HTTP_400_BAD_REQUEST, "Inventory change value is required.")

    inventory_change = data["inventory_change"]
    if not isinstance(inventory_change, int):
        abort(status.HTTP_400_BAD_REQUEST, "Inventory change value must be an integer.")

    product.inventory += inventory_change
    if product.inventory <= 0:
        product.inventory = 0
        product.available = False

    product.update()

    app.logger.info("Product Inventory with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()

    app.logger.info("Product with ID [%s] delete complete.", product_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# PURCHASE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>/purchase", methods=["PUT"])
def purchase_products(product_id):
    """Purchasing a Pet makes it unavailable"""
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )
    if not product.available:
        abort(
            status.HTTP_409_CONFLICT,
            f"Product with id '{product_id}' is not available.",
        )

    # At this point you would execute code to purchase the pet
    # For the moment, we will just set them to unavailable

    product.inventory -= 1
    if product.inventory == 0:
        product.available = False
    product.update()

    return product.serialize(), status.HTTP_200_OK


######################################################################
# DISABLE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>/disable", methods=["PUT"])
def disable_product(product_id):
    """
    Disable a Product

    This endpoint will disable a product given the id
    """
    app.logger.info("Request to disable product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )
    product.disable = True
    product.available = False
    product.update()
    app.logger.info("The [%s] has been disabled.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
