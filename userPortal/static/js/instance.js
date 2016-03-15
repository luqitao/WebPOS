 var instanceControllers = angular.module('instanceControllers', ['ui.bootstrap','ngResource','ng.bs.dropdown']);

//Instance dropDown action
instanceControllers.controller("InstanceActionController", function($scope,$http,$log,$rootScope,$uibModal){
        $scope.action = [
            "Soft Reboot Instance",
            "Hard Reboot Instance",
            "Pause Instance",
            "Start Instance",
            "Stop Instance",
            "Migrate Instance",
            "Live Migrate Instance",
            "Associate Floating IP",
            "Disassociate Floating IP",
            "Connect Console"
        ];
        $scope.selectAction = $scope.action[0];  //current select item

        /*changeYear function will be called if dropdown change*/
        $scope.changeAction = function(instance){
            //alert('selected:'+$scope.selectAction +":"+instance.id)
            var operate_type ;
                if($scope.selectAction=="Hard Reboot Instance"){
                    operate_type='HARD'
                }else if($scope.selectAction=="Soft Reboot Instance"){
                    operate_type='SOFT'
                }else if($scope.selectAction=="Pause Instance"){
                    operate_type='pause'
                }else if($scope.selectAction=="Migrate Instance"){
                    operate_type='migrate'
                }else if($scope.selectAction=="Start Instance"){
                    operate_type='os-start'
                }else if($scope.selectAction=="Stop Instance"){
                    operate_type='os-stop'
                }

            if($scope.selectAction=="Associate Floating IP")
            {
               var modalInstance = $uibModal.open({
               animation: $scope.animationsEnabled,
               templateUrl: '/static/view/network/associateip.html',
               controller: 'associateipCtrl',
               size: 500
              });
            }
            else if($scope.selectAction=="Disassociate Floating IP")
            {
               if(instance.addresses.length == 0 || instance.addresses.length == 1)
               {
                  alert('no floating ip to disassociate');
               }
               else
               {
                  var address = instance.addresses.split(",");
                  $rootScope.floatingip = address[1];
                  if($rootScope.floatingip.length == 0)
                  {
                     alert('no floating ip to disassociate');
                  }
                  else
                  {
                      var modalInstance = $uibModal.open({
                      animation: $scope.animationsEnabled,
                      templateUrl: '/static/view/image/confirm_glance_delete.html',
                      controller: 'disassociateipCtrl'
                     });
                  }
               }
            }

            else if($scope.selectAction=="Connect Console")
            {
                    var response = $http.post('/instance/console_url/?id='+instance.id);

                     response.success(function (data, status, headers, config) {
                         $log.debug('get success');
                         if (data['Success'] == 'OK'){

                            $log.debug('get success###########');

                            $scope.url = data['Date']

                            $log.debug('get success$$$$$$$$')
                            $log.debug($scope.url);
                            var modalInstance = $uibModal.open({
                            scope:$scope,
                            animation: $scope.animationsEnabled,
                            templateUrl: '/static/view/instance/instance_console.html',
                            controller: 'connectconsoleCtrl',
                            size:'large'
                      });
                         }
                         else
                             alert('Connect Console Failed')
                     });
                         response.error(function (data, status, headers, config) {
                         alert('Connect Console Failed:'+data)
                         $log.debug('get error');
                     });
                      console.log("InstanceActionController say... " + $scope.selectAction);


            }

        else
        {
           var response = $http.post('/operateInstance/?operate_type='+operate_type+'&id='+instance.id);

           response.success(function (data, status, headers, config) {
               $log.debug('get success');
               if (data['Success'] == 'OK'){
                  alert($scope.selectAction+' Success')
                  $rootScope.listInstance();
                  $rootScope.selected=[]
               }
               else
                   alert('rebootInstance Failed')
           });
               response.error(function (data, status, headers, config) {
               alert('rebootInstance Failed:'+data)
               $log.debug('get error');
           });
            console.log("InstanceActionController say... " + $scope.selectAction);
        }
        }
    });


 //list instance controller
 instanceControllers.controller('instanceCtrl', ['$scope', '$log','$http', '$rootScope',function($scope, $log, $http,$rootScope) {
       $scope.predicate = 'name';
       $scope.reverse = true;
       $scope.currentPage = 1;
       $scope.order = function (predicate) {
         $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
         $scope.predicate = predicate;
       };

      $rootScope.listInstance = function() {
        $log.debug('doneGet');
        var response = $http.get('/listInstance/');
        response.success(function(data, status, headers, config) {
            $log.debug('listInstance get success');
            $scope.instanceList = data;
              $scope.totalItems = $scope.instanceList.length;
               $scope.numPerPage = 5;
               $scope.paginate = function(value) {
                 var begin, end, index;
                 begin = ($scope.currentPage - 1) * $scope.numPerPage;
                 end = begin + $scope.numPerPage;
                 index = $scope.instanceList.indexOf(value);
                 return (begin <= index && index < end);
               };
        });
        response.error(function(data, status, headers, config) {
            $log.debug('listInstance get error');
        });
    };

     $rootScope.listInstance();

     /**
      * checkbox selected or not
      * @type {Array}
      */
    $rootScope.instanceSelected = [];
    $rootScope.instanceSelectedTags = [];

    var updateInstanceSelected = function(action,id,name){
        if(action == 'add' && $rootScope.instanceSelected.indexOf(id) == -1){
            $rootScope.instanceSelected.push(id);
            $rootScope.instanceSelectedTags.push(name);
        }

        if(action == 'remove' && $scope.instanceSelected.indexOf(id)!=-1){
            var idx = $rootScope.instanceSelected.indexOf(id);
            $rootScope.instanceSelected.splice(idx,1);
            $rootScope.instanceSelectedTags.splice(idx,1);
        }
    }

    $scope.updateInstanceSelection = function($event, id){
        var checkbox = $event.target;
        var action = (checkbox.checked?'add':'remove');
        updateInstanceSelected(action,id,checkbox.name);
    }

    $scope.isInstanceSelected = function(id){
        return  $rootScope.instanceSelected.indexOf(id)>=0;
    }
 }]);



 glanceControllers.controller('launchInstanceCtrl', function ($scope, $uibModal) {
  $scope.animationsEnabled = true;

  $scope.launchButtonClicked = function(size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/instance/launchInstance.html',
      controller: 'launchInstancePageCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

//获取flavor list dropdown
glanceControllers.controller('flavorCtr', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/list_flavor/');
    $rootScope.flavor_list = []
       response.success(function (data) {
           $log.debug('get success');
           var flavorListSize = data.length;

           for(var i = 0;i<flavorListSize;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $rootScope.flavor_list.push(element)
           }
       });
});

//获取network list dropdown
glanceControllers.controller('networkNameCtr', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/instance/list_network_names/');
    $scope.network_list = []
       response.success(function (data) {
           $log.debug('get success');
           var networkNameListSize = data.length;
           for(var i = 0;i<networkNameListSize;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $scope.network_list.push(element)
           }
       });

    var response = $http.get('/instance/list_network_port_names/');
    $scope.network_port_list = []
       response.success(function (data) {
           $log.debug('get success');
           var networkPortListSize = data.length;
           for(var i = 0;i<networkPortListSize;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $scope.network_port_list.push(element)
           }
       });
});

//获取networkPort list dropdown
glanceControllers.controller('networkPortCtr', function ($scope,$rootScope,$http,$log) {

    var response = $http.get('/instance/list_network_port_names/');
    $scope.network_port_list = []
       response.success(function (data) {
           $log.debug('get success');
           var networkPortListSize = data.length;
           for(var i = 0;i<networkPortListSize;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $scope.network_port_list.push(element)
           }
       });
});



//获取镜像ImageName List
glanceControllers.controller('imageNameCtr', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/instance/list_imageNames/');
    $scope.imageName_list = []
       response.success(function (data) {
           $log.debug('get success');
           var imageNameListSize = data.length;
           for(var i = 0;i<imageNameListSize;i++){
               var element ={
                   id:data[i].id,
                   name:data[i].name
               }
               $scope.imageName_list.push(element)
           }
       });
});


