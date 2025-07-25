from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests

def search_page(request):
    return render(request, 'taskapp/index.html')

def get_search(request, searchtag):
    if get_data(searchtag):
        return JsonResponse(get_data(searchtag))
    else:
        return JsonResponse({'error': 'No search tag provided'}, status=400)
    
def info_page(request, drinkName):
    print(drinkName)
    return render(request, 'taskapp/info.html')

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
