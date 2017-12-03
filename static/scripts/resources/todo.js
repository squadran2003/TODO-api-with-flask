'use strict';

angular.module('todoListApp')
.factory('Todo', function($resource){
  return $resource('/api/v1/todos/:id', {id: '@id'}, {
    update: {
      method: 'PUT'
    },
    query:{
        method:'GET',
        headers:{
            'Authorization':'token '+' eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxMjI4OTkwMCwiZXhwIjoxNTEyMjkyOTAwfQ.eyJpZCI6MX0.vpTJ403nkRxGlzYURxzPa9_9UjGj1gbZckREBVGz7dE'
        }
    }
  });
});