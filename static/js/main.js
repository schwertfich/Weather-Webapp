// Function for location
var x = document.getElementById("cords");
    
    function getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
      } else { 
        x.innerHTML = "Geolocation is not supported by this browser.";
      }
    }
    
    function showPosition(position) {
      var newUrl = location.protocol + "//" + location.host + location.pathname + ""
      newUrl = newUrl + "?position&lat="+ position.coords.latitude + "&long=" + position.coords.longitude + "&units=" + document.getElementById("units").value
      document.location.href = newUrl
    }

    function showError(error) {
      switch(error.code) {
        case error.PERMISSION_DENIED:
          x.innerHTML = "User denied the request for Geolocation."
          break;
        case error.POSITION_UNAVAILABLE:
          x.innerHTML = "Location information is unavailable."
          break;
        case error.TIMEOUT:
          x.innerHTML = "The request to get user location timed out."
          break;
        case error.UNKNOWN_ERROR:
          x.innerHTML = "An unknown error occurred."
          break;
      }
    }

// Line Chart for Forecast

var xmlhttp = new XMLHttpRequest();
var url = "https://192.168.178.25/static/js/hourlyforecast.json"
xmlhttp.open("GET", url, true);
xmlhttp.send();
xmlhttp.onreadystatechange = function(){
  if(this.readyState == 4 && this.status == 200){
    var data = JSON.parse(this.responseText);
    //console.log(data);
    var time = data.hourly.map(function(elem) {
      return elem.dt;
    });
    //console.log(time)    
    var hour = data.hourly.map(function(elem) {
      return elem.temp;
    });
    //console.log(hour);

    var ctx = document.getElementById('canvas').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time,
            datasets: [{
                label: 'Tempereture',
                data: hour,
                backgroundColor: 'transperent',
                borderColor: "red",
                borderWidth: 4
            }]
        },
        options: {
          elements:{
            line:{
              tension:0.1
            }
          },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
  }
}
