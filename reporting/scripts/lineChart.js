(function () {
    "use strict";
    angular
        .module("myModule")
        .directive('hcChart', function () { // Directive for generic chart, pass in chart options
            return {
                restrict: 'E',
                template: '<div></div>',
                scope: {
                    options: '='
                },
                link: function (scope, element, attrs) {
                    Highcharts.chart(element[0], scope.options);
                    scope.$watch(attrs.watch, function (newVal) {
                        if (newVal) {
                            var complete = function (options) {
                                var chart = $(element[0]).highcharts();
                                // capture all available series
                                var allSeries = chart.series;
                                for (var i = 0; i < allSeries.length; i++) {
                                    allSeries[i].setData(options.series[i].data, false);
                                }

                                chart.redraw();
                            };

                            // doesn't work without the timeout 
                            $timeout(function () {
                                Highcharts.data({
                                    table: config.data.table,
                                    complete: complete
                                });
                            }, 0);
                        }
                    });
                }
            };
        })
})();