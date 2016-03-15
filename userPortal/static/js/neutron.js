var neutronControllers = angular.module('neutronControllers', ['ui.bootstrap','ngResource']);

 neutronControllers.controller('neutronCtrl', ['$scope', '$log','$http', '$rootScope', function($scope, $log, $http, $rootScope) {

       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };


      $rootScope.listNetwork = function() {
        $log.debug('list network');
        var response = $http.get('/neutron/list_networks/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            //alert(data.networks)
            $scope.networks = data['networks'];
              $scope.totalItems = $scope.networks.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.networks.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    }

     $rootScope.listNetwork();


    $rootScope.selected = [];
    $rootScope.selectedTags = [];

    var updateSelected = function(action,id,name){
        if(action == 'add' && $rootScope.selected.indexOf(id) == -1){
            $scope.selected.push(id);
            $scope.selectedTags.push(name);
        }

        if(action == 'remove' && $rootScope.selected.indexOf(id)!=-1){
            var idx = $rootScope.selected.indexOf(id);
            $scope.selected.splice(idx,1);
            $scope.selectedTags.splice(idx,1);
        }
        $log.debug($rootScope.selected)
    }

    $rootScope.updateSelection = function($event, id){
        var checkbox = $event.target;
        var action = (checkbox.checked?'add':'remove');
        updateSelected(action,id,checkbox.name);
    }

    $rootScope.isSelected = function(id){
        return $rootScope.selected.indexOf(id)>=0;
    }
}]);


//create network controller
 neutronControllers.controller('createNWCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.createNW = function (size) {

    $scope.data = {};

    $scope.States = [{ id: 1, name: 'UP' }, { id: 2, name: 'DOWN' }];
    $scope.data.state =  $scope.States[0];

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createnetwork.html',
      controller: 'createnetworkCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

neutronControllers.controller('createnetworkCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {


    $scope.iniproject = function() {

        var response = $http.get('/neutron/list_project/');
        $rootScope.projects = []
           response.success(function (data) {
               $log.debug('get projectCtrl');
               var projectNum = data.length;
               for(var i = 0;i<projectNum;i++){
                   var element ={
                       id:data[i].id,
                       name:data[i].name
                   }
                   $rootScope.projects.push(element)
               }
               $log.debug($rootScope.projects);
           });
    };

     $scope.iniproject();

    $scope.createnetwork = function() {

        $log.debug('create network');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/neutron/create_network/',{network:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
               $rootScope.listNetwork();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('create error');
        });
    }

  $scope.createNW = function () {
    $scope.createnetwork()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create network');
  };
});


//delete network controller
neutronControllers.controller('deleteNWCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deleteNW = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/confirm_glance_delete.html',
      controller: 'deletenetworkCtrl',
      size: size
    });

    //modalInstance.result.then(function (selectedItem) {
    //
    //}, function () {
    //  $log.info('Modal dismissed at: ' + new Date());
    //});
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

neutronControllers.controller('deletenetworkCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deletenetwork = function() {
        $log.debug('delete network');
        var response = $http.delete('/neutron/delete_networks/' + $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['status'] == 'ok'){
               alert('delete Success')
               $rootScope.listNetwork();
            }
            else
                alert('delete Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('delete Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.ok = function () {
      $scope.deletenetwork()
      $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});


// edit network controller
 neutronControllers.controller('editNWorkCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.editNW = function(network) {
    $scope.data = {};
    $scope.data.id = network.id;
    $scope.data.name = network.name;

    if(network.admin_state_up)
    {
       $scope.data.state = 'UP';
    }
    else
    {
       $scope.data.state = 'DOWN';
    }


    $scope.States = [{ id: 1, name: 'UP' }, { id: 2, name: 'DOWN' }];

    var modalInstance = $uibModal.open({
      scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/editnetwork.html',
      controller: 'editnetworkCtrl',
      css:'/static/css/createImage.css'
      //size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



neutronControllers.controller('editnetworkCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.editnetwork = function() {
        $log.debug('edit network');
//        $scope.data.state="test"
        var args = {};


        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/neutron/update_network/',{network:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listNetwork();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.createNW = function () {
    $scope.editnetwork();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});


//select :  list projects
neutronControllers.controller('projectCtrl', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/neutron/list_project/');
    $rootScope.projects = []
       response.success(function (data) {
           $log.debug('get projectCtrl');
           var projectNum = data.length;
//           alert(projectNum);
           for(var i = 0;i<projectNum;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $rootScope.projects.push(element)
           }
           $log.debug($rootScope.projects);
       });
});



// add subnet controller
 neutronControllers.controller('addSubCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.addSubnet = function(network) {

//    $scope.subnet.enable_dhcp = 'YES';
//    $scope.Dhcps = [{id:1,name:'YES'},{id:2,name:'NO'}];

    $scope.data = {};
    $scope.data.id = network.id;
    $scope.data.name = network.name;
    $scope.data.tenant_id = network.tenant_id;

    $log.debug($scope.data);

    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createsubnet.html',
      controller: 'addSubnetCtrl'
      //css:'/static/css/createImage.css',
//      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



neutronControllers.controller('addSubnetCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.createsubnet = function() {
        $log.debug('create subnet');
//        $scope.data.state="test"
        var args1 = {};
        var args2 = {};
        var args = {};


//        if($scope.data.project==undefined){
//            alert('tcx')
//            $scope.data.project="test"
//        }
//
//        if($scope.data.state==undefined){
//            $scope.data.state="Up"
//        }
//
//        if($scope.data.shared==undefined){
//            $scope.data.state="YES"
//        }

        angular.copy($scope.data, args1);
        angular.copy($scope.subnet, args2);
//        args = args1 + args2;

        $log.debug(args2);

        var response = $http.post('/neutron/create_subnet/',{network:args1,subnet:args2});
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('Create Subnet  Success')
               $rootScope.listNetwork();
            }
            else
                alert('Create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('Create Failed:'+data)
            $log.debug('Create error');
        });
    }

  $scope.createSub = function () {
    $scope.createsubnet()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});