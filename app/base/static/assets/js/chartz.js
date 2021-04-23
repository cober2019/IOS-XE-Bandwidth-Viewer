Chart.defaults.datasets.line.borderColor = 'orange';
Chart.defaults.datasets.line.backgroundColor = 'orange';


var mbpsOptionsOutQos = {
    responsive: true,
    plugins: {
    legend: {
    display: false,
          },
          },
    scales: {
         x: {
            title: {
                display: true,
                text: 'Seconds',

            }
        }
    }
};

var mbpsOptionsIn = {
    responsive: true,
    plugins: {
    legend: {
    display: false,
          },
          title: {
            display: true,
            text: 'In Mbps',
            color: 'back',
            align: 'center',
            font:{
             opacity: 1,
             fontFamily: "Arial",
             fontStyle: 'italic',
             fontWeight: 'regular',
             color: "#E27F2D",
             size: '23px'
         },
          }
        },
    scales: {
        y: {
        min: 0,
        grid: {
                borderColor: 'black'
                },
            ticks: {
                stepSize: 5,
            }
        },
         x: {
            grid: {
                borderColor: 'black'
            },
            ticks: {
                stepSize: 1,
                color: 'black'
            },
            title: {
                display: true,
                text: 'Seconds'
            }
        }
    }
};

var mbpsOptionsOut = {
    responsive: true,
    plugins: {
    legend: {
    display: false,
          },
          labels: {
                font: {
                    size: 30
            }
          },
          title: {
            display: true,
            text: 'Out Mbps',
            color: 'back',
            align: 'center',
            font:{
             opacity: 1,
             fontFamily: "Arial",
             fontStyle: 'italic',
             fontWeight: 'regular',
             color: "#E27F2D",
             size: '23px'
         },
          }
        },
    scales: {
        y: {
        min: 0,
        grid: {
                borderColor: 'black'
                },
            ticks: {
                stepSize: 5,
            }
        },
         x: {
         grid: {
                borderColor: 'black'
         },
            ticks: {
                stepSize: 1,
                },
            title: {
                display: true,
                text: 'Seconds'
            }
        }
    }
};

var discardOptionsOut = {
    responsive: true,
    plugins: {
    legend: {
    display: false,
          },
          title: {
            display: true,
            text: 'Out Discards',
            color: 'back',
            align: 'center',
            font:{
             opacity: 1,
             fontFamily: "Arial",
             fontStyle: 'italic',
             fontWeight: 'regular',
             color: "#E27F2D",
             size: '23px'
            },
          }
        },
    scales: {
        y: {
        min: 0,
        grid: {
                borderColor: 'black'
                },
            ticks: {
                stepSize: 1,
            }
        },
        x: {
        grid: {
                borderColor: 'black'
        },
            ticks: {
                stepSize: 1,
             },
            title: {
                display: true,
                text: 'Seconds'
            }
        }
    }
};

var discardOptionsIn = {
    responsive: true,
    plugins: {
    legend: {
    display: false,
          },
          title: {
            display: true,
            text: 'In Discards',
            color: 'back',
            align: 'center',
            font:{
             opacity: 1,
             fontFamily: "Arial",
             fontStyle: 'italic',
             fontWeight: 'regular',
             color: "#E27F2D",
             size: '23px'
            },
          }
        },
    scales: {
        y: {
        min: 0,
        grid: {
                borderColor: 'black',
                },
            ticks: {
                stepSize: 1,
            }
        },
         x: {
         grid: {
                borderColor: 'black'
         },
            ticks: {
                stepSize: 1,
             },
            title: {
                display: true,
                text: 'Seconds'
            }
        }
    }
};

function removeGif(completeCharts){
    // Check completed chart count, remove loading GIF
    if (completeCharts == 4){
        $(".se-pre-con").fadeOut("slow");
    }

};

