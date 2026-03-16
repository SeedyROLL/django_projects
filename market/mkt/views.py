from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from mkt.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from mkt.models import Ad, Comment
from mkt.forms import CreateForm, CommentForm

from django.db.models import Q
from mkt.models import Ad

class AdListView(OwnerListView):
    model = Ad
    template_name = "mkt/ad_list.html"

    def get(self, request):
        strval = request.GET.get("search", False)
        if strval:
            query = Q(title__icontains=strval) | Q(text__icontains=strval) | Q(tags__name__in=[strval])
            ad_list = Ad.objects.filter(query).distinct().order_by('-updated_at')[:10]
        else:
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Логика избранного (из предыдущего шага)
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')
            favorites = [row['id'] for row in rows]

        ctx = {'ad_list': ad_list, 'search': strval, 'favorites': favorites}
        return render(request, self.template_name, ctx)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "mkt/ad_detail.html"

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        # Получаем список комментариев, связанных с этим объявлением
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        # Создаем пустую форму для нового комментария
        comment_form = CommentForm()
        context = {
            'ad': ad,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'mkt/ad_form.html'
    success_url = reverse_lazy('mkt:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Сохраняем модель, но не фиксируем в БД (commit=False)
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()

        # КРИТИЧЕСКИЙ МОМЕНТ: Сохраняем Many-to-Many данные (теги)
        form.save_m2m()

        return redirect(self.success_url)
class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'mkt/ad_form.html'
    success_url = reverse_lazy('mkt:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()
        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "mkt/ad_confirm_delete.html"

# Функция для отдачи картинки из базы
def stream_file(request, pk):
    # Получаем объект объявления по первичному ключу (ID)
    ad = get_object_or_404(Ad, id=pk)

    # Создаем пустой HTTP ответ
    response = HttpResponse()

    # Указываем тип контента (например, image/jpeg), который мы сохранили в базе
    response['Content-Type'] = ad.content_type

    # Указываем длину контента
    response['Content-Length'] = len(ad.picture)

    # Пишем байты картинки в тело ответа
    response.write(ad.picture)

    return response

from django.urls import reverse
from mkt.models import Ad, Comment
from mkt.owner import OwnerDeleteView

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Находим объявление, к которому пишется комментарий
        ad = get_object_or_404(Ad, id=pk)
        # Создаем объект комментария
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        # Возвращаемся на страницу деталей этого объявления
        return redirect(reverse('mkt:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "mkt/comment_delete.html"

    # Динамически определяем адрес перенаправления после удаления
    def get_success_url(self):
        ad = self.object.ad # 'ad' — это имя ForeignKey в твоей модели Comment
        return reverse('mkt:ad_detail', args=[ad.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.http import HttpResponse
from mkt.models import Ad, Fav

@method_decorator(csrf_exempt, name='dispatch')
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Находим объявление
        a = get_object_or_404(Ad, id=pk)
        # Создаем объект связи (но пока не сохраняем в БД)
        fav = Fav(user=request.user, ad=a)
        try:
            fav.save() # Пытаемся добавить в избранное
            return HttpResponse("Favorite added 42")
        except IntegrityError:  # Если уже в избранном, IntegrityError сработает из-за unique_together
            Fav.objects.get(user=request.user, ad=a).delete()
            return HttpResponse("Favorite deleted 42")
        except Exception as e:
            return HttpResponse("Error: " + str(e))