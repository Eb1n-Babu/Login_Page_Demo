from entry.Form import SignUpForm
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt



def Home(request):
    return render(request,'home.html')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

messages_list = []

@csrf_exempt
def Login(request):
    global messages_list

    if request.method == 'POST':
        # Handle login
        if 'username' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                auth.login(request, user)
                return render(request, 'welcome.html', {'user': user, 'messages': messages_list})
        # Handle message post/delete after login
        elif 'message' in request.POST or 'delete' in request.POST:
            user = request.user
            if request.user.is_authenticated:
                if 'delete' in request.POST:
                    idx = int(request.POST.get('delete'))
                    if 0 <= idx < len(messages_list):
                        messages_list.pop(idx)
                elif 'message' in request.POST:
                    msg = request.POST.get('message')
                    if msg:
                        messages_list.append(msg)
                return render(request, 'welcome.html', {'user': user, 'messages': messages_list})
            else:
                form = AuthenticationForm()
                return render(request, 'login.html', {'form': form})

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})