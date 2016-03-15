 var testControllers = angular.module('testControllers', []);

 testControllers.controller('testCtrl', ['$scope', '$log','$http', '$location', function($scope, $log, $http, $location) {
    
    //For pie-chart
    $scope.options = {thickness: 20};
    $scope.data = [
        {label: "one", value: 12.2, color: "red"}, 
        {label: "two", value: 45, color: "#00ff00"},
        {label: "three", value: 10, color: "rgb(0, 0, 255)"}
    ];

    $scope.firstName = "John";
    $scope.lastName = "Doe";
    $scope.doGet = function() {
        $log.debug('doneGet');
        var response = $http.get('/doHttpRequest/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            $scope.getValue = data;
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    }
    $scope.doPost = function() {
        $log.debug('donePost');
        var response = $http.post('/doHttpRequest/');
        response.success(function(data, status, headers, config) {
            $log.debug('post success');
            $scope.postValue = data;
        });
        response.error(function(data, status, headers, config) {
            $log.debug('post error');
        });
    }
    $scope.getToken = function() {
        $log.debug('getToken');
        var response = $http.get('/getToken/');
        response.success(function(data, status, headers, config) {
            $log.debug('getToken success');
            $log.debug("-----------data-----------");
            $log.debug(data);
            $scope.token = data['token'];
            $scope.tokenStatus = data['tokenStatus'];
        });
        response.error(function(data, status, headers, config) {
            $log.debug('getToken error');
        });
    }
}]);