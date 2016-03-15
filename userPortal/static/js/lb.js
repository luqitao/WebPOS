var lbControllers = angular.module('lbControllers', ['ui.bootstrap','ngResource','ng.bs.dropdown']);

//Loadbalancer dropDown action
lbControllers.controller("lbActionController", function($scope,$http,$log,$rootScope,$uibModal){
        $scope.action = [
            "Edit Pool",
            "Associate Monitor",
            "Disassociate Monitor",
        ];

        $scope.selectAction = "Edit ";  //current select item

        $scope.changeAction = function(pool){

        if($scope.selectAction=="Edit Pool")
        {
           $log.debug(pool);

           $scope.data = {};
           $scope.data.id = pool.id;
           $scope.data.name = pool.name;
           $scope.data.description = pool.description;

           $rootScope.admin_state_up = pool.admin_state_up;
           $rootScope.method = pool.lb_method;


           var modalInstance = $uibModal.open({
           scope: $scope,
           animation: $scope.animationsEnabled,
           templateUrl: '/static/view/network/editlbpool.html',
           controller: 'editlbpoolCtrl',
           size: 500
          });

        }
        else if($scope.selectAction=="Associate Monitor")
        {
           $scope.data = {};
           $scope.data.id = pool.id;
           $scope.data.name = pool.name;
           $scope.data.health_monitors = pool.health_monitors

           var modalInstance = $uibModal.open({
           scope: $scope,
           animation: $scope.animationsEnabled,
           templateUrl: '/static/view/network/associatemonitor.html',
           controller: 'associatemonitorCtrl',
           size: 500
          });
        }
        else
        {
           $scope.data = {};
           $scope.data.id = pool.id;
           $scope.data.name = pool.name;
           $scope.data.health_monitors = pool.health_monitors

           var modalInstance = $uibModal.open({
           scope: $scope,
           animation: $scope.animationsEnabled,
           templateUrl: '/static/view/network/disassociatemonitor.html',
           controller: 'disassociatemonitorCtrl',
           size: 500
          });
        }
        }
    });

lbControllers.controller('associatemonitorCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.iniMonitor = function () {
       var response = $http.get('/loadbalancer/list_monitor/');
       $rootScope.monitors = []
       response.success(function (data) {
           $log.debug('get monitors ');
           var allmonitor = data["health_monitors"];
           var ownmonitor = $scope.data.health_monitors;
           $log.debug(ownmonitor);
           var wonNum = ownmonitor.length;
           var Num = allmonitor.length;
           for(var i = 0;i<Num;i++){
           var flag = true;
              for(var j = 0;j<wonNum;j++){
                  if(allmonitor[i].id == ownmonitor[j]){
                     flag = false;
                     break;
                  }
              }

              if(flag){
                var element ={
                               id:allmonitor[i].id,
                               name: 'ping Delay:'+ allmonitor[i].delay + " retries:" + allmonitor[i].max_retries + " timeout:" + allmonitor[i].timeout
                             }
                $rootScope.monitors.push(element)
              }
           }
//           $log.debug($rootScope.monitors);
       });
    }

    $scope.iniMonitor();

    $scope.associateMonitorAction = function() {
        $log.debug('associate monitor to lb');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/loadbalancer/associate_monitor/',{pool:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listpools();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.associateMonitor = function () {
    $scope.associateMonitorAction();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});

lbControllers.controller('disassociatemonitorCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.iniMonitor = function () {
       var response = $http.get('/loadbalancer/list_monitor/');
       $rootScope.monitors = []
       response.success(function (data) {
           $log.debug('get monitors ');
           var allmonitor = data["health_monitors"];
           var ownmonitor = $scope.data.health_monitors;
           $log.debug(ownmonitor);
           var wonNum = ownmonitor.length;
           var Num = allmonitor.length;
           for(var i = 0;i<Num;i++){
           var flag = false;
              for(var j = 0;j<wonNum;j++){
                  if(allmonitor[i].id == ownmonitor[j]){
                     flag = true;
                     break;
                  }
              }

              if(flag){
                var element ={
                               id:allmonitor[i].id,
                               name: 'ping Delay:'+ allmonitor[i].delay + " retries:" + allmonitor[i].max_retries + " timeout:" + allmonitor[i].timeout
                             }
                $rootScope.monitors.push(element)
              }
           }
//           $log.debug($rootScope.monitors);
       });
    }

    $scope.iniMonitor();

    $scope.disassociateMonitorAction = function() {
        $log.debug('associate monitor to lb');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.delete('/loadbalancer/disassociate_monitor/' + $scope.data.id + '&&' + $scope.data.monitor);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['status'] == 'ok'){
               alert('delete Success')
               $rootScope.listpools();
            }
            else
                alert('delete Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('delete Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.disassociateMonitor = function () {
    $scope.disassociateMonitorAction();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});

