# Django Imports
from django.shortcuts import render, redirect
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.contrib import messages


# User imports
from .models import Todo
from .forms import TodoForm
#----------------------------------------------------------

class Homeview(View):
    def get(self, request):
        context = {"todos": Todo.objects.all(),"form": TodoForm}
        return render(request, "app/home.html",context)

    def post(self,request):
        form = TodoForm(request.POST)
        if form.is_valid:
            form.instance.user = request.user
            form.save()
            messages.success(request,"Todo saved sucessfully!!")
            return redirect("app:home")
        
        # context = {"form": TodoForm}
        # return render(request,"app/home.html",context)

def delete(request,pk):
    if request.method == "POST":
        todo=Todo.objects.filter(id=pk)
        todo.delete()
        messages.success(request,"deleted successfully")
        return redirect("app:home")
    
def complete(request, pk):
    todo = get_object_or_404(Todo, id=pk)

    if request.method == "POST":
        if not todo.completed:
            # If the task is not completed, mark it as completed and delete
            todo.completed = True
            todo.save()
            
            messages.success(request, "Task marked as complete")
        else:
            # If the task is already completed, just delete it
            todo.delete()
            messages.success(request, "Task removed")

    return redirect("app:home")

    
        