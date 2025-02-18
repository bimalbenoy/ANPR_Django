from django.shortcuts import render,get_object_or_404,redirect
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .running import process_video_file
from .databasecomp import  compare_license_plates
from .models import Residents,Logbook
from django.contrib import messages
from django.utils.timezone import now
from datetime import date, datetime




def index(request):
    return render(request, 'index.html')  
def animatedregister(request):
    return render(request, 'animatedregister.html') 
def registerveh(request):
    if request.method == "POST":
        owner_name = request.POST.get("ownerName")
        vehicle_number = request.POST.get("vehicleNumber")
        resident_address = request.POST.get("residentAddress")
        category = request.POST.get("category")

        
        if Residents.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "Vehicle Number already registered!")
            return redirect("registerveh")  

        
        Residents.objects.create(
            owner_name=owner_name,
            vehicle_number=vehicle_number,
            resident_address=resident_address,
            category=category,
            registered_at=now(),  
        )

        messages.success(request, "Vehicle registered successfully!")
        return redirect("registerveh")  

    return render(request, "registervehicle.html")  
def registerlogbook(request):
    if request.method == "POST":
        owner_name = request.POST.get("ownerName2")
        vehicle_number = request.POST.get("vehicleNumber2")
        resident_address = request.POST.get("residentAddress2")
        category = request.POST.get("category2")

        
        if Logbook.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "Vehicle Number already registered!")
            return redirect("registerlogbook")  

    
        Logbook.objects.create(
            owner_name=owner_name,
            vehicle_number=vehicle_number,
            resident_address=resident_address,
            category=category,
            registered_date=date.today(),
            registered_time=datetime.now().time()
        )

        messages.success(request, "Vehicle registered successfully!")
        return redirect("registerlogbook")  

    return render(request, "registerlogbook.html")  
def home1(request):
    return render(request, 'home1.html')
def logbook(request):
    vehicles=Logbook.objects.all()
    return render(request, 'logbook.html',{'vehicles':vehicles}) 
def gateopen(request):
    return render(request, 'approvegate.html')
def gateclose(request):
    return render(request, 'declinegate.html')  

def upload(request):
    if request.method=="POST":
        with open("tweet/car_plate_data.txt", "w") as file:
            file.write("")
        photo = request.FILES.get('photo')
        fs = FileSystemStorage(location='uploads/videos/')
        filename = fs.save(photo.name, photo)
        file_path = fs.path(filename)
        process_video_file(file_path)
        plates=compare_license_plates("tweet/car_plate_data.txt")
        
        for i in plates:
            resident = Residents.objects.filter(vehicle_number=i).first()
            if resident:

                Logbook.objects.create(
                owner_name=resident.owner_name,
                vehicle_number=resident.vehicle_number,
                resident_address=resident.resident_address,
                category=resident.category,
                registered_date=date.today(),
                registered_time=datetime.now().time()
                )
                return render(request,'approvegate.html',{'No':i})
        return render(request,'declinegate.html')   
                
            
            
        
        
        
    return render(request,'upload.html')

def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})
@login_required
def tweet_create(request):
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')

    else:
      form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})
def register(request): 
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

def tweet_search(request):
    if request.method=="POST":
        searched=request.POST['Searched']
        tweets=Tweet.objects.filter(text__contains=searched)

    else:
      pass
    return render(request,'search.html',{'searched':searched,'tweets':tweets})







    



