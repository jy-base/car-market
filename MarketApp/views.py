import stripe
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.base import View
from Market import settings
from MarketApp import models
from random import shuffle
from MarketApp import forms


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['advertisement'] = models.Car.objects.filter(is_advertised=True).select_related(
            'brand').prefetch_related('image_set')
        if not len(context['advertisement']):
            ids_list = list(models.Car.objects.all().values_list('id', flat=True))
            shuffle(ids_list)
            context['advertisement'] = models.Car.objects.filter(id__in=ids_list[:6]).select_related(
                'brand').prefetch_related('image_set')
        return context


class BrandPageView(FormView):
    template_name = 'brands.html'
    form_class = forms.FilterForm

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(BrandPageView, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
            'brand').prefetch_related('image_set')
        return context

    def get_form_kwargs(self):
        kwargs = super(BrandPageView, self).get_form_kwargs()
        kwargs['brand_id'] = self.kwargs['brand_id']
        return kwargs


class BrandContent(TemplateView):
    template_name = 'brand_content.html'

    def get_context_data(self, **kwargs):
        context = super(BrandContent, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        data = self.request.GET
        if len(data):
            context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id'])
            if data['colour'] != 'any colour':
                context['cars'] = context['cars'].filter(colour=data['colour'])
            if data['in_stock_only']:
                context['cars'] = context['cars'].filter(stock_count__gt=0)
            context['cars'] = context['cars'].filter(year__lte=data['max_year'], year__gte=data['min_year'],
                                                     number_of_seats=data['number_of_seats'],
                                                     price__gte=data['min_price'],
                                                     price__lte=data['max_price']).select_related(
                'brand').prefetch_related('image_set')
        else:
            context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
                'brand').prefetch_related('image_set')
        return context


class CarPageView(DetailView):
    template_name = 'cars.html'
    model = models.Car

    def get_context_data(self, **kwargs):
        context = super(CarPageView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['stripe_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super(ThanksView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['car'] = models.Car.objects.get(id=self.kwargs['pk'])
        return context


class ErrorView(TemplateView):
    template_name = 'error.html'

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        return context


class CheckOutView(View):
    def post(self, request, *args, **kwargs):
        token = request.POST.get("stripeToken")
        car = models.Car.objects.get(id=self.kwargs['pk'])
        car.stock_count -= 1
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe.Charge.create(
                amount=car.price * 100,
                currency="usd",
                source=token,
                description=f"{car} was sold to {request.user}"
            )
        except stripe.error.CardError as e:
            return redirect('error/')
        else:
            car.save()
            return redirect('thanks/')