glanceControllers.controller('launchInstancePageCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.launchInstance = function() {
        $log.debug('launchInstancePageCtrl');
        var args = {}
        args['available_zone']=$scope.data.available_zone
        args['name']= $scope.data.name;
        args['flavorRef']= $scope.data.flavorRef;
        args['imageRef']= $scope.data.imageRef;
        //args['metadata']= {
        //                "My Server Name": "Apache1"
        //            };
        //args['networks']= $scope.data.networks;
        //alert('===='+$scope.data.networks.length)
        alert('==port=='+$scope.data.networksport)
        alert('network--'+$scope.data.networks)
        if ($scope.data.networksport==undefined ||$scope.data.networks!=undefined) {
            var len = $scope.data.networks.length
            args['is_network'] = 'true'
            if (len ==1){
                args['networks'] = [{"uuid": $scope.data.networks[0]}]
            }else {
            //    var arrays = new Array(len)
            //    var str =""
            //    for (var i = 0; i < len; i++) {
            //        alert($scope.data.networks[i] )
            //       str = str+"{"+"uuid:"+ $scope.data.networks[i]+"},"
            //    }
            //    str = str.substring(0,str.length-1)
            //    alert(str)
                args['networks'] = $scope.data.networks

            }
        }else if($scope.data.networksport!=undefined){
            args['networks'] = $scope.data.networksport
        }

        //args['return_reservation_id']= "false";
        args['min_count']= $scope.data.instanceNum;
        args['max_count']= $scope.data.instanceNum;
        var response = $http.post('/launchInstance/',{server: args} );

        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('launchInstance Success')
               $rootScope.listInstance();
               $rootScope.instanceSelected=[]
            }
            else
                alert('launchInstance Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('launchInstance Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.launchInstanceClicked = function () {
    $scope.launchInstance()
    $uibModalInstance.close();
  };

  $scope.cancelLaunchInstance = function () {
    $uibModalInstance.dismiss('cancel');
  };
});




