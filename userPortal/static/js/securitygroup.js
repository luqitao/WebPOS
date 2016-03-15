var groupControllers = angular.module('groupControllers', ['ui.bootstrap','ngResource']);

 groupControllers.controller('groupCtrl', ['$scope', '$log','$http', '$rootScope', function($scope, $log, $http, $rootScope) {

       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };


      $rootScope.list_groups = function() {
        $log.debug('list security groups');
        var response = $http.get('/securitygroup/list_groups/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            $scope.groups = data['security_groups'];
              $scope.totalItems = $scope.groups.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.groups.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    }

     $rootScope.list_groups();


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


// create securitygroup Ctrl
 groupControllers.controller('creteGroupCtrl', function ($scope, $uibModal, $log) {

  $scope.animationsEnabled = true;
  $scope.createGroup = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createsecuritygroup.html',
      controller: 'createsgCtrl',
//    css:'/static/css/neutron.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});

groupControllers.controller('createsgCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createaction = function() {
        $log.debug('create security group');
        $log.debug($scope.data);
        var args = {};
        angular.copy($scope.data, args);
        var response = $http.post('securitygroup/create_group/',{groupinfo:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success')
               $rootScope.list_groups();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.creategroupsecurity = function () {
    $scope.createaction()
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel Create Security Group');
  };
});


//delete router controller
groupControllers.controller('delGroupCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;
  $scope.delGroup = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/confirm_glance_delete.html',
      controller: 'deletesgCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

groupControllers.controller('deletesgCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.delgroup = function() {
        $log.debug('delete security group');
        $log.debug($rootScope.selected);
        var response = $http.delete('/securitygroup/delete_group/' + $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['status'] == 'ok'){
               alert('delete Success')
               $rootScope.list_groups();
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
      $scope.delgroup()
      $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});


// edit network controller
 groupControllers.controller('editCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.editGroup = function(group) {

    $scope.data = {};
    $scope.data.id = group.id;
    $scope.data.name = group.name;
    $scope.data.description = group.description;

    $log.debug($scope.data);


    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createsecuritygroup.html',
      controller: 'editgroupCtrl',
      css:'/static/css/createImage.css'
      //size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



groupControllers.controller('editgroupCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.update = function() {
        $log.debug('edit security group');
        var args = {};
        angular.copy($scope.data, args);
        $log.debug(args);
        var response = $http.post('/securitygroup/update_group/',{group:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('update Success')
               $rootScope.list_groups();
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }

  $scope.creategroupsecurity = function () {
    $scope.update();
    $uibModalInstance.close();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});


// add grouprule controller
 routerControllers.controller('addsgruleCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.addRules = function(group) {

    $scope.data = {};
    $scope.data.id = group.id;
    $scope.data.name = group.name;
    $log.debug($scope.data);

    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/network/createsgrule.html',
      controller: 'createruleCtrl',
      //css:'/static/css/createImage.css',
      size: 500
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



routerControllers.controller('createruleCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.add = function() {
        $log.debug('add security group rule');
        var args = {};
        angular.copy($scope.data, args);

        var ports = [];
        if($scope.cb1 != undefined && $scope.cb1 != 'false')
        {
           ports.push($scope.cb1);
        }
        if($scope.cb2 != undefined && $scope.cb2 != 'false')
        {
           ports.push($scope.cb2);
        }
        if($scope.cb3 != undefined && $scope.cb3 != 'false')
        {
           ports.push($scope.cb3);
        }
        if($scope.cb4 != undefined && $scope.cb4 != 'false')
        {
           ports.push($scope.cb4);
        }
        if($scope.cb5 != undefined && $scope.cb5 != 'false')
        {
           ports.push($scope.cb5);
        }
        if($scope.cb6 != undefined && $scope.cb6 != 'false')
        {
           ports.push($scope.cb6);
        }
        if($scope.cb7 != undefined && $scope.cb7 != 'false')
        {
           ports.push($scope.cb7);
        }
        if($scope.cb8 != undefined && $scope.cb8 != 'false')
        {
           ports.push($scope.cb8);
        }
        if($scope.cb9 != undefined && $scope.cb9 != 'false')
        {
           ports.push($scope.cb9);
        }
        if($scope.cb10 != undefined && $scope.cb10 != 'false')
        {
           ports.push($scope.cb10);
        }

        $log.debug($scope.data);
        $log.debug(ports);


        if(ports.length == 0)
        {
           alert('please select rules!');
        }
        else
        {
            var response = $http.post('/securitygroup/add_grouprules/',{info:args,protocal:ports});
            response.success(function (data, status, headers, config) {
                $log.debug('get success');
                if (data['Success'] == 'OK'){
                   alert('Add security group  Success')
                   $rootScope.list_groups();
                }
                else
                    alert('Add Failed')
            });
            response.error(function (data, status, headers, config) {
                alert('Create Failed:'+data)
                $log.debug('Create error');
            });
            $uibModalInstance.close();
        }
    };

  $scope.addRules = function () {
    $scope.add();
  };


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel edit');
  };
});

