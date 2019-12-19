from django.shortcuts import render

def verify_request(request):
    logged_in = request.COOKIES.get('id', False)
    if not logged_in:
        return False
    else:
        return True

def render_template(request, template_name, context={}):
    response = render(request, template_name, context)
    return response

# Create your views here.
def homepage(request):
    status = verify_request(request)
    if status == True:
        context = {
            'title': "Home"
        }
        return render_template(request, 'community/homepage.html', context)
    else:
        return render_template(request, 'community/previewpage.html')