from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from cats.forms import BreedForm
from cats.models import Cat, Breed

# --- VIEWS FOR CATS (Используем Generic Views) ---

class CatList(LoginRequiredMixin, View):
    def get(self, request):
        bc = Breed.objects.count()
        cl = Cat.objects.all()
        ctx = {'breed_count': bc, 'cat_list': cl}
        return render(request, 'cats/cat_list.html', ctx)

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')
    # Добавляем имя, чтобы в шаблоне работало {{ cat }}
    context_object_name = 'cat'


# --- VIEWS FOR BREEDS (Используем ручные View, как для Make) ---

class BreedList(LoginRequiredMixin, View):
    def get(self, request):
        bl = Breed.objects.all()
        ctx = {'breed_list': bl}
        return render(request, 'cats/breed_list.html', ctx)

class BreedCreate(LoginRequiredMixin, View):
    template = 'cats/breed_form.html'
    success_url = reverse_lazy('cats:breed_list')

    def get(self, request):
        # BreedForm должен быть создан в cats/forms.py (или используйте модель напрямую)
        from cats.forms import BreedForm
        form = BreedForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        from cats.forms import BreedForm
        form = BreedForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        form.save()
        return redirect(self.success_url)

class BreedUpdate(LoginRequiredMixin, View):
    model = Breed
    template = 'cats/breed_form.html'
    success_url = reverse_lazy('cats:breed_list')

    def get(self, request, pk):
        breed = get_object_or_404(self.model, pk=pk)
        from cats.forms import BreedForm
        form = BreedForm(instance=breed)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        breed = get_object_or_404(self.model, pk=pk)
        from cats.forms import BreedForm
        form = BreedForm(request.POST, instance=breed)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        form.save()
        return redirect(self.success_url)

class BreedDelete(LoginRequiredMixin, View):
    model = Breed
    template = 'cats/breed_confirm_delete.html'
    success_url = reverse_lazy('cats:breed_list')

    def get(self, request, pk):
        breed = get_object_or_404(self.model, pk=pk)
        ctx = {'breed': breed}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        breed = get_object_or_404(self.model, pk=pk)
        breed.delete()
        return redirect(self.success_url)