$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var em1 = this.parentNode.children[2];
    console.log("pid =", id);

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log("data =", data);
            em1.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var em1 = this.parentNode.children[2];
    console.log("pid =", id);

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data){     
            em1.innerText = data.quantity;
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    });
});

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var em1 = this
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data){     
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            em1.parentNode.parentNode.parentNode.parentNode.remove()
        }
    });
});


// AJAX for increasing quantity for plastic items
document.querySelectorAll('.plastic-plus-cart').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent default action
        const itemId = this.dataset.id;
        fetch(`/add_plastic_quantity/${itemId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.quantity) {
                    document.getElementById(`plastic-quantity-${itemId}`).textContent = data.quantity;
                    document.getElementById(`plastic-total-supercoins-${itemId}`).textContent = data.total_supercoins;
                }
            });
    });
});

// AJAX for decreasing quantity for plastic items
document.querySelectorAll('.plastic-minus-cart').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent default action
        const itemId = this.dataset.id;
        fetch(`/reduce_plastic_quantity/${itemId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.quantity > 0) {
                    document.getElementById(`plastic-quantity-${itemId}`).textContent = data.quantity;
                    document.getElementById(`plastic-total-supercoins-${itemId}`).textContent = data.total_supercoins;
                } else {
                    document.getElementById(`plastic-item-${itemId}`).remove();  // Remove item if quantity is zero
                }
            });
    });
});

// AJAX for removing plastic items
document.querySelectorAll('.plastic-remove-cart').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent default action
        const itemId = this.dataset.id;
        fetch(`/remove_plastic_item/${itemId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'Item removed') {
                    document.getElementById(`plastic-item-${itemId}`).remove();  // Remove item from DOM
                }
            });
    });
});
