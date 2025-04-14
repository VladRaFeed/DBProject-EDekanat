from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, DekanatWorkers
from .forms import GroupForm, DekanatWorkersForm
from django.contrib import messages

def home(request):
    groups = Group.objects.all()
    return render(request, 'home.html')

# GROUPS
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

def group_create(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Групу успішно створено!")
        return redirect('group_list')
    return render(request, 'group_form.html', {'form': form})

def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(request.POST or None, instance=group)
    if form.is_valid():
        form.save()
        messages.success(request, "Групу успішно оновлено!")
        return redirect('group_list')
    return render(request, 'group_form.html', {'form': form})


def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group.delete()
        messages.success(request, "Групу успішно видалено!")
        return redirect('group_list')
    return render(request, 'group_confirm_delete.html', {'group': group})

# DEKANAT WORKERS
def worker_list(request):
    workers = DekanatWorkers.objects.all()
    return render(request, 'worker_list.html', {'workers': workers})

def worker_create(request):
    form = DekanatWorkersForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Працівника успішно створено!")
        return redirect('worker_list')
    return render(request, 'worker_form.html', {'form': form})

def worker_update(request, pk):
    worker = get_object_or_404(DekanatWorkers, pk=pk)
    form = DekanatWorkersForm(request.POST or None, instance=worker)
    if form.is_valid():
        form.save()
        messages.success(request, "Працівника успішно оновлено!")
        return redirect('worker_list')
    return render(request, 'worker_form.html', {'form': form})

def worker_delete(request, pk):
    worker = get_object_or_404(DekanatWorkers, pk=pk)
    if request.method == "POST":
        worker.delete()
        messages.success(request, "Працівника успішно видалено!")
        return redirect('worker_list')
    return render(request, 'worker_confirm_delete.html', {'worker': worker})