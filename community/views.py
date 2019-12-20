from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

def verify_request(request):
    return request.COOKIES.get('id', None) is not None

def render_template(request, template_name, context={}):
    response = render(request, template_name, context)
    return response

# Create your views here.
def homepage(request):
    logged_in = verify_request(request)
    print(logged_in)
    if logged_in:
        context = {
            'title': "Home",
            'logged_in': logged_in,
            "all_cards": [],
        }
        for card_no in range(15):
            cnt = {
                'card_title': 'Sample Card #{}'.format(card_no),
                'card_text': ' Sample text: Welcom to popN Community, The one stop for all thats popN ;)',
            }
            context['all_cards'].append(cnt)
        return render_template(request, 'community/homepage.html', context)
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            print(1)
            if form.is_valid():
                print(1)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    response = redirect('/community')
                    response.set_cookie('id', username)
                    return response 
        else:
            form = AuthenticationForm()
        return render_template(request, 'community/previewpage.html', {'form': form})

def searchpage(request):
    logged_in = verify_request(request)
    if request.method == 'GET':
        query = request.GET.get('q', None)
    context = {
        'title': 'Search-{}'.format(query) if query is not None else 'Search',
        'query': query,
        'logged_in': logged_in,
    }
    
    if query is not None:
        context['search_results'] = search(query, logged_in)
    return render_template(request, 'community/searchpage.html', context)

def search(query, logged_in):
    pass