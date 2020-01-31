from django.shortcuts import render, reverse, redirect
from accounts.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.forms import UserCreationForm

logger = logging.getLogger(__name__)
# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    logging.debug("Request method type: {method}".format(method=request.method))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logging.info("Redirect to root")
            return redirect('/')
        else:
            logging.info("Render login view")
            return render(request, 'accounts/login.html')
    logging.info("Render login view")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    logging.info("Redirect to root")
    return redirect('/')

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.profile.birth_date = form.cleaned_data.get('birth_date')
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/signup.html', {'form': form})

def profile_view(request, id):
    # Displays the user profile info

    return render(request, 'accounts/profile.html')

from django.views import View
# ------------ Test
def list(request):
    if request.method == 'POST':
        #Check if the form is valid then 
        #save the documentform file in the document model
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            csvimport(newdoc.docfile)

            #Redirect to list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        #If there are any documents already uploaded then show them and show them the form
        form = DocumentForm()
    documents = Document.objects.all()
    return render( 
        request,
        'list.html',
        {'form':form,
        'documents':documents}
    )