$(() => initMap = function() {
    var uluru = {lat: 46.7682504, lng: 23.6114152};
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 15, center: uluru});
});
