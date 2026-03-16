from django.shortcuts import render
from django.http import HttpResponse
def myview(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    content = f'view count={num_visits}\n'
    content += f'<p>0147329e</p>'
    resp = HttpResponse(content)
    resp.set_cookie('dj4e_cookie', '0147329e', max_age=1000)


    return resp
