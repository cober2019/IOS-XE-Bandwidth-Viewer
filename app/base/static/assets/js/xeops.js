

function getBandwidthUsage(val){
 $.ajax({
  url: '/interface_stats',
  type: 'POST',
  data: {'action': val},
  success: function(response) {
       interfaceBandwidth(val);
  },
 });
}


function openBandwidthPage(val){
 $.ajax({
  url: '/interface_stats',
  type: 'POST',
  data: {'openPage': val},
  success: function(response) {
  console.log(val)
     var wind_two = window.open("", "", "width=1000,height=500,scrollbars=yes");
      wind_two.location.assign('/interface_stats');
    },
 });
}

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

function getBandwidthIn(interface, callback){
 $.ajax({
  url: '/interface_stats',
  type: 'POST',
  data: {'action': 'bandwidth', 'direction': 'in', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}


function getBandwidthOut(interface, callback){
 $.ajax({
  url: '/interface_stats',
  type: 'POST',
  data: {'action': 'bandwidth', 'direction': 'out', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}

function getDiscardsIn(interface, callback){
 $.ajax({
  url: '/interface_stats',
  type: 'POST',
  data: {'action': 'discards', 'direction': 'in', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}


function getDiscardsOut(interface, callback){
 $.ajax({
  url: '/interface_stats',
  type: 'POST',
  data: {'action': 'discards', 'direction': 'out', 'interface': interface },
  success: function(response) {
    callback(response)
    }
 });
}


function getCpuUsage(callback){
     $.ajax({
      async: false,
      url: '/interface_stats',
      type: 'POST',
      data: {'action': 'cpu'},
      success: function(response) {
        callback(response)
        }
     });
    }












