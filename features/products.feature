Feature: The products service back-end
    As a Products Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name         | price | category   | inventory | available |  created_date | modified_date | like | disable |
        | coke         | 3.99  | beverage   | 999       |    True   |  2023-11-10   |   2023-11-10  |  10  |  False  |
        | milk         | 5.5   | dairy      | 15        |    True   |  2023-11-10   |   2023-11-10  |  10  |  False  |
        | kale         | 2.5   | fresh food | 0         |    False  |  2023-11-10   |   2023-11-10  |  10  |  True   |
        | ice cream    | 6.69  | frozen     | 90        |    True   |  2023-11-10   |   2023-11-10  |  10  |  False  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"


######################################################################
# Create Scenarios
######################################################################
Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "name" to "AA-Batteries"
    And I set the "price" to "19.9"
    And I set the "category" to "Electronics"
    And I set the "inventory" to "48"
    And I set the "created_date" to "12-11-2023"
    And I set the "modified_date" to "12-11-2023"
    And I set the "like" to "0"
    And I select "True" in the "Available" dropdown
    And I select "False" in the "Disable" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "name" field should be empty
    And the "category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success retrieve the product"
    And I should see "AA-Batteries" in the "name" field
    And I should see "19.9" in the "price" field
    And I should see "Electronics" in the "category" field
    And I should see "48" in the "inventory" field
    And I should see "2023-12-11" in the "created_date" field
    And I should see "2023-12-11" in the "modified_date" field
    And I should see "0" in the "like" field
    And I should see "True" in the "Available" dropdown
    And I should see "False" in the "Disable" dropdown


######################################################################
# Read Scenarios
######################################################################
Scenario: Read a product existed
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success list all products"
    When I copy the "Id" field
    And I press the "Clear" button
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success retrieve the product"
    Then I should see "coke" in the "name" field

Scenario: Read a product without id
    When I visit the "Home Page"
    And I press the "Retrieve" button
    Then I should see the message "Fail retrieve the product (product id is not provided)"

Scenario: Read a product not exisetd
    When I visit the "Home Page"
    And I set the "Id" to "-1"
    And I press the "Retrieve" button
    Then I should see the message "Fail retrieve the product (product -1 does not exist)"


######################################################################
# List Scenarios
######################################################################
Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success list all products"
    And I should see "coke" in the results
    And I should see "milk" in the results
    And I should not see "apple" in the results


######################################################################
# Update Scenarios
######################################################################
Scenario: Update a product
    When I visit the "Home Page"
    And I set the "Name" to "coke"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "coke" in the "Name" field
    And I should see "beverage" in the "Category" field
    When I change "Name" to "fanta"
    And I press the "Update" button
    Then I should see the message "Success update the product"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success retrieve the product"
    And I should see "fanta" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success list all products"
    And I should see "fanta" in the results
    And I should not see "coke" in the results

Scenario: Update a product without id
    When I visit the "Home Page"
    And I press the "Update" button
    Then I should see the message "Fail update the product (product id is not provided)"

Scenario: Update a product not exisetd
    When I visit the "Home Page"
     And I press the "Search" button
    And I set the "Id" to "-1"
    And I press the "Update" button
    Then I should see the message "Fail update the product (product -1 does not exist)"
    
Scenario: Update a product set availability wrong
    When I visit the "Home Page"
    And I press the "Search" button
    And I select "All" in the "Available" dropdown
    And I press the "Update" button
    Then I should see the message "Fail update the product (product availability should be either True or False)"

######################################################################
# Delete Scenarios
######################################################################
Scenario: Delete a product
    When I visit the "Home Page"
    And I set the "Name" to "coke"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "coke" in the "Name" field
    And I should see "beverage" in the "Category" field
    When I press the "Delete" button
    Then I should see the message "Success delete the product"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success list all products"
    And I should not see "coke" in the results

Scenario: Delete a product without id
    When I visit the "Home Page"
    And I press the "Delete" button
    Then I should see the message "Fail delete the product (product id is not provided)"

Scenario: Delete a product not exisetd
    When I visit the "Home Page"
    And I set the "Id" to "-1"
    And I press the "Delete" button
    Then I should see the message "Fail delete the product (product -1 does not exist)"


######################################################################
# Query Scenarios
######################################################################
Scenario: Search for coke
    When I visit the "Home Page"
    And I set the "Name" to "coke"
    And I press the "Search" button
    Then I should see the message "Success query products by name=coke"
    And I should see "coke" in the results
    And I should not see "milk" in the results

Scenario: Search for beverages
    When I visit the "Home Page"
    And I set the "Category" to "beverage"
    And I press the "Search" button
    Then I should see the message "Success query products by category=beverage"
    And I should see "coke" in the results
    And I should not see "milk" in the results

Scenario: Search through availability
    When I visit the "Home Page"
    And I select "True" in the "available" dropdown
    And I press the "Search" button
    Then I should see the message "Success query products by available=true"
    And I should see "milk" in the results
    And I should see "coke" in the results
    And I should see "ice cream" in the results
    And I should not see "kale" in the results


######################################################################
# Action Scenarios
######################################################################
Scenario: Like a Product
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success list all products"
    And I should see "10" in the "like" field
    And I should see "10" in the results
    When I press the "Like" button
    Then I should see the message "Success like a product"
    And I should see "11" in the "like" field
    When I press the "Like" button
    Then I should see the message "Success like a product"
    And I should see "12" in the "like" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success list all products"
    And I should see "12" in the results

Scenario: Disable a Product
    When I visit the "Home Page"
    And I set the "Name" to "coke"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "coke" in the results
    And I should not see "milk" in the results
    When I press the "Disable" button
    Then I should see the message "Success disable a product"
    And I should see "True" in the "Disable" dropdown

