from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop.models import Boardgame


class BoardgameListView(ListView):
    model = Boardgame
    template_name = "shop/boardgames_list.html"


class BoardgameDetailView(DetailView):
    model = Boardgame
    template_name = "shop/boardgame_details.html"


class BoardgameAddView(CreateView):
    model = Boardgame
    fields = '__all__'
    template_name = "shop/form.html"
    success_url = reverse_lazy('boardgames_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Boardgame'
        return context


class BoardgameUpdateView(UpdateView):
    model = Boardgame
    fields = '__all__'
    template_name = "shop/form.html"
    success_url = reverse_lazy('boardgames_list')

    # def get_success_url(self):
    #     return reverse('boardgame_update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Boardgame'
        return context


class BoardgameDeleteView(DeleteView):
    model = Boardgame
    template_name = 'shop/boardgame_confirm_delete.html'
    success_url = reverse_lazy('boardgames_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Boardgame'
        return context

