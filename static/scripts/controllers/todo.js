'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo) {

   $scope.todos = Todo.query();
   
  
    $scope.deleteTodo = function(todo,index) {
      $scope.todos.splice(index, 1);
      Todo.delete(todo);
    };

    $scope.saveTodos = function() {
        var filteredTodos = $scope.todos.filter(function(todo){
          if(todo.edited) {
            return todo;
          };
        });
        filteredTodos.forEach(function(todo) {
          if (todo.id) {
            Todo.update(todo);
          } else {
            Todo.save(todo);
          }

        });
  };
});

