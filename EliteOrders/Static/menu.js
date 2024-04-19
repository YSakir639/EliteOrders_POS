// Add event listener to the dish-img-button element
document.getElementById('dish-img-button').addEventListener('click', function () {
    // When the button is clicked, trigger a click event on the dish-img-file input element
    document.getElementById("dish-img-file").click();
});

// Add event listener to the dish-img-file 
document.getElementById("dish-img-file").addEventListener("change", function () {
    // Get the selected file
    const files = this.files[0];
    // Check if a file is selected
    if (files) {
        // Create a FileReader object to read the selected file
        const fileReader = new FileReader();
        // Read the selected file 
        fileReader.readAsDataURL(files);
        // When the file is loaded
        fileReader.addEventListener("load", function () {
            // Display the selected image preview inside the dish-img-button element
            document.getElementById("dish-img-button").innerHTML = '<img src="' + this.result + '" id="dish-selected-img" />';
        });
    }
});


// Establish a connection to the Socket.IO server
var socket = io();

// Select all elements with the class "delete-badge"
document.querySelectorAll('.delete-badge').forEach(function (badge) {
    // Add a click event listener to each delete badge
    badge.addEventListener('click', function () {
        // Find the parent element of the badge, which should have the item ID
        var item_card = badge.parentElement;
        // Extract the item ID from the parent element
        var id = item_card.id;
        // Log the IDs to the console for debugging purposes
        console.log(item_card, id);
        // Emit a 'delete-item' event to the server with the item ID
        socket.emit('delete-item', { id: id });
        // Remove the  the entire item from the DOM (Document object model)
        item_card.remove();
    });
});
