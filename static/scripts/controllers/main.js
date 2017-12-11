'use strict';

angular.module('todoListApp')
.controller('mainCtrl', function($scope, Todo, $cookies){


  $scope.addTodo = function() {
    var todo = new Todo();
    todo.name = 'New task!'
    todo.completed = false;
    $scope.todos.unshift(todo);
  };

});
