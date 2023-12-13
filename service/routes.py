"""
Product Service

Paths:
PUT /products/{product_id} - Updates a Product record in the database
"""

from flask import request, abort
from flask_restx import Resource, fields, reqparse, inputs
from service.common import status  # HTTP Status Codes
from service.models import Product

# Import Flask application
from . import app, api


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return {"status": "OK"}, status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    # return (
    #     "Reminder: return some useful information in json format about the service here",
    #     status.HTTP_200_OK,
    # )
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Product",
    {
        "name": fields.String(required=True, description="The name of the Product"),
        "price": fields.Float(required=True, description="The price of the Product"),
        "category": fields.String(
            required=True, description="The category/type of the Product "
        ),
        "inventory": fields.Integer(
            required=True, description="The inventory available of the Product"
        ),
        "available": fields.Boolean(
            required=True, description="Is the Product available for purchase?"
        ),
        "created_date": fields.String(
            required=True, description="The day the Product was created"
        ),
        "modified_date": fields.String(
            required=False, description="The day the Product detail was modified"
        ),
        "like": fields.Integer(
            required=True,
            description="The number of likes byt the previous purchasers of the Product",
        ),
        "disable": fields.Boolean(
            required=True, description="Is the Product disable for purchase?"
        ),
    },
)

product_model = api.inherit(
    "ProductModel",
    create_model,
    {
        "id": fields.String(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument(
    "name",
    type=str,
    location="args",
    required=False,
    help="List Products by name",
)
product_args.add_argument(
    "category",
    type=str,
    location="args",
    required=False,
    help="List Products by category",
)
product_args.add_argument(
    "available",
    type=inputs.boolean,
    location="args",
    required=False,
    help="List Products by availability",
)


######################################################################
#  PATH: /products/{product_id}
######################################################################
@api.route("/products/<product_id>")
@api.param("product_id", "The Product identifier")
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single product
    GET /product{id} - Returns a product with the id
    PUT /product{id} - Update a product with the id
    DELETE /product{id} -  Deletes a product with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A product
    # ------------------------------------------------------------------
    @api.doc("get_products")
    @api.response(404, "Product not found")
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single product

        This endpoint will return a product based on it's id
        """
        app.logger.info("Request to Retrieve a product with id [%s]", product_id)
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"product with id '{product_id}' was not found.",
            )
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING product
    # ------------------------------------------------------------------
    @api.doc("update_products")
    @api.response(404, "product not found")
    @api.response(400, "The posted product data was not valid")
    @api.expect(product_model)
    @api.marshal_with(product_model)
    # @token_required
    def put(self, product_id):
        """
        Update a product

        This endpoint will update a product
        """
        app.logger.info("Request to Update a product with id [%s]", product_id)
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"product with id '{product_id}' was not found.",
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A product
    # ------------------------------------------------------------------
    @api.doc("delete_products")
    @api.response(204, "product deleted")
    # @token_required
    def delete(self, product_id):
        """
        Delete a product

        This endpoint will delete a product based the id specified in the path
        """
        app.logger.info("Request to Delete a product with id [%s]", product_id)
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"product with id '{product_id}' was not found.",
            )

        product.delete()
        app.logger.info("product with id [%s] was deleted", product_id)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /products/{product_id}/disable
######################################################################
@api.route("/products/<product_id>/disable")
@api.param("product_id", "The Product identifier")
class DisableResource(Resource):
    """
    DisableResource class

    Allows the disabling of a single product

    PUT /product{id}/disable - Update a product with the id

    """

    # ------------------------------------------------------------------
    # Disable A product
    # ------------------------------------------------------------------
    @api.doc("disable_products")
    @api.response(200, "product disabled")
    def put(self, product_id):
        """
        Disable a product

        This endpoint will disable a product
        """
        app.logger.info("Request to disable product with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )
        product.disable = True
        product.available = False
        product.update()
        app.logger.info("The [%s] has been disabled.", product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /products/{product_id}/enable
######################################################################
@api.route("/products/<product_id>/enable")
@api.param("product_id", "The Product identifier")
class EnableResource(Resource):
    """
    DisableResource class

    Allows the disabling of a single product

    PUT /product{id}/enable - Update a product with the id

    """

    # ------------------------------------------------------------------
    # Enable A product
    # ------------------------------------------------------------------
    @api.doc("enable_products")
    @api.response(200, "product enabled")
    def put(self, product_id):
        """
        Disable a product

        This endpoint will disable a product
        """
        app.logger.info("Request to enable product with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )
        product.disable = False
        product.available = True
        product.update()
        app.logger.info("The [%s] has been enabled.", product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /products/{product_id}/like
######################################################################
@api.route("/products/<product_id>/like")
@api.param("product_id", "The Product identifier")
class LikeResource(Resource):
    """
    LikeResource class
    """

    # ------------------------------------------------------------------
    # Like A product
    # ------------------------------------------------------------------
    @api.doc("like_products")
    @api.response(404, "Product not found")
    # @token_required
    def put(self, product_id):
        """
        like a product

        This endpoint will like a product
        """
        app.logger.info("Request to like product with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )
        product.like += 1
        product.update()
        app.logger.info("Like count of product with id [%s] updated.", product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /products/{product_id}/adjust_inventory
######################################################################
@api.route("/products/<product_id>/adjust_inventory")
@api.param("product_id", "The Product identifier")
class AdjustResource(Resource):
    """
    Adjust Inventory of a Product
    """

    @api.doc(responses={404: "Product not found", 400: "Invalid input", 200: "Success"})
    @api.expect(
        api.model(
            "AdjustInventory",
            {"inventory_change": fields.Integer(description="Inventory Change")},
        )
    )
    def put(self, product_id):
        """
        Update a Product's Inventory
        """
        app.logger.info("Request to adjust inventory with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(api.abort(404, f"Product with id '{product_id}' was not found."))

        data = request.get_json()
        if "inventory_change" not in data:
            abort(api.abort(400, "Inventory change value is required."))

        inventory_change = data["inventory_change"]
        if not isinstance(inventory_change, int):
            abort(api.abort(400, "Inventory change value must be an integer."))

        product.inventory += inventory_change
        if product.inventory <= 0:
            product.inventory = 0
            product.available = False

        product.update()

        app.logger.info("Product Inventory with ID [%s] updated.", product.id)
        return product.serialize(), status.HTTP_200_OK


# class AdjustResource(Resource):
#     """
#     Adjust Inventory of a Product
#     """

#     @api.doc("adjust_products inventory")
#     @api.response(200, "inventory adjusted")
#     @api.expect(product_model)
#     @api.marshal_with(product_model)
#     def put(self, product_id):
#         """
#         Update inventory of a Product

#         This endpoint will update a Product based the body that is posted
#         """
#         app.logger.info("Request to adjust inventory with id: %s", product_id)

#         product = Product.find(product_id)
#         if not product:
#             abort(
#                 status.HTTP_404_NOT_FOUND,
#                 f"Product with id '{product_id}' was not found.",
#             )

#         data = request.get_json()
#         if "inventory_change" not in data:
#             abort(status.HTTP_400_BAD_REQUEST, "Inventory change value is required.")

#         inventory_change = data["inventory_change"]
#         if not isinstance(inventory_change, int):
#             abort(
#                 status.HTTP_400_BAD_REQUEST,
#                 "Inventory change value must be an integer.",
#             )

#         product.inventory += inventory_change
#         if product.inventory <= 0:
#             product.inventory = 0
#             product.available = False

#         product.update()

#         app.logger.info("Product Inventory with ID [%s] updated.", product.id)
#         return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
#  PATH: /products/{product_id}/purchase
######################################################################
@api.route("/products/<product_id>/purchase")
@api.param("product_id", "The Product identifier")
class PurchaseResource(Resource):
    """
    Purchase a Product
    """

    @api.doc("purchase_products")
    @api.response(200, "product purchased")
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Purchase a Product

        This endpoint will purchase a Product
        """
        app.logger.info("Request to purchase product with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )
        if not product.available:
            abort(
                status.HTTP_409_CONFLICT,
                f"Product with id '{product_id}' is not available.",
            )

        # At this point you would execute code to purchase the product
        # For the moment, we will just set them to unavailable

        product.inventory -= 1
        if product.inventory == 0:
            product.available = False
        product.update()

        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /PRODUCTS
######################################################################
@api.route("/products", strict_slashes=False)
class ProductCollection(Resource):
    """Handles all interactions with collections of Products"""

    # ------------------------------------------------------------------
    # LIST ALL ProductS
    # ------------------------------------------------------------------
    @api.doc("list_products")
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """Returns all of the Products in the inventory"""
        app.logger.info("Request to list Products inventory...")

        products = []
        args = product_args.parse_args()
        if args["category"]:
            app.logger.info("Filtering by category: %s", args["category"])
            products = Product.find_by_category(args["category"])
        elif args["name"]:
            app.logger.info("Filtering by name: %s", args["name"])
            products = Product.find_by_name(args["name"])
        elif args["available"] is not None:
            app.logger.info("Filtering by availability: %s", args["available"])
            products = Product.find_by_availability(args["available"])
        else:
            app.logger.info("Returning unfiltered list.")
            products = Product.all()

        # app.logger.info('[%s] Products returned', len(products))
        results = [product.serialize() for product in products]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # Add a new product
    # ------------------------------------------------------------------
    @api.doc("create_products")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product
        """
        app.logger.info("Request to Create a Product")

        product = Product()
        app.logger.debug("Payload = %s", api.payload)
        product.deserialize(api.payload)
        product.create()

        app.logger.info("Product with ID [%s] created.", product.id)
        location_url = api.url_for(
            ProductResource, product_id=product.id, _external=True
        )

        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


# def check_content_type(content_type):
#     """Checks that the media type is correct"""
#     if "Content-Type" not in request.headers:
#         app.logger.error("No Content-Type specified.")
#         abort(
#             status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             f"Content-Type must be {content_type}",
#         )

#     if request.headers["Content-Type"] == content_type:
#         return

#     app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
#     abort(
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         f"Content-Type must be {content_type}",
#     )
