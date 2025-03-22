from django.shortcuts import render , redirect
from .models import User , UserManager
from django.views.generic import View
from django.contrib.auth import authenticate, login 

# Create your views here.

'''making signup page view with custom user model(User)  using class based view 
and custom user manager  for user model  (UserManager)     
'''
class CreateUserView(View):
    template_name = 'accounts/signup.html'
    model = User
    fields = ['email', 'password']
    
    def get(self, request):       
        message = ''
        return render(request, self.template_name, context={ 'message': message})
    #post requets from form in signup.html and using for making new   
    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password1')
        passwordConf = self.request.POST.get('password2')
        if password == passwordConf :
            user = User.objects.create_user(email=email, password=password)
            return redirect('/')
        return render(request, self.template_name)



# making login page view with custom user model
class LoginPageView(View):
    template_name = 'accounts/login.html'
    model = User
    fields = ['email', 'password']
    
    def get(self, request):       
        message = ''
        return render(request, self.template_name, context={ 'message': message})
        
    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
    
        user = authenticate(
            request=self.request,
            username=email,
            password=password,
            )
        if user is not None:
            login(request, user)
            print('login successful')
            return redirect('/')
            
        else:
            print('login failed')
            print(email)
            print(password)
        message = 'Login failed!'
        return render(request, self.template_name, context={ 'message': message})
    