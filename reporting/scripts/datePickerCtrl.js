(function () {
    "use strict";
    angular
        .module("myModule")
        .controller("datePickerCtrl", ["$scope", function ($scope) {

        // grab today and inject into field
        $scope.today = function () {
            $scope.dt = new Date();
        };

        // run today() function
        $scope.today();

        // open min-cal
        $scope.open = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();

            $scope.opened = true;
        };

    }]);

})();