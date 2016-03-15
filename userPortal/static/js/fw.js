var fwControllers = angular.module('fwControllers', ['ui.bootstrap','ngResource','ng.bs.dropdown']);

 //FireWall dropDown action
fwControllers.controller("firewallActionController", function($scope,$http,$log,$rootScope,$uibModal){
        $scope.action = [
            "Edit Firewall",
            "Add Router",
            "Remove Router",
        ];

        $scope.selectAction = "Edit Firewall";  //current select item

        $scope.changeAction = function(fw){

        if($scope.selectAction=="Edit Firewall")
        {
           $log.debug(fw);

           $scope.data = {};
           $scope.data.id = fw.id;
           $scope.data.name = fw.name;
           $scope.data.description = fw.description;
           $rootScope.firewall_policy_id = fw.firewall_policy_id;


           if(fw.admin_state_up)
            {
                $scope.data.state = 'UP';
            }
           else
            {
                $scope.data.state = 'DOWN';
            }


            $scope.States = [{ id: 1, name: 'UP' }, { id: 2, name: 'DOWN' }];

            $log.debug($scope.data);

           var modalInstance = $uibModal.open({
           scope: $scope,
           animation: $scope.animationsEnabled,
           templateUrl: '/static/view/network/editfw.html',
           controller: 'editfwCtrl',
           size: 500
          });
        }
        else if($scope.selectAction=="Add Router")
        {
           $scope.data = {};
           $scope.data.id = fw.id;
           $scope.data.name = fw.name;
           $scope.data.router_ids = fw.router_ids

           var modalInstance = $uibModal.open({
           scope: $scope,
           animation: $scope.animationsEnabled,
           templateUrl: '/static/view/network/addrouter.html',
           controller: 'addrouterCtrl',
           size: 500
          });
        }
        else
        {
           $scope.data = {};
           $scope.data.id = fw.id;
           $scope.data.name = fw.name;
           $scope.data.router_ids = fw.router_ids

           var modalInstance = $uibModal.open({
           scope: $scope,
           animation: $scope.animationsEnabled,
           templateUrl: '/static/view/network/removerouter.html',
           controller: 'removerouterCtrl',
           size: 500
          });
        }
        }
    });


 fwControllers.controller('fwCtrl', ['$scope', '$log','$http', '$rootScope', function($scope, $log, $http, $rootScope) {

       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };


      $rootScope.listfws = function() {
        $log.debug('list routers');
        var response = $http.get('/firewall/list_firewall/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            //alert(data.networks)
            $scope.fws = data['firewalls'];
              $scope.totalItems = $scope.fws.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.fws.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    }

     $rootScope.listfws();


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


// create fw Ctrl
 fwControllers.controller('createFwCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.createFw = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createfw.html',
      controller: 'createCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

fwControllers.controller('createCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.create = function() {
        $log.debug('create firewall');
        $log.debug($scope.data);
        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('/firewall/create_firewall/',{fwinfo:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
               $rootScope.listfws();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    }

    $scope.iniPolicy = function () {
        var response = $http.get('/firewall/list_policy/');
       $rootScope.policys = []
       response.success(function (data) {
           $log.debug('get policy ');
           var policys = data["firewall_policies"];
           var Num = policys.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:policys[i].id,
                   name:policys[i].name
               }
               $rootScope.policys.push(element)
           }
//           $log.debug($rootScope.networks);
       });
    };


    $scope.iniRouter = function () {
        var response = $http.get('/router/list_routers/');
       $rootScope.routers = []
       response.success(function (data) {
           $log.debug('get routers ');
           var routers = data["routers"];
           var Num = routers.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:routers[i].id,
                   name:routers[i].name
               }
               $rootScope.routers.push(element)
           }
//           $log.debug($rootScope.networks);
       });
    }


    $scope.iniPolicy();
    $scope.iniRouter();

  $scope.createFirewall = function () {
    $scope.create()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create router');
  };
});


