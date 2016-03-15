var cinderControllers = angular.module('cinderControllers', ['ngTable', 'ui.bootstrap','ngResource','ng.bs.dropdown']);

cinderControllers.controller('cinderCtrl', ['$scope', '$log','$http', '$location', 'ngTableParams', '$rootScope', '$uibModal', function($scope, $log, $http, $location, ngTableParams, $rootScope, $uibModal) {

    //volumes
    $scope.queryvolumes = function(callback) {
        var response = $http.get('/volumeinfo/', {cache: false});
        response.success(function(data, status, headers, config) {
            $log.debug('listvolume success');
            $log.debug("-----------data-----------");
            $log.debug(data);
            callback(data);
            $scope.volumes = data['volumes']
        });
        response.error(function(data, status, headers, config) {
        });
    };

    $scope.page = 1;
    $scope.count = 6;

    $rootScope.listvolumes = function(page, count){
        $rootScope.selected = [];
        $scope.volumetableParams = new ngTableParams({
                page: 1,  // show first page
                count: 1           // count per page
            });
        $log.debug('-----listvolumes-----');
        $scope.queryvolumes(function(data) {
            $log.debug('-----queryvolumes-----');
            $scope.volumetableParams = new ngTableParams({
                page: page,            // show first page
                count: count            // count per page
                }, {
                    total: data['volumes'].length, // length of data
                    getData: function($defer,params) {
                        $log.debug('getdata...');
                        $log.debug(params.page());
                        $log.debug(params.count());
                        $scope.page = params.page();
                        $scope.size = params.count();
                        $defer.resolve(data['volumes'].slice((params.page() - 1) * params.count(),params.page() * params.count()));
                    }
             });
         });
     };
    $rootScope.listvolumes($scope.page, $scope.count);

    //snapshots
    $scope.querysnapshots = function(callback) {
        var response = $http.get('/snapshotinfo/', {cache: false});
        response.success(function(data, status, headers, config) {
            $log.debug('listsnapshot success');
            $log.debug("-----------data-----------");
            $log.debug(data);
            callback(data);
            $scope.snapshots = data['snapshots']
        });
        response.error(function(data, status, headers, config) {
        });
    };

    $rootScope.listsnapshots = function(page, count){
        $rootScope.selected = [];
        $scope.snapshottableParams = new ngTableParams({
                page: 1,  // show first page
                count: 1           // count per page
            });
        $log.debug('-----listsnapshots-----');
        $scope.querysnapshots(function(data) {
            $log.debug('-----querysnapshots-----');
            $scope.snapshottableParams = new ngTableParams({
                page: page,            // show first page
                count: count            // count per page
                }, {
                    total: data['snapshots'].length, // length of data
                    getData: function($defer,params) {
                        $log.debug('getdata...');
                        $log.debug(params.page());
                        $log.debug(params.count());
                        $scope.page = params.page();
                        $scope.size = params.count();
                        $defer.resolve(data['snapshots'].slice((params.page() - 1) * params.count(),params.page() * params.count()));
                    }
             });
         });
     };
    $rootScope.listsnapshots($scope.page, $scope.count);

    $scope.sort = function(keyname){
        $scope.sortKey = keyname;   //set the sortKey to the param passed
        $scope.reverse = !$scope.reverse; //if true make it false and vice versa
    };

      /**
      * checkbox selected or not
      * @type {Array}
      */
    $scope.selectedTags = [];


    var updateSelected = function(action,id,name){
        if(action == 'add' && $rootScope.selected.indexOf(id) == -1){
            $rootScope.selected.push(id);
            $scope.selectedTags.push(name);
        }

        if(action == 'remove' && $rootScope.selected.indexOf(id)!=-1){
            var idx = $rootScope.selected.indexOf(id);
            $rootScope.selected.splice(idx,1);
            $scope.selectedTags.splice(idx,1);
        }
        $log.debug($rootScope.selected)
    };

    $scope.updateSelection = function($event, id){
        var checkbox = $event.target;
        var action = (checkbox.checked?'add':'remove');
        updateSelected(action, id, checkbox.id);
    };

    $scope.isSelected = function(id){
        return $rootScope.selected.indexOf(id)>=0;
    };

    $scope.animationsEnabled = true;

    // Create Volume
    $scope.createVolume = function () {
        $scope.source = "No source, empty volume";
        var modelcreateVolume = $uibModal.open({
            scope:$scope,
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/createVolume.html',
            controller: 'createVolumeCtrl'
            //css: '/static/css/test.css'
        });
    };
    
    // Delete Volume
    $scope.deleteVolume = function () {
        var modeldeleteVolume = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/confirm_deleteVolume.html',
            controller: 'deleteVolumeCtrl'
            //css: '/static/css/test.css'
        });
    };

    //volume action
    $scope.volumeActionchange = function(action, volume){
        if(action == "Edit Volume") {
            $scope.editvolume = {};
            $scope.oldsize = volume.size;
            angular.copy(volume, $scope.editvolume);
            $log.debug(volume);
            $log.debug($scope.editvolume.id);
            $log.debug($scope.oldsize);
            $log.debug(volume.size);
            var modalVolume = $uibModal.open({
                scope: $scope,
                animation: $scope.animationsEnabled,
                templateUrl: '/static/view/model/editVolume.html',
                controller: 'editVolumeCtrl'
                //css: '/static/css/test.css'
            });
        }
        else if(action == "Create Snapshot"){
            $scope.volume_snapshot = {};
            angular.copy(volume, $scope.volume_snapshot);
            var modelcreateSnapshot = $uibModal.open({
                scope:$scope,
                animation: $scope.animationsEnabled,
                templateUrl: '/static/view/model/createSnapshot.html',
                controller: 'createSnapshotCtrl'
                //css: '/static/css/test.css'
            });
        }
        else{
            $scope.data = volume;
            var modalattVolume = $uibModal.open({
                scope: $scope,
                animation: $scope.animationsEnabled,
                templateUrl: '/static/view/model/manageAttachments.html',
                controller: 'manageAttachmentsCtrl'
                //css: '/static/css/test.css'
            });
        }
    };

    // Edit Volume
    $scope.editVolume = function(volume) {
        $scope.editvolume = {};
        $scope.oldsize = volume.size;
        angular.copy(volume, $scope.editvolume);
        $log.debug(volume);
        $log.debug($scope.editvolume.id);
        $log.debug($scope.oldsize);
        $log.debug(volume.size);
        var modalVolume = $uibModal.open({
            scope: $scope,
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/editVolume.html',
            controller: 'editVolumeCtrl'
            //css: '/static/css/test.css'
        });
    };

    //attachment
    $scope.attachments = function (volume) {
        $scope.data = volume;
        var modalattVolume = $uibModal.open({
            scope: $scope,
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/manageAttachments.html',
            controller: 'manageAttachmentsCtrl'
            //css: '/static/css/test.css'
        });
    };

    //create snapshot
    $scope.createSnapshot = function (volume) {
        $scope.volume_snapshot = {};
        angular.copy(volume, $scope.volume_snapshot);
        var modelcreateSnapshot = $uibModal.open({
            scope:$scope,
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/createSnapshot.html',
            controller: 'createSnapshotCtrl'
            //css: '/static/css/test.css'
        });
    };

    //edit snapshot
    $scope.editSnapshot = function(snapshot) {
        $scope.editsnapshot = {};
        angular.copy(snapshot, $scope.editsnapshot);
        $log.debug(snapshot);
        $log.debug($scope.editsnapshot.id);
        var modalSnapshot = $uibModal.open({
            scope: $scope,
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/editSnapshot.html',
            controller: 'editSnapshotCtrl'
            //css: '/static/css/test.css'
        });
    };

    //delete snapshot
    $scope.deleteSnapshot = function () {
        var modeldeleteSnapshot = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: '/static/view/model/confirm_deleteSnapshot.html',
            controller: 'deleteSnapshotCtrl'
            //css: '/static/css/test.css'
        });
    };

    //snapshot action
    $scope.snapshotActionchange = function(action,snapshot){
        $log.debug(action);
        if(action=="Edit Snapshot") {
            $scope.editsnapshot = {};
            angular.copy(snapshot, $scope.editsnapshot);
            $log.debug(snapshot);
            $log.debug($scope.editsnapshot.id);
            var modalSnapshot = $uibModal.open({
                scope: $scope,
                animation: $scope.animationsEnabled,
                templateUrl: '/static/view/model/editSnapshot.html',
                controller: 'editSnapshotCtrl'
                //css: '/static/css/test.css'
            });
        }
        else{
            $scope.snapshot_volume = "Snapshot_volume";
            $scope.snapshots = [snapshot];
            $scope.source = "Snapshot";
            var modelcreateVolume = $uibModal.open({
                scope: $scope,
                animation: $scope.animationsEnabled,
                templateUrl: '/static/view/model/createVolume.html',
                controller: 'createVolumeCtrl'
                //css: '/static/css/test.css'
            });
        }
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };
}]);

 // Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.