lbControllers.controller('lbCtrl', ['$scope', '$log','$http', '$rootScope', function($scope, $log, $http, $rootScope) {

       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };


      $rootScope.listpools = function() {
        $log.debug('list pools');
        var response = $http.get('/loadbalancer/list_pools/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            //alert(data.networks)
            $scope.pools = data['pools'];
              $scope.totalItems = $scope.pools.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.pools.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    }

     $rootScope.listpools();


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

// create loadbalancer pool Ctrl
lbControllers.controller('createpoolCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.addPool = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/addlbpool.html',
      controller: 'createpoolhtmlCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

lbControllers.controller('createpoolhtmlCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.addPoolAction = function() {
        $log.debug('create lb pool');
        $log.debug($scope.data);

        if($scope.data.admin_state_up == 'UP' ){
            $scope.data.admin_state_up="True";
        }else
        {
            $scope.data.admin_state_up="False";
        }

        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('loadbalancer/add_lbpool/',{info:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
               $rootScope.listpools();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    }

    $scope.iniSubnet = function () {
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
       });
    }
    $scope.iniSubnet();

  $scope.addPool = function () {
    $scope.addPoolAction()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create router');
  };
});

//delete loadbalancer pool
lbControllers.controller('delpoolCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deletePool = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/confirm_glance_delete.html',
      controller: 'deletePoolActionCtrl',
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

lbControllers.controller('deletePoolActionCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deletepool = function() {
        $log.debug('delete lb pool');
        var response = $http.delete('/loadbalancer/delete_lbpool/' + $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['status'] == 'ok'){
               alert('delete Success')
               $rootScope.listpools();
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
      $scope.deletepool()
      $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

// edit pool controller
lbControllers.controller('editlbpoolCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
  $scope.animationsEnabled = true;

  $scope.iniDropdown = function() {

       if($rootScope.admin_state_up)
         {
           $scope.data.state = 'UP';
         }
        else
         {
           $scope.data.state = 'DOWN';
         }


         $scope.States = [{ id: 1, name: 'UP' }, { id: 2, name: 'DOWN' }];


         $scope.data.method = $rootScope.method;
         $scope.Methods = [{ id: 1, name: 'ROUND_ROBIN' }, { id: 2, name: 'LEAST_CONNECTIONS' }, { id: 3, name: 'SOURCE_IP' }];


  }

  $scope.iniDropdown();

  $scope.editlbPool = function() {
        $log.debug('edit pool');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/loadbalancer/edit_lbpool/',{pool:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listpools();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.updatelbPool = function () {
    $scope.editlbPool()
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create router');
  };
});

// add monitor Ctrl
lbControllers.controller('addMonitorBtnCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.addMonitorBtn = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/addmonitor.html',
      controller: 'addmonitorCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

lbControllers.controller('addmonitorCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.addMonitorAction = function() {
        $log.debug('add monitor');
        $log.debug($scope.data);

        if($scope.data.admin_state_up == 'UP' ){
            $scope.data.admin_state_up="True";
        }else
        {
            $scope.data.admin_state_up="False";
        }

        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('/loadbalancer/add_monitor/',{info:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.addMonitor = function () {
    $scope.addMonitorAction()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create pool');
  };
});


// add monitor Ctrl
lbControllers.controller('addLbMemberBtnCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.addLbMemberBtn = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/addlbmember.html',
      controller: 'addlbmemberCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

lbControllers.controller('addlbmemberCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.iniMember = function () {
       var response = $http.get('/listInstance/');
       $rootScope.Members = []
       response.success(function (data) {
           $log.debug('get instances ');
           $log.debug(data);
           var instances = data;
           var Num = instances.length;
           for(var i = 0;i<Num;i++){

              if(instances[i].addresses.length != 0)
              {
                  var temp = instances[i].addresses;
                  var tmpid = temp.substring(0,temp.length - 1)
                  var element ={
                               id:tmpid,
                               name: instances[i].name +':'+ tmpid
                           }
                  $rootScope.Members.push(element);

              }
           }
       });
    }

    $scope.iniPool = function () {
       var response = $http.get('/loadbalancer/list_pools/');
       $rootScope.Pools = []
       response.success(function (data) {
           $log.debug('get pools ');
           $log.debug(data);
           var pools = data['pools'];
           var Num = pools.length;
           for(var i = 0;i<Num;i++){

                  var element ={
                               id:pools[i].id,
                               name: pools[i].name
                           }
                  $rootScope.Pools.push(element);
           }
       });
    }

    $scope.iniMember();
    $scope.iniPool();

    $scope.addMemberAction = function() {
        $log.debug('add monitor');
        $log.debug($scope.data);

        if($scope.data.admin_state_up == 'UP' ){
            $scope.data.admin_state_up="True";
        }else
        {
            $scope.data.admin_state_up="False";
        }

        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('/loadbalancer/add_member/',{info:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
               $rootScope.listpools();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.addMember = function () {
    $scope.addMemberAction()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create pool');
  };
});
