

function getBandwidthUsage(val){
 $.ajax({
  url: '/interface_stats/' + val,
  type: 'POST',
  data: {'action': val},
  success: function(response) {
       interfaceBandwidth(val);
  },
 });
}


function openBandwidthPage(val){
 $.ajax({
  url: '/interface_stats/' + val,
  type: 'POST',
  data: {'openPage': val},
  success: function(response) {
  console.log(val)
     var wind_two = window.open("", "", "width=1000,height=500,scrollbars=yes");
      wind_two.location.assign('/interface_stats/' + val);
      var windowCheck = setInterval(function(){if (wind_two.closed === true){
        clearInterval(windowCheck);
        //call funtions to remove polling objects with the window is closed
        endPollingBandwidth(val)}
      }, 50)
    },
 });
}

// Sends the interface back to the python function to remove objects from dictionary
function endPollingBandwidth(val){
 $.ajax({
  url: '/interface_stats/' + val,
  type: 'POST',
  data: {'endPoll': val},
  success: function(response){}
 });
}

//Get cli view of interface statistics, opend pop up window
function moreIntDetails(val){
console.log(val)
 $.ajax({
  url: '/int_details',
  type: 'POST',
  data: {'details': val},
  success: function(response) {
      var details_window = window.open("", "", "width=700,height=800,scrollbars=yes");
        details_window.document.write(response);
  },
 });
}

// Get interface statistics and return to caller
function getBandwidthIn(interface, callback){
 $.ajax({
  url: '/interface_stats/' + interface,
  type: 'POST',
  data: {'action': 'bandwidth', 'direction': 'in', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}

// Get interface statistics and return to caller
function getBandwidthOut(interface, callback){
 $.ajax({
  url: '/interface_stats/' + interface,
  type: 'POST',
  data: {'action': 'bandwidth', 'direction': 'out', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}

// Get interface statistics and return to caller
function getDiscardsIn(interface, callback){
 $.ajax({
  url: '/interface_stats/' + interface,
  type: 'POST',
  data: {'action': 'discards', 'direction': 'in', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}

// Get interface statistics and return to caller
function getDiscardsOut(interface, callback){
 $.ajax({
  url: '/interface_stats/' + interface,
  type: 'POST',
  data: {'action': 'discards', 'direction': 'out', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}

// Not used
function getCpuUsage(callback){
     $.ajax({
      url: '/index',
      type: 'POST',
      data: {'action': 'cpu'},
      success: function(response) {
        callback(response)
        }
     });
    }

// Get interface statistics and return to caller
function getQos(interface, callback){
     $.ajax({
      url: '/qos_stats/' + interface,
      type: 'POST',
      data: {'action': 'qos', 'interface': interface },
      success: function(response) {
        callback(response)
        }
     });
    }

function openQosPage(val){
 $.ajax({
  url: '/qos_stats/' + val,
  type: 'POST',
  data: {'openPage': val},
  success: function(response) {
  console.log(val)
     var wind_two = window.open("", "", "width=1000,height=500,scrollbars=yes");
      wind_two.location.assign('/qos_stats/'+ val);
        var windowCheck = setInterval(function(){if (wind_two.closed === true){
        clearInterval(windowCheck);
        //call funtions to remove polling objects with the window is closed
        endPollingQos(val)}
      }, 50)
    },
 });
}

// Sends the interface back to the python function to remove objects from dictionary
function endPollingQos(val){
 $.ajax({
  url: '/qos_stats/' + val,
  type: 'POST',
  data: {'endPoll': val},
  success: function(response){}
 });
}













