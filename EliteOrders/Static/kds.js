// Initialize socket connection to the server
var socket = io();

// Listen for "kds-data" event from the server
socket.on("kds-data", (arg) => {
    // Reload the page when "kds-data" event is received
    location.reload();
});

// Select all elements with the class "ready-btn"
var readyButtons = document.querySelectorAll('.ready-btn');

// Loop through each ready button and add event listener
readyButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        order = event.target.closest(".col")
        socket.emit('order-complete', {order:order.id});
        order.remove()
    });
});

////////////////////////////////////////////////////////////////////

// function namee(receivedTime) {
//         const currentTime = new Date();
//         const elapsedTime = currentTime - receivedTime;
//         const minutes = Math.floor(elapsedTime / (1000 * 60));
//         const seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
//         const formattedElapsedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
//         document.querySelectorAll(".nav").forEach(nav=>{
//             nav.querySelector(".elapsed-time").innerHTML=formattedElapsedTime;
//         })
//     }


// const x= new Date()
// // Call the updateElapsedTimes function periodically (e.g., every second)
// setInterval(() => namee(x), 1000);
