from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop.models import Boardgame, Cart, CartBoardgame


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


class CartListView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'shop/cart_list.html', {'cart': cart})


class AddBoardgameToCartView(View):
    def get(self, request, boardgame_pk):
        boardgame = Boardgame.objects.get(pk=boardgame_pk)
        cart, created = Cart.objects.get_or_create(user=request.user)

        try:
            cart_item = CartBoardgame.objects.get(boardgame=boardgame, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartBoardgame.DoesNotExist:
            cart.boardgames.add(boardgame)

        return redirect('boardgames_list')


class DeleteBoardgameFromCartView(View):
    def get(self, request, boardgame_pk):
        boardgame = Boardgame.objects.get(pk=boardgame_pk)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item = CartBoardgame.objects.get(boardgame=boardgame, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('cart_list')

