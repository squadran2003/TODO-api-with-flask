'use strict';

angular.module('todoListApp')
.factory('Todo', function($resource,$cookies){
  return $resource('/api/v1/todos/:id', {id: '@id'}, {
    'update': {
      method: 'PUT',
      headers:{
        'Authorization':'token '+$cookies.get("token")
      },

    },
    'save': {
      method: 'POST',
      headers:{
        'Authorization':'token '+$cookies.get("token")
      },

    },
    'delete': {
      method: 'DELETE',
      headers:{
        'Authorization':'token '+$cookies.get("token")
      },
 
    },
    query:{
      method:'GET',
      isArray:true,
      headers:{
        'Authorization':'token '+$cookies.get("token")
      },
      interceptor: {
        response: function(response) {      
            var result = response.resource;        
            result.$status = response.status;
            return result;
        }
      }
      

    },
    

  });

});