function initializeCharts(interface) {


var chartsOut = ['0'];
cycleCheck = 0
setInterval(getBandwidth, 15000);
// Count chart completion, add one when each chart is completed
completeCharts = 0

function getBandwidth(){
    getBandwidthOut( interface, function(response) {
    var time = new Date()
    if (cycleCheck < 2){
        cycleCheck += 1
        getBandwidth();
        }
     else if (chartsOut.length == 1){

            var ctx = document.getElementById('interfaceUsageOut')
            myChart = new Chart(ctx, {
            type: 'line',
            options: mbpsOptionsOut,
            data: {
            labels: [time.getSeconds()],
            datasets: [{
                label: 'Mbps Out',
                data: [parseInt(response)],
                fill: false,
                tension: .5
                        }],

                        }

                    }),

                    chartsOut.splice(1, 1, myChart);
                    completeCharts +=1;
                    removeGif(completeCharts);
       }
       else {
            var time = new Date()

            chartsOut[1].data.datasets.forEach((dataset) => {

            if (dataset.data.length >= 10){
                chartsOut[1].data.labels.push(time.getSeconds());
                dataset.data.push(parseInt(response));
                chartsOut[1].data.labels.shift();
                dataset.data.shift();
            }
            else{
                chartsOut[1].data.labels.push(time.getSeconds());
                dataset.data.push(parseInt(response));
                }
            });
            chartsOut[1].update();

            }
        });
       }

cycleCheckOutDis = 0;
var chartsDisOut = ['0'];
setInterval(interfaceDiscardsOut, 16000);

function interfaceDiscardsOut(){
    getDiscardsOut( interface, function(response) {
    var time = new Date();
    if (cycleCheckOutDis < 2){
        cycleCheckOutDis += 1;
        interfaceDiscardsOut();
        }
     else if (chartsDisOut.length == 1){

            var ctx = document.getElementById('interfaceDiscardsOut')
            myChart = new Chart(ctx, {
            type: 'line',
            options: discardOptionsOut,
            data: {
            labels: [time.getSeconds()],
            datasets: [{
                label: 'Discards Out',
                data: [parseInt(response)],
                fill: false,
                borderColor: 'red',
                scaleStartValue : 0 ,
                tension: .5
                        }],
                        }
                    });
                    chartsDisOut.splice(2, 1, myChart);
                    completeCharts +=1;
                    removeGif(completeCharts);
       }
       else {
            var time = new Date()

            chartsDisOut[1].data.datasets.forEach((dataset) => {
            if (dataset.data.length >= 10){
                chartsDisOut[1].data.labels.push(time.getSeconds());
                dataset.data.push(parseInt(response));
                chartsDisOut[1].data.labels.shift();
                dataset.data.shift();
            }
            else{
                chartsDisOut[1].data.labels.push(time.getSeconds());
                dataset.data.push(parseInt(response));
                }
            });
            chartsDisOut[1].update();

            }
        });

       }

cycleCheckIn = 0;
var chartsIn = ['0'];
setInterval(inBandwidth, 13000);

function inBandwidth(){
    getBandwidthIn( interface, function(response) {

    var time = new Date()
    if (cycleCheckIn < 2){
        cycleCheckIn += 1
        inBandwidth();
        }
    else if (chartsIn.length == 1){

        var ctx = document.getElementById('interfaceUsageIn')
        myChart = new Chart(ctx, {
        type: 'line',
        options: mbpsOptionsIn,
        data: {
        labels: [time.getSeconds()],
        datasets: [{
            label: 'Mbps In',
            data: [parseInt(response)],
            fill: false,
            tension: .5
                    }],
                    }
                });
                chartsIn.splice(2, 1, myChart);
                completeCharts +=1;
                removeGif(completeCharts);
       }
    else {
        var time = new Date()

        chartsIn[1].data.datasets.forEach((dataset) => {
        if (dataset.data.length >= 10){
            chartsIn[1].data.labels.push(time.getSeconds());
            dataset.data.push(parseInt(response));
            chartsIn[1].data.labels.shift();
            dataset.data.shift();
        }
        else{
            chartsIn[1].data.labels.push(time.getSeconds());
            dataset.data.push(parseInt(response));
            }
        });

        chartsIn[1].update();
        }

        })

       }

cycleCheckInDis = 0;
var chartsDisIn = ['0'];
setInterval(inDiscards, 16000);

function inDiscards(){
    getDiscardsIn( interface, function(response) {
    var time = new Date()
    if (cycleCheckInDis < 2){
        cycleCheckInDis += 1
        inDiscards();
        }
     if (chartsDisIn.length == 1){

            var ctx = document.getElementById('interfaceDiscardsIn')
            myChart = new Chart(ctx, {
            type: 'line',
            options: discardOptionsIn,
            data: {
            labels: [time.getSeconds()],
            datasets: [{
                label: 'Discards In',
                data: [parseInt(response)],
                fill: false,
                borderColor: 'red',
                tension: .5
                        }],
                        }
                    });
                    chartsDisIn.splice(2, 1, myChart)
                    completeCharts +=1
                    removeGif(completeCharts)
       }
       else {
            var time = new Date()
            chartsDisIn[1].data.labels.push(time.getSeconds());
            chartsDisIn[1].data.datasets.forEach((dataset) => {
                if (dataset.data.length >= 10){
                    dataset.data.push(parseInt(response));
                    chartsDisIn[1].data.labels.shift()
                    dataset.data.shift();
                }
                else{
                    dataset.data.push(parseInt(response));
                    }
                });
                chartsDisIn[1].update();
                }
            });
       }

}

