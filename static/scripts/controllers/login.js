'use strict';

angular.module('todoListApp')
.controller('loginCtrl',function($scope,login,$http,$base64,$cookies,$location,Authenticate){

            // if the user closes the browser remove the cookie
        $scope.onExit = function(){
                
                $cookies.remove('token');
        };
        
        $scope.error = false;
        $scope.errorMessage="this is an error";
        $scope.signin = function(){
                // remove the old cookie
                if($cookies.get('token')!=''){
                    $cookies.remove('token');
                }
                //$cookie.remove("token");
                var username = $scope.username;
                var password = $scope.password;
                var credentials = $base64.encode(username+':'+password);
                var auth = Authenticate.get(
                        {'username_or_email':username,
                        'password':password}
                );
                //catch any errors that occur during authentication
                auth.$promise.catch(function(result){
                        if(result.status==400){
                                $scope.error=true;
                                $scope.errorMessage="username/email or password doesnt match";

                        }

                }).then(function(result){
                        var result = $http.defaults.headers.common['Authorization']='Basic '+credentials;
                        var mytoken = login.get()
                        mytoken.$promise.then(function(result){
                                $cookies.put('token',result.token);
                                document.location.href = '/gettodos'
                        });    
                        
    
                        
                });

        }

});