cinderControllers.controller('createVolumeCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createVolumeClicked = function() {
        $log.debug('createVolume');
        $log.debug($scope.data);
        var response = $http.post('/createVolume/', $scope.data);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('create Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data);
            $log.debug('get error');
        });
    };

    $scope.createVolume = function () {
      $scope.createVolumeClicked();
      $uibModalInstance.close();
    };


    $scope.cancelCreateVolume = function () {
      $uibModalInstance.dismiss('cancelCreateVolume');
    };
});

cinderControllers.controller('deleteVolumeCtrl', function ($scope, $uibModalInstance, $log, $rootScope, $http) {
    $scope.deleteVolumeClicked = function() {
        $log.debug('deleteVolume');
        $log.debug($rootScope.selected);
        var response = $http.post('/deleteVolume/', $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('delete Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('delete Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('delete Failed:'+data);
            $log.debug('get error');
        });
    };

    $scope.ok = function () {
        $scope.deleteVolumeClicked();
        $uibModalInstance.close();
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});

cinderControllers.controller('editVolumeCtrl', function ($scope, $uibModalInstance, $log, $rootScope, $http) {
    $scope.updateVolumeClicked = function() {
        $log.debug('updateVolume');
        $log.debug($scope.editvolume);
        $log.debug($scope.oldsize);
        var response = $http.post('/updateVolume/?id=' + $scope.editvolume.id, [$scope.editvolume,$scope.oldsize]);
        response.success(function (data, status, headers, config) {
            $log.debug('update success');

            if (data['Success'] == 'OK'){
               alert('update Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('update Failed:'+ data);
            $log.debug('update error');
        });
    };

    $scope.updateVolume = function () {
        $scope.updateVolumeClicked();
        $uibModalInstance.close();
    };


    $scope.cancelEditVolume = function () {
        $uibModalInstance.dismiss('cancelEditVolume');
    };
});

cinderControllers.controller('manageAttachmentsCtrl', function ($scope, $uibModalInstance, $log, $rootScope, $http) {
    $log.debug($scope.data.attachments);
    $scope.listInstance = function() {
        $log.debug('doneGet');
        var response = $http.get('/listInstance/');
        response.success(function(data, status, headers, config) {
            $log.debug('listInstance get success');
            $scope.instanceList = data;
            $log.debug($scope.instanceList)
        });
        response.error(function(data, status, headers, config) {
            $log.debug('listInstance get error');
        });
    };
    $scope.listInstance();

    $scope.instance_id = "";
    $scope.attachVolumeClicked = function() {
        $log.debug('attachVolume');
        var response = $http.post('/attachVolume/?id=' + $scope.data.id, $scope.instance_id);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('attach Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('attach Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data);
            $log.debug('get error');
        });
    };

    $scope.attachVolume = function () {
        $scope.attachVolumeClicked();
        $uibModalInstance.close();
    };


    $scope.cancelAttachVolume = function () {
        $uibModalInstance.dismiss('cancelAttachVolume');
    };

    $scope.detachVolume = function(attachment) {
        $log.debug('detachVolume');
        var response = $http.post('/detachVolume/', attachment[0]);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');

            if (data['Success'] == 'OK'){
               alert('detach Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('detach Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data);
            $log.debug('get error');
        });
    };
});

