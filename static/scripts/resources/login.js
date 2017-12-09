'use strict';

angular.module('todoListApp')
.factory('login', function($resource){
    return $resource('/api/v1/users/token',{
        'get':{
            method:'GET',
            isArray:false,
            interceptor: {
                response: function(response) {      
                    var result = response.resource;        
                    result.$status = response.status;
                    return result;
                }
            }
      
          },

    });
})
.factory('Authenticate',function($resource){
    return $resource('/api/v1/users/:username_or_email/:password',
     {username_or_email:'@username_or_email',password:'@password'},
    {
        'get':{
            method:'GET',
            isArray:false,
            interceptor: {
                response: function(response) {      
                    var result = response.resource;        
                    result.$status = response.status;
                    return result;
                }
            }
        }
    });

});