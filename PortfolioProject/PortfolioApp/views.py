from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Blog,Contact,Skills

# Create your views here.
def index(request):
    data=Skills.objects.all()
    context={"data":data}
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")

def contact(request):
    if not request.user.is_authenticated:
        messages.info(request,"Please Login to contact us")
        return render(request,"login.html")
    if request.method=="POST":
        name = request.POST['name']
        email= request.POST['email']
        phone = request.POST['num']
        desc = request.POST['desc']
        if len(phone)>10 or len(phone)<10 :
            messages.warning(request,"please enter 10 digit number")
            return redirect('/contact')
        query = contact(name=name,email=email,phone=phone,description=desc)
        query.save()
        messages.success(request,"Thanks for contacting us we will get back to you soon")
        return redirect('/contact')
        
    return render(request,"contact.html")

def blog(request):
    data = Blog.objects.all()
    print(data)
    context={"data":data}
    return render(request,"blog.html",context)


def signup(request):
   #  messages.success(request,"hey i am a alert message")
   #  messages.error(request,"hey i am a alert  danger message")
    if request.method=="POST":
       fname =request.POST.get('fname')
       lname =request.POST.get('lname')
       email =request.POST.get('email')
       pass1 =request.POST.get('pass1')
       pass2 =request.POST.get('pass2')
       print(fname,lname,email,pass1,pass2)
      #  messages.info(request,f'{fname},{lname},{email},{pass1},{pass2}') just for checking data is displaying or not
      
      # Validate password and confirm password
       if  pass2!= pass1:
          messages.warning(request,"Password is not matching")
          return redirect('/signup'  )
      
      
      # I am validating the user exist or not with the same email and username
       try:
           if User.objects.get(username = email):
               messages.warning(request,"User already exists")
               return redirect('/signup')
       except:
           pass
       
       try:
           if User.objects.get(email = email):
               messages.warning(request,"Email already exists")
               return redirect('/signup')
       except:
           pass
      
      
       user=User.objects.create_user(email,email,pass1)
       user.first_name = fname
       user.last_name = lname
       user.save()
       messages.success(request,"Signup success")
       return redirect("/login")
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":
        email =request.POST.get('email')
        pass1 =request.POST.get('pass1')
        user = authenticate(username=email,password=pass1) #user is the table
        if user is not None:
            login(request,user)
            messages.success(request,"Login Success")
            return redirect("/")
      #  Redirects the user to the home page or root URL of the website.


        else:
            messages.error(request,"Invalid Credentials Try again")
            return redirect("/login")
        #  Redirects the user to the login page.
        
        
        
        
    return render(request,"login.html")
    
    
def handlelogout(request):
            logout(request)
            messages.info(request,"Logout Success")
            return redirect("/login")
      #  Redirects the user to the home page or root URL of the website.


      
def search(request):
    query= request.GET['search']
    # print(query)
    if len(query)>100:
        allPosts=Blog.objects.none()
    else:
        allPostsTitle=Blog.objects.filter(title__icontains=query)
        allPostsDescription=Blog.objects.filter(description__icontains=query)
        allPosts=allPostsTitle.union(allPostsDescription)
    if allPosts.count()==0:
        messages.warning(request,f"No search result found......{query}")
        
    params={"data":allPosts}        
    return render(request,"search.html",params)      












