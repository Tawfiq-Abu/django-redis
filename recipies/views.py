from multiprocessing import context
from django.shortcuts import render
from django.views.generic import ListView,View
from .models import *
from django.core.cache import  cache
from django.http import HttpResponse


# Create your views here.
class Homeview(ListView):
    model = Recipe
    template_name = 'index.html'


class Recipeview(View):

    template_name = 'recipe.html'
    def get(self, request,*args, **kwargs):
        recipe_id = kwargs["pk"]

        if cache.get(recipe_id):
            recipe = cache.get(recipe_id)
            print('hit the cache')
        else:
            try:
                recipe = Recipe.objects.get(pk=recipe_id)
                cache.set(recipe_id,recipe)
                print('hit the db')
            except Recipe.DoesNotExist:
                return HttpResponse("this recipe does not exist")

        context = {
            "recipe":recipe,
        }
        return render(request,self.template_name,context)