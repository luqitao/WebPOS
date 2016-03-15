var ceilometerControllers = angular.module('ceilControllers', ['ngTable', 'ui.bootstrap', 'ngResource']);

ceilometerControllers.controller('ceilometerCtrl', ['$scope', '$log','$http', '$location', 'ngTableParams', '$uibModal', function($scope, $log, $http, $location, ngTableParams, $uibModal) {

    var formatDate = function (time) {           // change the formate of date into yyyy-mm-dd
     if(typeof time == 'string'){
         return time
     }
     else{
         var y = time.getFullYear();
         var m = time.getMonth() + 1;
         m = m < 10 ? '0' + m : m;
         var d = time.getDate();
         d = d < 10 ? ('0' + d) : d;
         return y + '-' + m + '-' + d;
     }
    };
    //
     $scope.init_date = function() {
         $scope.dt_from = formatDate(new Date());
         $scope.dt_to = formatDate(new Date());
         $scope.today = formatDate(new Date());
     };
     $scope.init_date();

    $scope.toggleMin = function() {
        $scope.minDate = $scope.minDate ? null : new Date();
    };
    $scope.toggleMin();
    $scope.maxDate = new Date(2020, 5, 22);

    $scope.open_from = function($event) {
        $scope.status.from = true;
    };

     $scope.open_to = function($event) {
        $scope.status.to = true;
    };

    $scope.status = {
        from: false,
        to: false
    };

    $scope.sort = function(keyname){
        $scope.sortKey = keyname;   //set the sortKey to the param passed
        $scope.reverse = !$scope.reverse; //if true make it false and vice versa
    };

     $scope.listinfo = function(callback) {
            $log.debug('Get meters information');
            var response = $http.get('/get_ceilometer/information/');
            response.success(function(data, status, headers, config) {
                $log.debug('list meters success');
                $log.debug(data);
                callback(data);
            });
            response.error(function(data, status, headers, config) {
            });
        };
    $scope.getinformation = function(){
        $scope.listinfo(function(data) {
            $scope.meterstableParams = new ngTableParams({
                page: 1,            // show first page
                count: 10           // count per page
                }, {
                    total: data.length, // length of data
                    getData: function($defer,params) {
                        $scope.page = params.page();
                        $scope.size = params.count();
                        $defer.resolve(data.slice((params.page() - 1) * params.count(),params.page() * params.count()));
                    }
            });
        });
    };
    $scope.getinformation();

     // Alarms

    $scope.getAlarms = function(callback) {
         var url = '/get_ceilometer/list_alarms/';
         var response = $http.get(url);
         response.success(function(data, status, headers, config) {
             $log.debug('get meters data success');
             $log.debug("-----------meters data-----------");
             //$log.debug(data);
             //$scope.data_total = data;
             callback(data)
         });
         response.error(function(data, status, headers, config) {
            $log.debug("get meters data error")
         });
    };

    $scope.Alarms = function () {
        $scope.getAlarms(function(data) {
            $scope.AlarmstableParams = new ngTableParams({
                page: 1,            // show first page
                count: 5            // count per page
                }, {
                    total: data.length, // length of data
                    getData: function($defer,params) {
                        $log.debug('Get Alarms ...');
                        $log.debug(params.page());
                        $log.debug(params.count());
                        $scope.page = params.page();
                        $scope.size = params.count();
                        $defer.resolve(data.slice((params.page() - 1) * params.count(),params.page() * params.count()));
                    }
            });
        });
    };
    $scope.Alarms();

    $scope.createAlarm = function () {
        var createAlarm = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/ceilometer/create_alarm.html',
            controller: 'createAlarmCtrl'
            //css: '/static/css/test.css'
        });
    };
}]);

ceilometerControllers.controller('createAlarmCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createAlarmClicked = function() {
        $log.debug('Create Alarm');
        var response = $http.post('/createAlarm/');
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success');
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data);
            $log.debug('get error');
        });
    };

  $scope.createAlarm = function () {
      $scope.createAlarmClicked();
      $uibModalInstance.close();
  };


  $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
  };
});

