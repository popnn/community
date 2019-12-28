from django.shortcuts import render

# Create your views here.
def verify_request(request):
    return request.COOKIES.get('id', None) is not None, request.COOKIES.get('id', None)

def render_template(request, template_name, context={}):
    response = render(request, template_name, context)
    response.set_cookie('load', datetime.datetime.now().strftime("%H:%M:%S.%f %b %d %Y"))
    return response

def homepage(request):
    return render_template(request, 'chat/homepage.html', {})
