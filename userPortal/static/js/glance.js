 var glanceControllers = angular.module('glanceControllers', ['ui.bootstrap','ngResource']);



 glanceControllers.controller('glanceCtrl', ['$scope', '$log','$http', '$rootScope',function($scope, $log, $http,$rootScope) {
       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };

      $rootScope.listGlance = function() {
        $log.debug('doneGet');
        var response = $http.get('/listGlance/');

        response.success(function(data, status, headers, config) {
            $log.debug('get success');
            $scope.imageList = data['images'][0];
            $scope.totalItems = $scope.imageList.length;
               $scope.numPerPage = 5;
               $scope.paginate = function (value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.imageList.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('get error');
        });
    };

     $rootScope.listGlance();


     /**
      * checkbox selected or not
      * @type {Array}
      */
    $rootScope.selected = [];
    $scope.selectedTags = [];


    var updateSelected = function(action,id,name){
        if(action == 'add' && $scope.selected.indexOf(id) == -1){
            $rootScope.selected.push(id);
            $scope.selectedTags.push(name);
        }

        if(action == 'remove' && $scope.selected.indexOf(id)!=-1){
            var idx = $scope.selected.indexOf(id);
            $rootScope.selected.splice(idx,1);
            $scope.selectedTags.splice(idx,1);
        }
    };

    $scope.updateSelection = function($event, id){
        var checkbox = $event.target;
        var action = (checkbox.checked?'add':'remove');
        updateSelected(action,id,checkbox.name);
    };

    $scope.isSelected = function(id){
        return $rootScope.selected!=undefined && $rootScope.selected.indexOf(id)>=0;
    }
 }]);


 glanceControllers.controller('deleteImageCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.deleteButtonClicked = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/confirm_glance_delete.html',
      controller: 'deleteImageInstanceCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

glanceControllers.controller('deleteImageInstanceCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.deleteImage = function() {
        $log.debug('deleteImage');
        $log.debug($rootScope.selected);
        var response = $http.post('/deleteImage/', $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('delete Success')
               $rootScope.listGlance();
               $rootScope.selected=[]
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
      $scope.deleteImage()
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

 //createImageCtrl
 glanceControllers.controller('createImageCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.createButtonClicked = function (size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/createImage.html',
      controller: 'createImageInstanceCtrl',
      //css:'/static/css/createImage.css',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});


 glanceControllers.controller('imageSourceCtr', function ($scope,$rootScope) {
    $rootScope.image_source_dropdown_list = []
           var flavorListSize = 2;
           data = [{'id':'1','name':'Image File'},{'id': '2','name' : 'Image URL'  }];
           for(var i = 0;i<flavorListSize;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $rootScope.image_source_dropdown_list.push(element)
           }

    $scope.onSelectedChange = function(){
        alert('root scope')
    }
});


glanceControllers.controller('createImageInstanceCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createImageClicked = function() {
        $log.debug('createImage');
        var args = {};

        if($scope.image_data.visibility!=undefined){
            $scope.image_data.visibility="public";
        }else
            $scope.image_data.visibility="private";

        if($scope.image_data.protected!=undefined){
            $scope.image_data.protected="True";
        }else
             $scope.image_data.protected="False";


        //$scope.image_data.disk_format="raw"
        $scope.image_data.container_format="bare"
        angular.copy($scope.image_data, args);
        $log.debug($scope.image_data);
        var response = $http.post('/createImage/',{image:args} );

        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success');
               $rootScope.listGlance();
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data)
            $log.debug('get error');
        });
    };

  $scope.createImage = function () {
    $scope.createImageClicked();
      $uibModalInstance.close();
  };


  $scope.cancelCreateImage = function () {
    $uibModalInstance.dismiss('cancelCreateImage');
  };
});

 //editImageCtrl--------------------------------------------------------------
 glanceControllers.controller('editImageCtrl', function ($scope, $uibModal, $log) {
  $scope.animationsEnabled = true;
  $scope.editImageButtonClicked = function(image) {

    $scope.edit = {};
    $scope.edit.id =image.id;
    $scope.edit.name =  image.name;
    $scope.edit.desc =  image.desc;
    $scope.edit.uri =  image.uri;
    $scope.edit.address =  image.address;
    $scope.edit.disk_format =  image.disk_format;
    $scope.edit.description =  image.description;
    //$scope.edit.arct =  image.arct;
    //$scope.edit.smallest_disk =  image.smallest_disk;
    //$scope.edit.lowest_memory =  image.lowest_memory;
    if (image.visibility=='public')
        $scope.edit.public =  true;
     else
        $scope.edit.public =  false;
    $scope.edit.protected =  image.protected;

    var modalInstance = $uibModal.open({scope: $scope,
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/image/editImage.html',
      controller: 'editImageInstanceCtrl'//,
      //css:'/static/css/createImage.css',
      //size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };
});



glanceControllers.controller('editImageInstanceCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.editImageClicked = function() {
        $log.debug('editImage');
        var args = {};

        if($scope.edit.public){
            $scope.edit.public="True"
        }else{
            $scope.edit.public="False"
        }

        if($scope.edit.protected){
            $scope.edit.protected="True"
        }else{
            $scope.edit.protected="False"
        }
        angular.copy($scope.edit, args);
        var response = $http.post('/editImage/',{image:args } );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('edit Success')
               $rootScope.listGlance();
            }
            else
                alert('edit Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('edit Failed:'+data)
            $log.debug('edit error');
        });
    }


   $scope.updateSelection = function($event,type){
        var checkbox = $event.target;
       if (type=='public') {
           $scope.edit.visibility = (checkbox.checked ? 'public' : 'private');
       }
       if(type=='protected' && checkbox.checked){
           $scope.edit.protected = "protected"
       }
    }

    $scope.isSelected = function(id){
        return $scope.selected.indexOf(id)>=0;
    }
  $scope.editImage = function () {
    $scope.editImageClicked()
    $uibModalInstance.close();
  };


  $scope.cancelEditImage = function () {
    $uibModalInstance.dismiss('cancelEditImage');
  };
});