//delete fw controller
fwControllers.controller('delFwCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deleteFw = function (size) {

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

fwControllers.controller('deleteCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deletefirewall = function() {
        $log.debug('delete firewall');
        var response = $http.delete('/firewall/delete_firewall/' + $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['status'] == 'ok'){
               alert('delete Success')
               $rootScope.listfws();
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
      $scope.deletefirewall()
      $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

// add polciy Ctrl
 fwControllers.controller('addPolicyBtnCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.addPolicyBtn = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/addpolicy.html',
      controller: 'addpolicyCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

fwControllers.controller('addpolicyCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.add = function() {
        $log.debug('add policy');
        $log.debug($scope.data);
        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('/firewall/add_policy/',{info:args } );
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


    $scope.iniRule = function () {
        var response = $http.get('/firewall/list_rule/');
       $rootScope.rules = []
       response.success(function (data) {
           $log.debug('get rules ');
           var rules = data["firewall_rules"];
           var Num = rules.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:rules[i].id,
                   name:rules[i].name
               }
               $rootScope.rules.push(element)
           }
       });
    }

    $scope.iniRule();

  $scope.addPolicy = function () {
    $scope.add()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create router');
  };
});


// add rule Ctrl
 fwControllers.controller('addRuleBtnCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.addRuleBtn = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/addrule.html',
      controller: 'addruleCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});


fwControllers.controller('addruleCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.add = function() {
        $log.debug('add rule');
        $log.debug($scope.data);

        if($scope.data.shared==undefined || !$scope.data.shared){
            $scope.data.shared="False";
        }else
        {
            $scope.data.shared="True";
        }

        if($scope.data.enabled==undefined || !$scope.data.enabled){
            $scope.data.enabled="False";
        }else
        {
            $scope.data.enabled="True";
        }

        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('/firewall/add_fwrule/',{info:args } );
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

  $scope.addRule = function () {
    $scope.add()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create router');
  };
});


fwControllers.controller('editfwCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.iniPolicy = function () {
        var response = $http.get('/firewall/list_policy/');
       $rootScope.policys = []
       response.success(function (data) {
           $log.debug('get policy ');
           var policys = data["firewall_policies"];
           var Num = policys.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:policys[i].id,
                   name:policys[i].name
               }
               $rootScope.policys.push(element)
           }
       });
    };

    $scope.iniPolicy();

    $scope.update = function() {
        $log.debug('edit firewall');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/firewall/update_firewall/',{firewall:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listfws();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.updateFirewall = function () {
    $scope.update();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});


fwControllers.controller('addrouterCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.iniRouter = function () {
       var response = $http.get('/router/list_routers/');
       $rootScope.routers = []
       response.success(function (data) {
           $log.debug('get routers ');
           var routers = data["routers"];
           var routeradded = $scope.data.router_ids;
           var Numadded = routeradded.length;
           var Num = routers.length;
           for(var i = 0;i<Num;i++){
           var flag = true;
              for(var j = 0;j<Numadded;j++){
                  if(routers[i].id == routeradded[j]){
                     flag = false;
                     break;
                  }
              }

              if(flag){
                var element ={
                               id:routers[i].id,
                               name:routers[i].name
                             }
                $rootScope.routers.push(element)
              }
           }
//           $log.debug($rootScope.networks);
       });
    }

    $scope.iniRouter();

    $scope.add = function() {
        $log.debug('add router to firewall');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/firewall/add_router_to_fw/',{firewall:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listfws();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.addRouter = function () {
    $scope.add();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});


fwControllers.controller('removerouterCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.iniRouter = function () {
       var response = $http.get('/router/list_routers/');
       $rootScope.routers = []
       response.success(function (data) {
           $log.debug('get routers ');
           var routers = data["routers"];
           var routerremove = $scope.data.router_ids;
           var Numremove = routerremove.length;
           var Num = routers.length;
           for(var i = 0;i<Num;i++){
           var flag = false;
              for(var j = 0;j<Numremove;j++){
                  if(routers[i].id == routerremove[j]){
                     flag = true;
                     break;
                  }
              }

              if(flag){
                var element ={
                               id:routers[i].id,
                               name:routers[i].name
                             }
                $rootScope.routers.push(element)
              }
           }
       });
    }

    $scope.iniRouter();

    $scope.remove = function() {
        $log.debug('remove router to firewall');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/firewall/remove_router_to_fw/',{firewall:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.listfws();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.removeRouter = function () {
    $scope.remove();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});





