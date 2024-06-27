// static/accounts/js/map.js

// Initialize Google Map
function initMap() {
    // Set the initial location to a default value
    var initialLocation = { lat: 40.712776, lng: -74.005974 }; // Example: New York City

    // Create a new map instance
    var map = new google.maps.Map(document.getElementById('map'), {
        center: initialLocation,
        zoom: 12 // Adjust the zoom level as needed
    });

    // Create a marker for the initial location
    var marker = new google.maps.Marker({
        position: initialLocation,
        map: map,
        draggable: true // Allow marker to be draggable by user
    });

    // Add event listener to marker to update location when dragged
    google.maps.event.addListener(marker, 'dragend', function(event) {
        // Get updated marker position
        var updatedLocation = marker.getPosition();
        // Update the form fields with the updated latitude and longitude
        document.getElementById('latitude').value = updatedLocation.lat();
        document.getElementById('longitude').value = updatedLocation.lng();
    });
}
