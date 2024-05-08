let pounds = Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
});
// Initialize variables
var subTotal = 0;
var totalItems = 0;
var total=0;
var items = {} // Object to store the items

// Event listener for clicking on items
document.querySelector('.items').addEventListener('click', function (event) {
    // Find the closest parent element with the class "card" that was clicked
    // this will get the "card" even if the user clicks the inner tags of the items (eg: the name or the img )
    card = event.target.closest(".card")
     // Extract the ID of the card
     // the ID of the card also represents the ID of the Items in database
    id = card.id

    // check if the closest card is found
    if (card) {
        // Extract the badge element associated with the clicked card
        var badge = card.children[1]
        // Increment the badge count by 1
        badge.innerHTML = Number(badge.innerHTML) + 1;
        // Set the display style of the badge to "block" (this is done to display the badge when first clicked )
        badge.style.display = "block";

        // If the item is already added, update its quantity 
        if (Number(badge.innerHTML) > 1) {
            items[id] = [card.children[2].children[0].innerHTML, items[id][1] += 1]
            var elements = document.querySelectorAll('.qty');
            elements.forEach(function (element) {
                if (element.nextElementSibling.innerHTML == card.children[2].children[0].innerHTML) {
                    element.innerHTML = "X" + String(parseInt(element.innerHTML.substring(1)) + 1)
                }
                return;
            });
        }

        // If the item is added for the first time, add it to the table in orders window
        if (Number(badge.innerHTML) == 1) {
             // Insert a new row in the display table
            var table = document.querySelector("#display-item")
            row = table.insertRow(-1);
            item_qty = row.insertCell(0)
            item_name = row.insertCell(1);
            item_price = row.insertCell(2);
            // Set quantity to 1 
            item_qty.innerHTML = "X1";
            // Add the "qty" class to the item_qty cell (this will be used to increment it when clicked multiple times)
            item_qty.classList.add("qty");
            //Set item_name , item_price cells with the item name and item price from the card 
            item_name.innerHTML = card.children[2].children[0].innerHTML;
            item_price.innerHTML = card.children[2].children[1].innerHTML;

            // Add a new entry to the 'items' object with the card ID as the key
            // The value is a 2d array containing the name of the item 
            // and the quantity of the item, which is set to 1 since it's the first occurrence
            items[id] = [card.children[2].children[0].innerHTML, 1]
        }
        // increment the subTotal variable adding the items price 
        // item price is extracted from the html (and sliced to ignore the currency (£) symbol ) and casted to float to perform arithemetics.
        subTotal += parseFloat(item_price.innerHTML.substring(1))
        // Update the innerHTML of the element with the id "total" to display the updated subtotal.
        // this will make the total equal as subtotal until discount is applied
        // document.getElementById("total").innerHTML=subTotal;
        document.getElementById("total").innerHTML=pounds.format(subTotal);
        total=subTotal
        // Update the innerHTML of the element with the id "sub-total" to display the updated subtotal after casting it as a float.
        // document.getElementById("sub-total").innerHTML = parseFloat(subTotal);
        document.getElementById("sub-total").innerHTML = pounds.format(subTotal);
        // increment totalitems by 1 (this represents the total items that the customers has ordered)
        totalItems += 1
        // Update the innerHTML of the element with the id "total-items" to display the updated total items count.
        document.getElementById("total-items").innerHTML = totalItems
    }
}, false);


var discount = 0
// Add event listener to the discount button
document.getElementById("discount-btn").addEventListener("click", function(event) {
    // Retrieve discount value from the discount input field
    discount = parseFloat(document.getElementById("discount-input").value);

    // Check if discount value is not valid or empty, then return
    if (!discount || isNaN(discount) || discount <= 0) {
        return;
    }
    // Calculate total after applying discount
    total = subTotal - ((subTotal * discount) / 100);
    // Update total displayed on the webpage
    // document.getElementById("total").innerHTML = total;
    document.getElementById("total").innerHTML = pounds.format(total);
});


// Add event listener to the clear button
document.getElementById("clear-btn").addEventListener('click', function () {
    // Reload the page to clear all data
   location.reload();
  });



// Connect to the Socketio server
var socket = io();

// Add event listener to the card button and cash button, calling the handleclick function
document.getElementById('card-btn').addEventListener('click', handleclick);
document.getElementById('cash-btn').addEventListener('click', handleclick);

// Function to handle the click event
function handleclick(event) {
    // Get notes from the notes input field
    var notes = document.querySelector('#notes').value;

    // Emit an 'order' event to the server with order details based on the clicked button
    if (event.target.id == "cash-btn") {
        socket.emit('order', { notes: notes, items: items, discount: discount, total: total, paymentMethod: "cash" });
    } else {
        socket.emit('order', { notes: notes, items: items, discount: discount, total: total, paymentMethod: "card" });
    }
    location.reload();
}