glanceControllers.controller('terminateInstanceCtrl', function ($scope, $uibModal,$rootScope) {
  $scope.animationsEnabled = true;

  $scope.terminateButtonClicked = function(size) {
    $scope.selectedTags=$rootScope.instanceSelectedTags;
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/static/view/instance/confirm_instance_terminate.html',
      controller: 'terminateInstancePageCtrl',
      size: size
    });
  };
  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

glanceControllers.controller('terminateInstancePageCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {
    $scope.ternaminateInstance = function() {
        $log.debug('terminateInstance');
        var response = $http.post('/terminateInstance/',$rootScope.instanceSelected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('terminateInstance Success')
               $rootScope.listInstance();
               $rootScope.instanceSelected=[]
            }
            else
                alert('terminateInstance Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('terminateInstance Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.ok = function () {
    $scope.ternaminateInstance()
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});


 glanceControllers.controller('editInstanceCtrl', function ($scope, $log,$rootScope,$http) {
    $scope.editInstanceButtonClicked = function() {
        $log.debug('editInstance');
        var response = $http.post('/editInstance/' + $rootScope.instanceSelected);
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('editInstance Success')
               $rootScope.listInstance();
               $rootScope.instanceSelected=[]
            }
            else
                alert('editInstance Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('editInstance Failed:')
            $log.debug('get error'+data);
        });
    }
});


instanceControllers.controller('associateipCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.associate = function() {
        $log.debug('associateipCtrl');
        var args = {}
        angular.copy($scope.data, args);
        $log.debug($scope.data);

        var response = $http.post('/floatingip/associate_ip/',{info:args} );

        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('associate ip Success')
               $rootScope.listInstance();
               $rootScope.instanceSelected=[]
            }
            else
                alert('associate Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('associate Failed:'+data)
            $log.debug('get error');
        });
    }

    $scope.inifloatingip = function () {

       var response = $http.get('/floatingip/list_floatingip/');
       $rootScope.ips = []
       response.success(function (data) {
           $log.debug('get floating ips');
           var ip_list = data["floatingips"];
           var Num = ip_list.length;
           for(var i = 0;i<Num;i++){
               var element ={
                   id:ip_list[i].id,
                   name:ip_list[i].floating_ip_address
               }
               $rootScope.ips.push(element)
           }
           $log.debug($rootScope.ips);
       });
  };


   $scope.iniports = function () {

       var response = $http.get('/floatingip/list_ports/');
    $rootScope.ports = []
       response.success(function (data) {
           $log.debug('get ports');
           var list_ports = data["ports"];
           var Num = list_ports.length;

           for(var i = 0;i<Num;i++){
               var element ={
                   id:list_ports[i].id,
                   name:list_ports[i].name
               }
               $rootScope.ports.push(element)
           }
           $log.debug($rootScope.ports);
       });
  };

   $scope.inifloatingip()
   $scope.iniports()

  $scope.associateIP = function () {
    $scope.associate()
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});


//list floating ip
instanceControllers.controller('ipCtrl', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/floatingip/list_floatingip/');
    $rootScope.ips = []
       response.success(function (data) {
           $log.debug('get floating ips');
           var ip_list = data["floatingips"];
           var Num = ip_list.length;
//           alert(projectNum);
           for(var i = 0;i<Num;i++){
               var element ={
                   id:ip_list[i].id,
                   name:ip_list[i].floating_ip_address
               }
               $rootScope.ips.push(element)
           }
           $log.debug($rootScope.ips);
       });
});

//list ports
instanceControllers.controller('portCtrl', function ($scope,$rootScope,$http,$log) {
    var response = $http.get('/floatingip/list_ports/');
    $rootScope.ports = []
       response.success(function (data) {
           $log.debug('get ports');
           var list_ports = data["ports"];
           var Num = list_ports.length;

           for(var i = 0;i<Num;i++){
               var element ={
                   id:list_ports[i].id,
                   name:list_ports[i].name
               }
               $rootScope.ports.push(element)
           }
           $log.debug($rootScope.ports);
       });
});


instanceControllers.controller('disassociateipCtrl', function ($scope, $uibModalInstance,$log,$rootScope,$http) {

    $scope.disassociateip = function() {
        $log.debug('disassociate ip');
        args = {'ip': $rootScope.floatingip}
        $log.debug(args);
        var response = $http.post('/floatingip/disassociate_ip/',{info:args} );
        response.success(function (data, status, headers, config) {
            $log.debug('get success');
            if (data['Success'] == 'OK'){
               alert('disassociate Success')
               $rootScope.listInstance();
            }
            else
                alert('disassociate Failed')
        });
        response.error(function (data, status, headers, config) {
            alert('disassociate Failed:'+data)
            $log.debug('get error');
        });
    }

  $scope.ok = function () {
      $scope.disassociateip()
      $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

instanceControllers.controller('connectconsoleCtrl', function ($sce, $scope, $uibModalInstance,$log,$rootScope,$http) {
    $log.debug("sasasasasasas")


    $log.debug($scope.url)
    $scope.consoleurl = $sce.trustAsResourceUrl($scope.url);


});