cinderControllers.controller('createSnapshotCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.createSnapshotClicked = function() {
        $log.debug('createSnapshot');
        var response = $http.post('/createSnapshot/?id=' + $scope.volume_snapshot.id, $scope.data);
        response.success(function (data, status, headers, config) {
            $log.debug('create success');

            if (data['Success'] == 'OK'){
               alert('create Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('create Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('create Failed:'+data);
            $log.debug('get error');
        });
    };

  $scope.createSnapshot = function () {
      $scope.createSnapshotClicked();
      $uibModalInstance.close();
  };


  $scope.cancelCreateSnapshot = function () {
      $uibModalInstance.dismiss('cancelCreateSnapshot');
  };
});

cinderControllers.controller('editSnapshotCtrl', function ($scope, $uibModalInstance, $log, $rootScope, $http) {
    $scope.updateSnapshotClicked = function() {
        $log.debug('updateSnapshot');
        $log.debug($scope.editsnapshot);
        var response = $http.post('/updateSnapshot/?id=' + $scope.editsnapshot.id, $scope.editsnapshot);
        response.success(function (data, status, headers, config) {
            $log.debug('update success');

            if (data['Success'] == 'OK'){
               alert('update Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('update Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('update Failed:'+ data);
            $log.debug('update error');
        });
    };

    $scope.updateSnapshot = function () {
        $scope.updateSnapshotClicked();
        $uibModalInstance.close();
    };


    $scope.cancelEditSnapshot = function () {
        $uibModalInstance.dismiss('cancelEditSnapshot');
    };
});

cinderControllers.controller('deleteSnapshotCtrl', function ($scope, $uibModalInstance, $log, $rootScope, $http) {
    $scope.deleteSnapshotClicked = function() {
        $log.debug('deleteSnapshot');
        $log.debug($rootScope.selected);
        var response = $http.post('/deleteSnapshot/', $rootScope.selected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('delete Success');
               $rootScope.listvolumes(1, 6);
            }
            else
                alert('delete Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('delete Failed:'+data);
            $log.debug('get error');
        });
    };

    $scope.ok = function () {
        $scope.deleteSnapshotClicked();
        $uibModalInstance.close();
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});