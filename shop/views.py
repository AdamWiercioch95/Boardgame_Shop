from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop.models import Boardgame, Cart, CartBoardgame, Order, OrderBoardgame, Review


class BoardgameListView(ListView):
    model = Boardgame
    template_name = "shop/boardgames_list.html"


class BoardgameDetailView(DetailView):
    model = Boardgame
    template_name = "shop/boardgame_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = Review.objects.get(user=self.request.user, boardgame=self.get_object())
        boardgame = self.get_object()
        context["review"] = review
        context['is_reviewed'] = Review.objects.filter(user=self.request.user, boardgame=boardgame).exists()
        return context


class BoardgameAddView(UserPassesTestMixin, CreateView):
    model = Boardgame
    fields = '__all__'
    template_name = "shop/form.html"
    success_url = reverse_lazy('boardgames_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Boardgame'
        return context

    def test_func(self):
        return self.request.user.is_superuser


class BoardgameUpdateView(UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        return self.request.user.is_superuser


class BoardgameDeleteView(UserPassesTestMixin, DeleteView):
    model = Boardgame
    template_name = 'shop/boardgame_confirm_delete.html'
    success_url = reverse_lazy('boardgames_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Boardgame'
        return context

    def test_func(self):
        return self.request.user.is_superuser


class CartListView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'shop/cart_list.html', {'cart': cart})


class AddBoardgameToCartView(LoginRequiredMixin, View):
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


class DeleteBoardgameFromCartView(LoginRequiredMixin, View):
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


class MakeOrderView(LoginRequiredMixin, View):
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        if created or not cart.cartboardgame_set.all():
            return redirect('cart_list')

        order = Order.objects.create(user=request.user)

        for cart_boardgame in cart.cartboardgame_set.all():
            OrderBoardgame.objects.create(boardgame=cart_boardgame.boardgame,
                                          order=order,
                                          quantity=cart_boardgame.quantity)

        cart.cartboardgame_set.all().delete()
        return redirect('cart_list')


class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_detail.html'


class ReviewAddView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'shop/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Review'
        return context

    def form_valid(self, form):
        boardgame_pk = self.kwargs['boardgame_pk']
        boardgame = Boardgame.objects.get(pk=boardgame_pk)

        if Review.objects.filter(user=self.request.user, boardgame=boardgame).exists():
            raise IntegrityError("You have already added review for this game.")

        form.instance.boardgame = boardgame
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('boardgame_details', kwargs={'pk': self.kwargs['boardgame_pk']})

    def test_func(self):
        return self.request.user.is_authenticated


class ReviewDitailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'shop/review_detail.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Review Detail'
        return context
