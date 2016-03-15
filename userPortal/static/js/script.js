var myApp = angular.module('MyApp', ['ngRoute', 'routeStyles', 'testControllers', 'n3-pie-chart', 'cinderControllers', 'ceilControllers','glanceControllers','neutronControllers','instanceControllers','userControllers','routerControllers','projectControllers','groupControllers','lbControllers','fwControllers']);


myApp.config(function($interpolateProvider){
	 $interpolateProvider.startSymbol('[[');
	 $interpolateProvider.endSymbol(']]');

});
//置換標籤 從{{ }} 變成 [[ ]]

myApp.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});
//增加csrftoken跨站攻擊防範的token

myApp.config(['$routeProvider','$locationProvider',function($routeProvider,$locationProvider) {
    $routeProvider.
         when('/test/', {
            templateUrl : '/static/view/test.html',
            controller  : 'testCtrl',
            css: '/static/css/test.css'
        }). when('/glance/', {
            templateUrl : '/static/view/image/glance.html',
            controller  : 'glanceCtrl',
            css: '/static/css/glance_list.css'
        }).
         when('/volumes/', {
            templateUrl : '/static/view/cinder.html',
            controller  : 'cinderCtrl',
            css: '/static/css/cinder.css'
        }).
        when('/volumes/?tab=snapshots_tab/', {
            templateUrl : '/static/view/snapshots_tab.html',
            controller  : 'snapshotsCtrl',
            css: '/static/css/snapshots.css'
        }).
        when('/ceilometer/', {
            templateUrl : '/static/view/ceilometer.html',
            controller : 'ceilometerCtrl',
            css: '/static/css/ceilometer.css'
        }).
        when('/listTest/', {
            templateUrl : '/static/view/userlist_test.html',
            css: '/static/css/userlist_test.css'
        })
        .when(
            '/neutron/', {
            templateUrl : '/static/view/network/neutron.html',
            controller  : 'neutronCtrl',
            css: '/static/css/userlist_test.css'
        })
        .when(
            '/router/', {
            templateUrl : '/static/view/network/router.html',
            controller  : 'routerCtrl',
            css: '/static/css/userlist_test.css'
        })
        .when(
            '/securitygroup/', {
            templateUrl : '/static/view/network/securitygroup.html',
            controller  : 'groupCtrl',
            css: '/static/css/userlist_test.css'
        })
        .when(
            '/loadbalancer/', {
            templateUrl : '/static/view/network/lb.html',
            controller  : 'lbCtrl',
            css: '/static/css/userlist_test.css'
        })
        .when(
            '/firewall/', {
            templateUrl : '/static/view/network/firewall.html',
            controller  : 'fwCtrl',
            css: '/static/css/userlist_test.css'
        })
        .when(
            '/instance/', {
            templateUrl : '/static/view/instance/instance.html',
            controller  : 'instanceCtrl',
            css: '/static/css/instance_list.css'
        }).when(
            '/user/', {
            templateUrl : '/static/view/user/user.html',
            controller  : 'userCtrl',
            css: '/static/css/user_list.css'
        }).when(
            '/project/', {
            templateUrl : '/static/view/project/project.html',
            controller  : 'projectCtrl',
            css: '/static/css/project_list.css'
        })
          .otherwise({
             redirectTo: '/'
        });
        // use the HTML5 History API
        $locationProvider.html5Mode(true);

  }]);

myApp.controller('myCtrl', ['$scope', '$log','$http', '$location', function($scope, $log, $http, $location) {
        //以後這個script檔不會有controller，全部都用import的
    $scope.logout = function() {
        var response = $http.get('/logout/');
        response.success(function(data, status, headers, config) {
            $log.debug('logout success');
        });
        response.error(function(data, status, headers, config) {
        });
    };
}]);

