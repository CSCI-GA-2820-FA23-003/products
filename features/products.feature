Feature: The products service back-end
    As a Products Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name         | price | category   | inventory | available |  created_date | modified_date | like | disable |
        | coke         | 3.99  | beverage   | 999       |    True   |  2023-11-10   |   2023-11-10  |  10  |  False  |
        | milk         | 5.5   | dairy      | 15        |    True   |  2023-11-10   |   2023-11-10  |  10  |  False  |
        | Kale         | 2.5   | fresh food | 0         |    False  |  2023-11-10   |   2023-11-10  |  10  |  True   |
        | ice cream    | 6.69  | frozen     | 90        |    True   |  2023-11-10   |   2023-11-10  |  10  |  False  |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Like a Product
    When I visit the "Home Page"
    And I set the "name" to "Switch"
    And I set the "price" to "299.9"
    And I set the "category" to "Game device"
    And I set the "inventory" to "5"
    And I set the "created_date" to "2023-11-10"
    And I set the "modified_date" to "2023-11-10"
    And I set the "like" to "100"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    When I paste the "Id" field
    And I press the "Like" button
    Then I should see the message "Success like a product"
    And I should not see "1" in the results
    And I should not see "2" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "airpods"
    And I set the "Price" to "249.9"
    And I set the "Category" to "Headphone"
    And I set the "Inventory" to "3"
    And I set the "modified_date" to "2023-11-10"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "airpods" in the "Name" field
    When I change "Name" to "airpods pro"
    And I change "Price" to "299.9"
    And I change "Like" to "10"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "airpods pro" in the "Name" field
    And I should see "299.9" in the "Price" field
    And I should see "Headphone" in the "Category" field
    And I should see "3" in the "Inventory" field
    And I should see "10" in the "Like" field