var parentBandwidth = 0
function buildHtml(element, v, iteration){

    // Dynamically build HTML elements

    var newLine = document.createElement("br");
    var header = document.createElement("h2");

    if(v['who_am_i'] == 'parent'){
        parentBandwidth = v['allocation']
        var headerText = document.createTextNode("Queue Parent: " + v['queue_name'] + " Allocation: " + v['allocation'] + "Mbps");
    }
    else{
        var headerText = document.createTextNode("Child Policy: " + v['parent_path'].split(' ')[2] +
                                            " | Queue: " + v['queue_name'] + " Allocation: " +
                                            ( v['allocation'] / 100) * parentBandwidth + " Mbps (" + v['allocation'] + '%)');
        }

    header.style.color = 'black';
    header.style.textAlign = 'left';
    header.style.margin = '5px 0px 5px 30px';
    header.append(headerText);
    element.append(header);

    // Access Qos policy data from out JSON object. Build HTML elements conditionally depend on Qos policy
    if (v['match'] != undefined){
        var matchTypeOne = document.createElement("h3");
        var policyTextOne = document.createTextNode('Match Type: ' + v['match'][0]['match_what']);
        matchTypeOne.style.color = 'black';
        matchTypeOne.style.textAlign = 'left';
        matchTypeOne.style.margin = '5px 0px 5px 60px';
        matchTypeOne.append(policyTextOne);
        element.append(matchTypeOne);

        if (v['match'].length == 2){
            if(v['match'][1]['match_list'] != undefined){
                var matchTypeTwo = document.createElement("h3");
                var policyTextTwo = document.createTextNode('Match: ' + v['match'][1]['match_list']);
                matchTypeTwo.style.color = 'black';
                matchTypeTwo.style.textAlign = 'left';
                matchTypeTwo.style.margin = '5px 0px 5px 90px';
                matchTypeTwo.append(policyTextTwo);
                element.append(matchTypeTwo);
            }
            else if(v['match'][1]['vlan'] != undefined){
                var matchTypeFour = document.createElement("h3");
                var policyTextFour = document.createTextNode('Match: ' + v['match'][1]['vlan']);
                matchTypeFour.style.color = 'black';
                matchTypeFour.style.textAlign = 'left';
                matchTypeFour.style.margin = '5px 0px 5px 60px';
                matchTypeFour.append(policyTextFour);
                element.append(matchTypeFour);
            }
            else if(v['match'][1]['protocols'] != undefined){
                var matchTypeFive = document.createElement("h3");
                var policyTextFive = document.createTextNode('Match: ' + v['match'][1]['protocols'])
                matchTypeFive.style.color = 'black'
                matchTypeFive.style.textAlign = 'left';
                matchTypeFive.style.margin = '5px 0px 5px 60px';
                matchTypeFive.append(policyTextFive);
                element.append(matchTypeFive);
            }
            else if(v['match'][1]['access_group'] != undefined){
                var matchTypeSix = document.createElement("h3")
                var policyTextSix = document.createTextNode('Match: ' + v['match'][1]['access_group']);
                matchTypeSix.style.color = 'black';
                matchTypeSix.style.textAlign = 'left';
                matchTypeSix.style.margin = '5px 0px 5px 60px';
                matchTypeSix.append(policyTextSix);
                element.append(matchTypeSix);
            }
            else if(v['match'][1]['sec_group'] != undefined){
                var matchTypSeven = document.createElement("h3");
                var policyTextSeven = document.createTextNode('Match: ' + v['match'][1]['sec_group']);
                matchTypeSeven.style.color = 'black';
                matchTypeSeven.style.textAlign = 'left';
                matchTypeSeven.style.margin = '5px 0px 5px 60px';
                matchTypeSeven.append(policyTextSeven);
                element.append(matchTypeSeven);
            }
            else if(v['match'][1]['atm'] != undefined){
                var matchTypeEight = document.createElement("h3");
                var policyTextEight = document.createTextNode('Match: ' + v['match'][1]['atm']);
                matchTypeEight.style.color = 'black';
                matchTypeEight.style.textAlign = 'left';
                matchTypeEight.style.margin = '5px 0px 5px 60px';
                matchTypeEight.append(policyTextEight);
                element.append(matchTypeEight);
            }
            else if(v['match'][1]['discards'] != undefined){
                var matchTypeNine = document.createElement("h3");
                var policyTextNine = document.createTextNode('Match: ' + v['match'][1]['discards']);
                matchTypeNine.style.color = 'black';
                matchTypeNine.style.textAlign = 'left';
                matchTypeNine.style.margin = '5px 0px 5px 60px';
                matchTypeNine.append(policyTextNine)
                element.append(matchTypeNine);
            }
            else if(v['match'][1]['ip']  != undefined){
                var matchTypeTen = document.createElement("h3");
                var policyTextTen = document.createTextNode('Match: ' + v['match'][1]['ip']);
                matchTypeTen.style.color = 'black';
                matchTypeTen.style.textAlign = 'left';
                matchTypeTen.style.margin = '5px 0px 5px 60px';
                matchTypeTen.append(policyTextTen);
                element.append(matchTypeTen);
            };
        };
    };

    var row1 = document.createElement("div");
    row1.className = "row";

    var row = document.createElement("div");
    row.className = "row";

    ///

    var col = document.createElement("div");
    col.className = "col-xl-12";

    var chartDiv = document.createElement('canvas');
    chartDiv.id = v['parent_path'] + v['queue_name'] + 'One';
    chartDiv.style.height = "200px";
    chartDiv.style.width = "100%";
    chartDiv.setAttribute = ('box-sizing', "border-box");
    chartDiv.setAttribute = ('height', '200px');
    chartDiv.style.margin = '15px 0px 30px 0px';


    ////

    var col3 = document.createElement("div");
    col3.className = "col-xl-3";

    var chartDiv3 = document.createElement('canvas');
    chartDiv3.id = v['parent_path'] + v['queue_name'] + 'Three';
    chartDiv3.style.height = "200px";
    chartDiv3.style.width = "100%";


    ////

    var col4 = document.createElement("div");
    col4.className = "col-xl-3";

    var chartDiv4 = document.createElement('canvas');
    chartDiv4.id = v['parent_path'] + v['queue_name'] + 'Four';
    chartDiv4.style.height = "200px";
    chartDiv4.style.width = "100%";

    ////

    var col5 = document.createElement("div");
    col5.className = "col-xl-3";

    var chartDiv5 = document.createElement('canvas');
    chartDiv5.id = v['parent_path'] + v['queue_name'] + 'Five';
    chartDiv5.style.height = "200px";
    chartDiv5.style.width = "100%";


    ////

    var col6 = document.createElement("div");
    col6.className = "col-xl-3";

    var chartDiv6 = document.createElement('canvas');
    chartDiv6.id = v['parent_path'] + v['queue_name'] + 'Six';
    chartDiv6.style.height = "200px";
    chartDiv6.style.width = "100%";


    ///


    row1.append(col);
    row.append(col4);
    row.append(col3);
    row.append(col5);
    row.append(col6);
    col.append(chartDiv);
    col3.append(chartDiv3);
    col4.append(chartDiv4);
    col5.append(chartDiv5);
    col6.append(chartDiv6);

    element.append(row1);
    element.append(newLine);
    element.append(row);
    element.append(newLine);

}

