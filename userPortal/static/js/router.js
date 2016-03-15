var routerControllers = angular.module('routerControllers', ['ui.bootstrap','ngResource']);

 routerControllers.controller('routerCtrl', ['$scope', '$log','$http', '$rootScope', function($scope, $log, $http, $rootScope) {

       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };


      $rootScope.listrouters = function() {
        $log.debug('list routers');
        var response = $http.get('/router/list_routers/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            //alert(data.networks)
            $scope.routers = data['routers'];
              $scope.totalItems = $scope.routers.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.routers.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    }

     $rootScope.listrouters();


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


// create router Ctrl
 routerControllers.controller('createRouterCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.createRouterBtn = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createrouter.html',
      controller: 'createrouterhtmlCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

routerControllers.controller('createrouterhtmlCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createrouterAction = function() {
        $log.debug('create router');
        $log.debug($scope.data);
        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('router/create_router/',{routerinfo:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
               $rootScope.listrouters();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.createRouter = function () {
    $scope.createrouterAction()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create router');
  };
});


//delete router controller
routerControllers.controller('delRouterCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deleteRouter = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/confirm_glance_delete.html',
      controller: 'deleteCtrl',
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

routerControllers.controller('deleteCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deletenetwork = function() {
        $log.debug('delete router');
        var response = $http.delete('/router/delete_router/' + $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['status'] == 'ok'){
               alert('delete Success')
               $rootScope.listrouters();
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
 routerControllers.controller('editRouterCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.editRouter = function(router) {

    $scope.data = {};
    $scope.data.id = router.id;
    $scope.data.name = router.name;
    if(router.admin_state_up)
    {
       $scope.data.state = 'UP';
    }
    else
    {
       $scope.data.state = 'DOWN';
    }


    $scope.States = [{ id: 1, name: 'UP' }, { id: 2, name: 'DOWN' }];

    $log.debug($scope.data);


    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/editrouter.html',
      controller: 'editrouterhtmlCtrl',
      css:'/static/css/createImage.css'
      //size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



routerControllers.controller('editrouterhtmlCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.update = function() {
        $log.debug('edit router');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/router/update_router/',{router:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listrouters();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.updateRouter = function () {
    $scope.update();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});


//select :  list external networkCtrl
routerControllers.controller('networkCtrl', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/router/list_extnet/');
       $rootScope.networks = []
       response.success(function (data) {
           $log.debug('get external network');
           var nets = data["networks"];
           var Num = nets.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:nets[i].id,
                   name:nets[i].name
               }
               $rootScope.networks.push(element)
           }
//           $log.debug($rootScope.networks);
       });
});


//select :  list subnet
routerControllers.controller('subnetCtrl', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/neutron/list_subnet/');
       $rootScope.subnets = []
       response.success(function (data) {
           $log.debug('get subnet ');
           var nets = data["subnets"];
           var Num = nets.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:nets[i].id,
                   name:nets[i].name
               }
               $rootScope.subnets.push(element)
           }
//           $log.debug($rootScope.networks);
       });
});



// add subnet controller
 routerControllers.controller('addInterfaceCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.addInterface = function(router) {

    $scope.data = {};
    $scope.data.id = router.id;
    $scope.data.name = router.name;
//    $scope.data.project = network.project;
//    $scope.data.state = network.admin_state_up;
//    $scope.data.tenant_id = network.tenant_id;
//    $scope.data.shared = network.shared;
    $log.debug($scope.data);

    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/addinterface.html',
      controller: 'addinterfacectrl',
      //css:'/static/css/createImage.css',
      size: 500
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



routerControllers.controller('addinterfacectrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.add = function() {
        $log.debug('add interface');
        var args = {};

        angular.copy($scope.data, args);

        $log.debug(args);

        var response = $http.post('/router/add_interface/',{interface:args});
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('Add interface  Success')
               $rootScope.listrouters();
            }
            else
                alert('Add Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('Create Failed:'+data)
            $log.debug('Create error');
        });
    }

  $scope.addInterFace = function () {
    $scope.add()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});


