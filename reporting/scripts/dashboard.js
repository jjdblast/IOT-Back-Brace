(function () {
    "use strict";
    angular
            .module('myModule', ["highcharts-ng"])
            .controller('myController', dashboardController)
            .filter('percentage', function() {
                return function(input) {
                    if (isNaN(input)) {
                        return input;
                    }
                    return Math.floor((input * 100)) + '%';
                }
            })

    function dashboardController($scope, $http) {  

        var vm = this;
        vm.today = today;
        vm.openDatePicker = openDatePicker;
        vm.readingsSeries = [];
        vm.refresh = refresh;
        vm.selectedDevice = {
            deviceID: "0",
            assignedTo: "All Devices"
        }
        vm.pieData = [
  {
      "name": "Stooping",
      "y": 0.03
  },
  {
      "name": "Bending",
      "y": 0.08
  },
  {
      "name": "Upright",
      "y": 0.89
  }
  ];



        // Get Facilities
        $http({
            method: 'GET',
            url: "http://sandbox.mycontraption.com/iotbb/api/?action=facilities",
            headers: { "Accept": "application/json;" }
        }).then(function (response) {
            vm.facilities = response.data;
            vm.selectedFacility = vm.facilities[0];
        });

        function today() {
            vm.dt = new Date();
        }

        function openDatePicker() {
            vm.datePicker.opened = true;
        };

        // Get Available Dates
        $http({
            method: 'GET',
            url: "http://sandbox.mycontraption.com/iotbb/api/?action=availableDates",
            headers: { "Accept": "application/json;" }
        }).then(function (response) {
            vm.availableDates = response.data;
            vm.selectedDate = vm.availableDates[0];
            refresh();
        });

        // Get Readings Detail
        $http({
            method: 'GET',
            url: "http://sandbox.mycontraption.com/iotbb/api/?action=readingsDetail",
            headers: { "Accept": "application/json;" }
        }).then(function (response) {
            vm.readingsDetail = response.data;
            // populate our series for charting
            for (var i = 0; i < vm.readingsDetail.length; i++) {
                vm.readingsSeries.push(vm.readingsDetail[i].actualPitch);
                vm.bandedChartOptions.series.push({
                    data: vm.readingsDetail[i].actualPitch
                })
            }
            //chart.series[0].setData(vm.readingSerices);

        });



        today();

        function refresh() {
            getSummaryData();

        }



        function getSummaryData() {
            // Get Summary Data
            var readingDate = vm.selectedDate.readingDate;
            var selectedFacility = vm.selectedFacility.facilityID;
            var selectedDevice = vm.selectedDevice.deviceID;
            console.log("http://sandbox.mycontraption.com/iotbb/api/?action=summaryData&readingDate=" + readingDate + "&selectedFacility=" + selectedFacility + "&selectedDevice=" + selectedDevice);
            $http({
                method: 'GET',
                url: "http://sandbox.mycontraption.com/iotbb/api/?action=summaryData&readingDate=" + readingDate + "&selectedFacility=" + selectedFacility + "&selectedDevice=" + selectedDevice,
                headers: { "Accept": "application/json;" }
            }).then(function (response) {
                vm.summaryData = response.data;

            });
        }

        

        vm.deviceReadingsTrend = [
  -11.4,
  -13.4,
  -45,
  -54.3,
  -51.4,
  -51,
  -51.3,
  -48.8,
  -61.4,
  -65.5,
  -58.4,
  -58,
  40.3,
  45.2,
  43.3,
  -61,
  -60.9,
  -11.4,
  48.8,
  43.5,
  46.9,
  47.6,
  42.1,
  46.2,
  47.6,
  44.5,
  31.7,
  24.4,
  20.5,
  21.9,
  19,
  18.9,
  18.8,
  32.3,
  30.9,
  4,
  -10.5,
  -2.8,
  18.8,
  6.3,
  12.9,
  13.3,
  13.9,
  16.9,
  16.9,
  16.9,
  13.7,
  7.3,
  0.1,
  -2.1,
  9.5,
  37.8
        ];

        // Simple Chart
        vm.chartOptions = {
            title: {
                text: 'Posture Trend'
            },
            /*xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },*/

            series: [{
                data: vm.deviceReadingsTrend
            }]
        };

        
        // Banded Spline Chart
        vm.bandedChartOptions = {
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Posture Trend'
            },
            xAxis: {
                type: 'datetime',
                labels: {
                    overflow: 'justify'
                }
            },
            yAxis: {
                title: {
                    text: 'Degree of Posture Change'
                },
                minorGridLineWidth: 0,
                gridLineWidth: 0,
                alternateGridColor: null,
                plotBands: [{ // stooping
                    from: 0.3,
                    to: 1.5,
                    color: 'rgba(68, 170, 213, 0.1)',
                    label: {
                        text: 'Stooping',
                        style: {
                            color: '#606060'
                        }
                    }
                }, { // Bending
                    from: 1.5,
                    to: 3.3,
                    color: 'rgba(0, 0, 0, 0)',
                    label: {
                        text: 'Bending',
                        style: {
                            color: '#606060'
                        }
                    }
                }, { // Upright
                    from: 3.3,
                    to: 5.5,
                    color: 'rgba(68, 170, 213, 0.1)',
                    label: {
                        text: 'Upright',
                        style: {
                            color: '#606060'
                        }
                    }
                }]
            },
            tooltip: {
                valueSuffix: ' m/s'
            },
            plotOptions: {
                spline: {
                    lineWidth: 4,
                    states: {
                        hover: {
                            lineWidth: 5
                        }
                    },
                    marker: {
                        enabled: false
                    },
                    pointInterval: 3600000, // one hour
                    pointStart: Date.UTC(2015, 4, 31, 0, 0, 0)
                }
            },
            series: [{
                name: 'Device ac423eb65d4a32',
                data: vm.deviceReadingsTrend

            }],
            navigation: {
                menuItemStyle: {
                    fontSize: '10px'
                }
            }
        };

        

        // Sample data for pie chart
        vm.pieOptions = {
            "options": {
                "chart": {
                    "type": "pie"
                }
            },
            "series": [{
                data: vm.pieData
            }],
            "title": {
                "text": "Posture Summary"
            },
            "credits": {
                "enabled": true
            },
            "loading": false,
            "size": {}
        };

        


    };
})();
