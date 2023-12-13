$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_price").val(res.price);
        $("#product_category").val(res.category);
        $("#product_inventory").val(res.inventory);
        if (res.available == true) {
            $("#product_available").val("true");
        } else {
            $("#product_available").val("false");
        }
        $("#product_created_date").val(res.created_date);
        $("#product_modified_date").val(res.modified_date);
        $("#product_like").val(res.like);
        if (res.disable == true) {
            $("#product_disable").val("true");
        } else {
            $("#product_disable").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_price").val("");
        $("#product_category").val("");
        $("#product_inventory").val("");
        $("#product_available").val("");
        $("#product_created_date").val("");
        $("#product_modified_date").val("");
        $("#product_like").val("");
        $("#product_disable").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {


        let name = $("#product_name").val();
        let price = $("#product_price").val();
        let category = $("#product_category").val();
        let inventory = $("#product_inventory").val();
        let available = $("#product_available").val() == "true";
        let created_date = $("#product_created_date").val();
        let modified_date = $("#product_modified_date").val();
        let like = $("#product_like").val();
        let disable = $("#product_disable").val() == "true";

        let data = {
            "name": name,
            "price": price,
            "category": category,
            "inventory": inventory,
            "available": available,
            "created_date": created_date,
            "modified_date": modified_date,
            "like": like,
            "disable": disable
        }

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let id = $("#product_id").val();
        let name = $("#product_name").val();
        let price = $("#product_price").val();
        let category = $("#product_category").val();
        let inventory = $("#product_inventory").val();
        let available = $("#product_available").val() == "true";
        let created_date = $("#product_created_date").val();
        let modified_date = $("#product_modified_date").val();
        let like = $("#product_like").val();
        let disable = $("#product_disable").val() == "true";

        let data = {
            "name": name,
            "price": price,
            "category": category,
            "inventory": inventory,
            "available": available,
            "created_date": created_date,
            "modified_date": modified_date,
            "like": like,
            "disable": disable
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/products/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#like-btn").click(function () {

        let id = $("#product_id").val();
        // let name = $("#product_name").val();
        // let price = $("#product_price").val();
        // let category = $("#product_category").val();
        // let inventory = $("#product_inventory").val();
        // let available = $("#product_available").val() == "true";
        // let created_date = $("#product_created_date").val();
        // let modified_date = $("#product_modified_date").val();
        // let like = $("#product_like").val();
        // let disable = $("#product_disable").val() == "false";

        // let data = {
        //     "name": name,
        //     "price": price,
        //     "category": category,
        //     "inventory": inventory,
        //     "available": available,
        //     "created_date": created_date,
        //     "modified_date": modified_date,
        //     "like": like,
        //     "disable": disable
        // }

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/products/${id}/like`,
                // contentType: "application/json",
                // data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success like a product")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Disable a Product
    // ****************************************

    $("#disable-btn").click(function () {

        let id = $("#product_id").val();
        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/products/${id}/disable`
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success disable a product")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        if (product_id!=""){
            let ajax = $.ajax({
                type: "GET",
                url: `/api/products/${product_id}`,
                contentType: "application/json",
                data: ''
            })
    
            ajax.done(function(res){
                //alert(res.toSource())
                update_form_data(res)
                flash_message("Success retrieve the product")
            });
    
            ajax.fail(function(res){
                clear_form_data()
                flash_message("Fail retrieve the product (product " + product_id + " does not exist)")
            });
        }else{
            clear_form_data()
            flash_message("Fail retrieve the product (product id is not provided)")
        }
    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();
        if (product_id!=""){
            let ajax = $.ajax({
                type: "DELETE",
                url: `api/products/${product_id}`,
                contentType: "application/json",
                data: '',
            })
    
            ajax.done(function(res){
                clear_form_data()
                flash_message("Success delete the product")
            });
    
            ajax.fail(function(res){
                clear_form_data()
                flash_message("Fail delete the product (product " + product_id + " does not exist)")
            });
        }else{
            clear_form_data()
            flash_message("Fail delete the product (product id is not provided)")
        }
        
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let available = $("#product_available").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }

        if (available === "true") {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }
        if(available === "false"){
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/products?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Inventory</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Created_date</th>'
            table += '<th class="col-md-2">Modified_date</th>'
            table += '<th class="col-md-2">like</th>'
            table += '<th class="col-md-2">disable</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}">
                           <td>${product.id}</td>
                           <td>${product.name}</td>
                           <td>${product.price}</td>
                           <td>${product.category}</td>
                           <td>${product.inventory}</td>
                           <td>${product.available}</td>
                           <td>${product.created_date}</td>
                           <td>${product.modified_date}</td>
                           <td>${product.like}</td>
                           <td>${product.disable}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            if (queryString == ""){
                flash_message("Success list all products")
            }else{
                flash_message("Success")
            }
            
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
