 var projectControllers = angular.module('projectControllers', ['ui.bootstrap','ngResource']);

 projectControllers.controller('projectCtrl', ['$scope', '$log','$http', '$rootScope',function($scope, $log, $http,$rootScope) {
       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };

      $rootScope.listProject = function() {
        $log.debug('doneGet');
        var response = $http.get('/listProject/');
        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            $scope.projectList = data['projects'];
              $scope.totalItems = $scope.projectList.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.projectList.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    };

     $rootScope.listProject();


     /**
      * checkbox selected or not
      * @type {Array}
      */
    $rootScope.selectedProject = [];
    $scope.selectedProjectTags = [];


    var updateProjectSelected = function(action,id,name){
        if(action == 'add' && $rootScope.selectedProject.indexOf(id) == -1){
            $rootScope.selectedProject.push(id);
            $scope.selectedProjectTags.push(name);
        }

        if(action == 'remove' && $rootScope.selectedProject.indexOf(id)!=-1){
            var idx = $rootScope.selectedProject.indexOf(id);
            $rootScope.selectedProject.splice(idx,1);
            $scope.selectedProjectTags.splice(idx,1);
        }
    };

    $scope.updateProjectSelection = function($event, id){
        var checkbox = $event.target;
        var action = (checkbox.checked?'add':'remove');
        updateProjectSelected(action,id,checkbox.name);
    };

    $scope.isProjectSelected = function(id){
        return $rootScope.selectedProject!=undefined && $rootScope.selectedProject.indexOf(id)>=0;
    }
 }]);


 projectControllers.controller('deleteProjectCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deleteProjectButtonClicked = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/project/confirm_project_delete.html',
      controller: 'deleteProjectDetailCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.
projectControllers.controller('deleteProjectDetailCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deleteProject = function() {
        $log.debug('deleteProject');
        $log.debug($rootScope.selectedProject);
        var response = $http.post('/deleteProject/', $rootScope.selectedProject);
        response.success(function (data) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('delete Success')
               $rootScope.listProject();
               $rootScope.selectedProject=[]
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
      $scope.deleteProject()
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

 //createImageCtrl
 projectControllers.controller('createProjectCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;
  $scope.createProjectButtonClicked = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/project/createProject.html',
      controller: 'createProjectDetailCtrl',
      size: 'large'
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});


 projectControllers.controller('projectCtr', function ($scope,$rootScope,$http,$log) {
    $rootScope.user_dropdown_list = []
        var response = $http.get('/listUserName/');
        response.success(function (data) {
            $log.debug('get success');
               for(var i = 0;i<data.length;i++){
                   var element ={
                       id:data[i].id,
                       name:data[i].name
                   }
                   $scope.user_dropdown_list.push(element)
                }
        })
});

projectControllers.controller('createProjectDetailCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createProjectClicked = function() {
        $log.debug('createProject');
        var args = {};
        $log.debug($scope.project_data);
        args.name = $scope.project_data.name
        args.description = $scope.project_data.description
        args.project_user_id=$scope.project_data.project_user_id

        if (true==$scope.project_data.enabled)
            args.enabled='True'
        else
            args.enabled='False'



        var response = $http.post('/createProject/',{project:args});

        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('create Success');
               $rootScope.listProject();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    };

  $scope.createProject = function () {
    $scope.createProjectClicked();
      $uibModalInstance.close();
  };


  $scope.cancelCreateProject = function () {
    $uibModalInstance.dismiss('cancelCreateProject');
  };
});

 //editProjectCtrl--------------------------------------------------------------
 projectControllers.controller('editProjectCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;
  $scope.editProjectButtonClicked = function(project) {

    $scope.edit = {};
    $scope.edit.id =project.id;
    $scope.edit.name =  project.name;
    $scope.edit.desc =  project.email;
    $scope.edit.uri =  project.project;

    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/editproject.html',
      controller: 'editProjectDetailCtrl'//,
      //css:'/static/css/createImage.css',
      //size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



projectControllers.controller('editProjectDetailCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.editProjectClicked = function() {
        $log.debug('editProject');
        var args = {};
        angular.copy($scope.edit, args);

        var response = $http.post('/editProject/',{project:args } );
        response.success(function (data) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('edit Success')
               $rootScope.listProject();
            }
            else
                alert('edit Failed')
        });
        response.error(function (data) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }


   $scope.updateProjectSelection = function($event,type){
        var checkbox = $event.target;
       if (type=='public') {
           $scope.edit.visibility = (checkbox.checked ? 'public' : 'private');
       }
       if(type=='protected' && checkbox.checked){
           $scope.edit.protected = "protected"
       }
    }

    $scope.isSelected = function(id){
        return $scope.selectedProject.indexOf(id)>=0;
    }
  $scope.editProject = function () {
    $scope.editProjectClicked()
    $uibModalInstance.close();
  };


  $scope.cancelEditProject = function () {
    $uibModalInstance.dismiss('cancelEditProject');
  };
});