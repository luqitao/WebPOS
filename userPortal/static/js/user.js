 var userControllers = angular.module('userControllers', ['ui.bootstrap','ngResource']);

 userControllers.controller('userCtrl', ['$scope', '$log','$http', '$rootScope',function($scope, $log, $http,$rootScope) {
       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };

      $rootScope.listUser = function() {
        $log.debug('doneGet');
        var response = $http.get('/listUser/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            $scope.userList = data['users'];
              $scope.totalItems = $scope.userList.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.userList.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    };

     $rootScope.listUser();


     /**
      * checkbox selected or not
      * @type {Array}
      */
    $rootScope.selectedUser = [];
    $scope.selectedUserTags = [];


    var updateUserSelected = function(action,id,name){
        if(action == 'add' && $scope.selectedUser.indexOf(id) == -1){
            $rootScope.selectedUser.push(id);
            $scope.selectedUserTags.push(name);
        }

        if(action == 'remove' && $scope.selectedUser.indexOf(id)!=-1){
            var idx = $scope.selectedUser.indexOf(id);
            $rootScope.selectedUser.splice(idx,1);
            $scope.selectedUserTags.splice(idx,1);
        }
    };

    $scope.updateUserSelection = function($event, id){
        var checkbox = $event.target;
        var action = (checkbox.checked?'add':'remove');
        updateUserSelected(action,id,checkbox.name);
    };

    $scope.isUserSelected = function(id){
        return $rootScope.selectedUser!=undefined && $rootScope.selectedUser.indexOf(id)>=0;
    }
 }]);


 userControllers.controller('deleteUserCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deleteUserButtonClicked = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/user/confirm_user_delete.html',
      controller: 'deleteUserDetailCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.
userControllers.controller('deleteUserDetailCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deleteUser = function() {
        $log.debug('deleteUser');
        $log.debug($rootScope.selectedUser);
        var response = $http.post('/deleteUser/', $rootScope.selectedUser);
        response.success(function (data) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('delete Success')
               $rootScope.listUser();
               $rootScope.selectedUser=[]
            }
            else
                alert('delete Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('delete Failed:'+data)
            $log.debug('get error');
        });
    };

  $scope.ok = function () {
      $scope.deleteUser()
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

 //createImageCtrl
 userControllers.controller('createUserCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;
  $scope.createUserButtonClicked = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/user/createUser.html',
      controller: 'createUserDetailCtrl',
      size: 'large'
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});


 userControllers.controller('userRoleCtr', function ($scope,$rootScope,$http,$log) {
    $rootScope.user_role_dropdown_list = []
        var response = $http.get('/listUserRole/');
        response.success(function (data) {
            $log.debug('get success');
                for(var i = 0;i<data.length;i++){
                   var element ={
                       id:data[i].id,
                       name:data[i].name
                   }
                   $scope.user_role_dropdown_list.push(element)
                }
        });
});


 userControllers.controller('projectCtr', function ($scope,$rootScope,$http,$log) {
    $rootScope.project_dropdown_list = []
        var response = $http.get('/listProjectName/');
        response.success(function (data) {
            $log.debug('get success');
               for(var i = 0;i<data.length;i++){
                   var element ={
                       id:data[i].id,
                       name:data[i].name
                   }
                   $scope.project_dropdown_list.push(element)
                }
        })
});

userControllers.controller('createUserDetailCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createUserClicked = function() {
        $log.debug('createUser');
        var args = {};
        $log.debug($scope.user_data);
        args.name = $scope.user_data.name
        args.password = $scope.user_data.confirmPassword
        args.default_project_id=$scope.user_data.default_project_id
        args.email = $scope.user_data.email
        args.role = $scope.user_data.role

        var response = $http.post('/createUser/',{user:args} );

        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('create Success');
               $rootScope.listUser();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    };

  $scope.createUser = function () {
    $scope.createUserClicked();
      $uibModalInstance.close();
  };


  $scope.cancelCreateUser = function () {
    $uibModalInstance.dismiss('cancelCreateUser');
  };
});

 //editUserCtrl--------------------------------------------------------------
 userControllers.controller('editUserCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;
  $scope.editUserButtonClicked = function(user) {

    $scope.edit = {};
    $scope.edit.id =user.id;
    $scope.edit.name =  user.name;
    $scope.edit.desc =  user.email;
    $scope.edit.uri =  user.project;

    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/editUser.html',
      controller: 'editUserDetailCtrl'//,
      //css:'/static/css/createImage.css',
      //size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



userControllers.controller('editUserDetailCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.editUserClicked = function() {
        $log.debug('editUser');
        var args = {};
        angular.copy($scope.edit, args);

        var response = $http.post('/editUser/',{user:args } );
        response.success(function (data) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('edit Success')
               $rootScope.listUser();
            }
            else
                alert('edit Failed')
        });
        response.error(function (data) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }


   $scope.updateUserSelection = function($event,type){
        var checkbox = $event.target;
       if (type=='public') {
           $scope.edit.visibility = (checkbox.checked ? 'public' : 'private');
       }
       if(type=='protected' && checkbox.checked){
           $scope.edit.protected = "protected"
       }
    }

    $scope.isSelected = function(id){
        return $scope.selectedUser.indexOf(id)>=0;
    }
  $scope.editUser = function () {
    $scope.editUserClicked()
    $uibModalInstance.close();
  };


  $scope.cancelEditUser = function () {
    $uibModalInstance.dismiss('cancelEditUser');
  };
});