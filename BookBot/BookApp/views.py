from django.shortcuts import render,redirect
from .models import *
from dotenv import load_dotenv
from .services import *
# from django.contrib
# Create your views here.
load_dotenv()


from .models import *
from django.shortcuts import get_list_or_404,get_object_or_404
from .models import *


def reset(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    Message.objects.filter(session_key=session_key).delete()
    return redirect('home')

def chat(request):
    if not request.session.session_key:
        request.session.create()
    session_key =request.session.session_key
    if request.method == 'POST':
        user_message = request.POST.get('message','').strip()
        if user_message:
            past = Message.objects.filter(session_key = session_key).order_by('timestamp')
            history =[{'role':m.role, 'content': m.content} for m in past]

            reply,source = Convo(user_message,history)

            Message.objects.create(role='user',content=user_message,session_key=session_key)
            Message.objects.create(role='bot',content=reply,source='Groq',session_key=session_key)
        return redirect('home')

    context = {
    'messages': Message.objects.filter(session_key=session_key).order_by('timestamp')
    }
    return render(request,'home.html',context)

def home(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    suggestions = Suggestions.objects.all()
    messages = Message.objects.filter(session_key=session_key).order_by('timestamp')

    context ={
        'suggestions':suggestions,
        'messages':messages,
    }
    return render(request,'home.html',context)

