'use strict';

angular.module('todoListApp')
.factory('Todo', function($resource,mytoken){
  return $resource('/api/v1/todos/:id', {id: '@id'}, {
    'update': {
      method: 'PUT',
      headers:{'Authorization':'token '+mytoken}
    },
    'save': {
      method: 'POST',
      headers:{'Authorization':'token '+mytoken}
    },
    'delete': {
      method: 'DELETE',
      headers:{'Authorization':'token '+mytoken}
    },
    query:{
      method:'GET',
      isArray:true,
      headers:{'Authorization':'token '+mytoken}
    },
    

  });
});