var tries = 0
function verifyQos(response, pollInterval){
    // Check data length. Close window if ok is clicked
    tries += 1
    if (Object.keys(response['data']).length == 0 && tries == 2){
        confirm('An Error Occured or Qos Isnt Assigned')
        clearTimeout(pollInterval)
        window.close()

                }
    }

function qosCharts(interface){

// Arrays for storing chart.js charts
var chartsRate = ['0'];
var charts3 = ['0'];
var charts4 = ['0'];
var charts5 = ['0'];
var charts6 = ['0'];

// Call funtions every 12 seconds (Polling)
pollInterval = setInterval(getInterfaceQos, 12000);

function getInterfaceQos(){
    getQos(interface, function(response) {

        //Verify Qos assigment by checking data length
        verifyQos(response, pollInterval);

    for (const [key, value] of Object.entries(response['data'])){
        var element = document.getElementById("body");

        if (document.getElementById(key) == null && value.length){
            var parentHeader = document.createElement("h1");
            parentHeader.id = key;
            var parentHeaderText = document.createTextNode("Policy: " + key.split(' ')[0]);
            parentHeader.style.color = 'black';
            parentHeader.style.textAlign = 'left';
            parentHeader.append(parentHeaderText);
            element.append(parentHeader);
        }
        else if (document.getElementById(key) != null){
        }
        else{continue;}

        var iteration = 1;
        for (const [k, v] of Object.entries(value)){
             try {
                if(document.getElementById(v['parent_path'] + v['queue_name'] + 'One') == null){

                    //Call function which build HTML elements
                    buildHtml(element, v, iteration)

                    // Get elements created from last line, builds new charts
                    var ctx3 = document.getElementById(v['parent_path'] + v['queue_name'] + 'Three');
                    var myChart3 = new Chart(ctx3, {
                    type: 'bar',
                    labels: ['Bytes'],
                    options: {
                        plugins: {
                            legend: {
                                display: false,
                                    },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                          }
                        },
                    data: {
                        datasets: [{
                            data: [v['bytes']],
                            backgroundColor: [
                                'rgba(144, 198, 149, 1)',

                            ],
                            borderColor: [
                                'rgba(30, 130, 76, 1)',
                            ],
                            borderWidth: 1,
                            barThickness: 80
                        }]
                    },
                    });

                    var ctx4 = document.getElementById(v['parent_path'] + v['queue_name'] + 'Four')
                    var myChart4 = new Chart(ctx4, {
                    type: 'bar',
                    labels: ['Packets'],
                    options: {
                        plugins: {
                            legend: {
                                display: false,
                                    },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                          }
                        },
                    data: {
                        datasets: [{
                            data: [v['packets']],
                            backgroundColor: [
                                'rgba(144, 198, 149, 1)',

                            ],
                            borderColor: [
                                'rgba(30, 130, 76, 1)',
                            ],
                            borderWidth: 1,
                            barThickness: 80
                        }]
                    },
                    });

                    var ctx5 = document.getElementById(v['parent_path'] + v['queue_name'] + 'Five')
                    var myChart5 = new Chart(ctx5, {
                    type: 'bar',
                    options: {
                        plugins: {
                            legend: {
                                display: false,
                                    },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                          }
                        },
                    data: {
                        datasets: [{
                            label: ['Drop Pkts'],
                            data: [v['drop_packets']],
                            backgroundColor: [
                                'red'
                            ],
                            borderColor: [
                                'red'
                            ],
                            borderWidth: 1,
                            barThickness: 80
                        }]
                    },
                    });

                    var ctx6 = document.getElementById(v['parent_path'] + v['queue_name'] + 'Six')
                    var myChart6 = new Chart(ctx6, {
                    type: 'bar',
                    options: {
                        plugins: {
                            legend: {
                                display: false,
                                    },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                          }
                        },
                    data: {
                        datasets: [{
                            label: ['Drop Bytes'],
                            data: [v['drop_bytes']],
                            backgroundColor: [
                               'red'
                            ],
                            borderColor: [
                                'red'
                            ],
                            borderWidth: 1,
                            barThickness: 80
                        }]
                    },
                    });

                // If first interation create charts

                    var time = new Date()
                    var ctx1 = document.getElementById(v['parent_path'] + v['queue_name'] + 'One')
                    console.log(ctx1)
                    var myChart1 = new Chart(ctx1, {
                    type: 'line',
                    options: mbpsOptionsOutQos,
                    data: {
                    labels: [time.getSeconds()],
                    datasets: [{
                        label: 'Mbps',
                        data: [(v['bytes'] * 8 * 100) / (12 * v['speed'])],
                        fill: false,
                        tension: .5
                                }],
                                }
                            });

                    chartsRate.splice(iteration, 1, myChart1);
                    charts3.splice(iteration, 1, myChart3);
                    charts4.splice(iteration, 1, myChart4);
                    charts5.splice(iteration, 1, myChart5);
                    charts6.splice(iteration, 1, myChart6);


                    }

                    else{
                        console.log(v['bytes'])
                        // Update charts is elements exist
                        charts3[iteration].data.labels.pop();
                        charts3[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.pop();
                        });
                        charts3[iteration].update();

                        charts3[iteration].data.labels.push('Bytes');
                        charts3[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.push(v['bytes']);
                        });
                        charts3[iteration].update();

                        charts4[iteration].data.labels.pop();
                        charts4[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.pop();
                        });
                        charts4[iteration].update();

                        charts4[iteration].data.labels.push('Packets');
                        charts4[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.push(v['packets']);
                        });
                        charts4[iteration].update();

                        charts5[iteration].data.labels.pop();
                        charts5[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.pop();
                        });
                        charts5[iteration].data.labels.push('Drop Pkts');
                        charts5[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.push(v['drop_packets']);
                        });
                        charts5[iteration].update();

                        charts6[iteration].data.labels.pop();
                        charts6[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.pop();
                        });
                        charts6[iteration].data.labels.push('Drop Bytes');
                        charts6[iteration].data.datasets.forEach((dataset) => {
                            dataset.data.push(v['drop_bytes']);
                        });
                        charts6[iteration].update();

                        // For line chart it data length >= 10 pop first index, add to end. Slides the graph`
                        var time = new Date();
                        chartsRate[iteration].data.datasets.forEach((dataset) => {
                        if (dataset.data.length >= 10){
                            chartsRate[iteration].data.labels.push(time.getSeconds());
                            dataset.data.push((v['bytes'] * 8 * 100) / (12 * v['speed']));
                            chartsRate[iteration].data.labels.shift()
                            dataset.data.shift();

                            }
                            else{
                                chartsRate[iteration].data.labels.push(time.getSeconds());
                                dataset.data.push((v['bytes'] * 8 * 100) / (12 * v['speed']));
                                }

                        });

                        chartsRate[iteration].update();

                    }

                    $(".se-pre-con").fadeOut("slow");
                    iteration += 1;

            } catch (error){
            iteration += 1;
            }

        }
        }
    });
};
}
