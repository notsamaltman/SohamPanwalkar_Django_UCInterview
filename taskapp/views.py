from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Drink
import requests
import re

def search_page(request):
    return render(request, 'taskapp/index.html')

def get_search(request, searchtag):
    if get_data(searchtag):
        return JsonResponse(get_data(searchtag))
    else:
        return JsonResponse({'error': 'No search tag provided'}, status=400)
    
def info_page(request, drinkName):
    data = get_data(drinkName)
    data = data.get('drinks')
    data = data[0]
    instruction = data.get('drinkinstruction')
    data['drinkinstruction'] = split_into_sentences(instruction)
    if Drink.objects.filter(name=drinkName).exists():
        founddrink = Drink.objects.get(name=drinkName)
        founddrink.searches += 1
        founddrink.save()
        data['searches'] = founddrink.searches
    return render(request, 'taskapp/info.html', {'drink':data})

def top10page(request):
    drinks = Drink.objects.order_by('-searches').values()[0:20]
    drinks = list(drinks)
    return render(request, 'taskapp/top10.html', {'drinks':drinks})

def get_data(search):
    typesrch = 's='
    url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?'+typesrch+search
    response = requests.get(url=url)
    data = response.json()
    drinks = data.get('drinks')
    if drinks:
        drinklist = []

        for drink in drinks:
            drinkid = drink.get('idDrink')
            drinkname = drink.get('strDrink')
            drinkimg = drink.get('strDrinkThumb')
            drinktypes = drink.get('strAlcoholic')
            drinkcategory = drink.get('strCategory')
            drinkInstruction = drink.get('strInstructions')

            if not Drink.objects.filter(name=drinkname).exists():
                newdrink = Drink.objects.create(name=drinkname, image=drinkimg)
            
            info = {'drinkid':drinkid,
                    'drinkname':drinkname,
                    'drinkimg':drinkimg,
                    'drinktypes':drinktypes,
                    'drinkcategory':drinkcategory,
                    'drinkinstruction':drinkInstruction
                    }
            drinklist.append(info)
        reply = {'drinks':drinklist}
        return reply
    else:
        return

def split_into_sentences(text):
    # Use regex to split on `.`, `?`, or `!` followed by a space and a capital letter
    sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
    sentences = sentence_endings.split(text)
    return [s.strip() for s in sentences if s.strip()]