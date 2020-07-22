from django.shortcuts import render, redirect,get_object_or_404
from .forms import Registration,EditProfileForm,EditUserInformationForm  ,forms  
from validate_email import validate_email
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models  import User
from .models import Userinformation
from .models import Data
from datetime import date
from django.utils.timezone import now
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.forms.models import inlineformset_factory
from bs4 import BeautifulSoup
import requests
from datetime import time
from datetime import datetime
import datetime
import calendar
from django.urls import reverse




# Create your views here.

   


def home(request):
    context={'home':'active'}
    return render(request,'start.html',context)


def user_login(request):
    context={'login':'active'}
    if request.method=="POST":
        valuename=request.POST['name']
        valuepassword=request.POST['password']
        if '@'  not in valuename:
            if User.objects.filter(name=valuename).exists():
                pswcheck=User.objects.get(name=valuename).password
                if pswcheck==valuepassword:
                    username=User.objects.get(name=valuename).name
                    return redirect('profile',username)

                else:
                    messages.info(request,'Password didnot matched')
                    return render(request,'loginuser.html',context)
            else:
                messages.info(request,'Name didnot matched')
                return render(request,'loginuser.html',context)
            
            

        elif '@'  in valuename:
            if User.objects.filter(email=valuename).exists():
                pswcheck=User.objects.get(email=valuename).password
                if pswcheck==valuepassword:
                    username=User.objects.get(email=valuename).name
                    return redirect('profile',username)

                    
                else:
                    messages.info(request,'Password didnot matched')
                    return render(request,'loginuser.html',context)
            else:
                messages.info(request,'Email didnot matched')
                return render(request,'loginuser.html',context)
                  
    else:
        return render(request,'loginuser.html' ,context)


def signup(request):
    context={'signup':'active'}
    if request.method =='POST':
        fm=Registration(request.POST)
        valname=request.POST['name']
        valemail=request.POST['email']
        email_check=validate_email(valemail,verify=True)
        valpassword=request.POST['password']
        valpsw=request.POST['psw']

        if fm.is_valid():
            if len(valname)<3:
                messages.info(request,'Username is less than 3 charater')
                return render(request, 'signup.html',context)

            if User.objects.filter(name=valname).exists():
                messages.info(request,'Username already taken')
                return render(request,'signup.html',context)

            if '@' in valname:
                messages.info(request,'Username doesnot support @ ')
                return render(request,'signup.html',context)

            
            if len(valpassword)<4:
                messages.info(request,'Password is less than 4 charater')
                return render(request,'signup.html',context)

            if email_check==None:
                messages.info(request,'Email doesnot exists')
                return render(request,'signup.html',context)

            if User.objects.filter(email=valemail).exists():
                messages.info(request,'Email already taken')
                return render(request,'signup.html',context)


            if valpassword!=valpsw:
                messages.info(request,'Password not matched')
                return render(request,'signup.html',context)

            else:
                reg = User(name=valname,email=valemail,password=valpassword,psw=valpsw)
                reg.save()
                reger=Userinformation(user=reg)
                reger.save()
                con={'login':'active',
                     'infor':'You are registerd.Enter detail to get logged'}
                return redirect('/login/')

    else:
        return render(request,'signup.html',context)






def profile(request,username):
    userinfocollect=User.objects.get(name=username) 
    us=Userinformation.objects.get(user=userinfocollect.id)
    cont={'login':'active',
        'profile':'active',
        'data1':userinfocollect,
        'data2':us,
        'username':username}
    if request.method=='POST':
        us=Userinformation.objects.get(user=userinfocollect.id)
        if 'detailsubmit'  in request.POST:
            nc=request.POST['name']
            ec=request.POST['email']
            pc=request.POST['password']
            email_check=validate_email(ec,verify=True)
            
            if len(nc)<3:
                messages.info(request,'Username is less than 3 charater')
                return render(request, 'profile.html',cont)

            if User.objects.filter(name=nc).exclude(name=userinfocollect.name).exists():
                messages.info(request,'Username already taken')
                return render(request,'profile.html',cont)
            
            if '@' in nc:
                messages.info(request,'Username doesnot support @ ')
                return render(request,'profile.html',cont)

                
            if len(pc)<4:
                messages.info(request,'Password is less than 4 charater')
                return render(request,'profile.html',cont)

            if email_check==None:
                messages.info(request,'Email doesnot exists')
                return render(request,'profile.html',cont)

            if User.objects.filter(email=ec).exclude(email=userinfocollect.email).exists():
                messages.info(request,'Email already taken')
                return render(request,'profile.html',cont)

            else:
                reg = User(id=userinfocollect.id,name=nc,email=ec,password=pc,psw=pc)
                reg.save()
                return redirect('/login/')  

        if 'photosubmit' in request.POST:
            try:
                photo=request.FILES['image']
                regs=Userinformation(user=userinfocollect,image=photo,calculation_history=us.calculation_history,calculation_water=us.calculation_water,calculation_coffee=us.calculation_coffee,calculation_exercise=us.calculation_exercise,posted_date=us.posted_date)
                regs.save()
                us=Userinformation.objects.get(user=userinfocollect.id)
                conts=  {'login':'active',
                        'profile':'active',
                        'data1':userinfocollect,
                        'data2':us,
                        'username':username }
                return render(request,'profile.html',conts)  
            except MultiValueDictKeyError:
                messages.info(request,'Please Upload Image')
                return render(request,'profile.html',cont)

    else:
        return render(request,'profile.html',cont)

    



    
def calculate(request,username):
    userinfocollect=User.objects.get(name=username)
    us=Userinformation.objects.get(user=userinfocollect.id)
    if request.method=="POST":
        if 'foods' in request.POST:
            search=request.POST['foods']
            try:
                url=f"https://www.myfitnesspal.com/food/search?page=1&search={search}"
                req = requests.get(url)
                sor = BeautifulSoup(req.text,"html.parser")
                temp = sor.find("h1" ,class_="jss5").text
                gm = sor.find("div" , class_="jss9").text
                dat1=date.today()
                dat1=dat1.strftime("%d-%m-%Y")
                water=us.calculation_water
                coffee=us.calculation_coffee
                exercise=0
                dat2=water[0:10]
                dat3=coffee[0:10]
                if dat1==dat2:
                    glass=water[13:14]
                if dat1!=dat2:
                    glass=0
                if dat1==dat3:
                    cup=coffee[13:14]
                if dat1!=dat3:
                    cup=0
                contes={
                    'login':'active',
                'calculate':'active',
                'food':temp,
                'gm':gm,
                'water':glass,
                'coffee':cup,
                'exercise':exercise,
                'username':username
                }
                return render(request,'calculate.html',contes)
            except AttributeError:
                dat1=date.today()
                dat1=dat1.strftime("%d-%m-%Y")
                water=us.calculation_water
                coffee=us.calculation_coffee
                exercise=0
                dat2=water[0:10]
                dat3=coffee[0:10]
                if dat1==dat2:
                    glass=water[13:14]
                if dat1!=dat2:
                    glass=0
                if dat1==dat3:
                    cup=coffee[13:14]
                if dat1!=dat3:
                    cup=0
                contes={
                    'login':'active',
                'calculate':'active',
                'water':glass,
                'coffee':cup,
                'exercise':exercise,
                'username':username
                }
                messages.info(request,'Food not found')
                return render(request,'calculate.html',contes)


        if 'add' in request.POST:
            foodcal=(request.POST['foodcal'])
            amount=request.POST['amount']
            dt=date.today()
            dt=dt.strftime("%d-%m-%Y")
            cal=(f"{dt} : {foodcal}, {amount}")
            cal1=us.calculation_history
            cal=cal+'\n'+cal1
            regs=Userinformation(user=userinfocollect,image=us.image,calculation_history=cal,calculation_water=us.calculation_water,calculation_coffee=us.calculation_coffee,calculation_exercise=us.calculation_exercise,posted_date=us.posted_date)
            regs.save()
            water=us.calculation_water
            coffee=us.calculation_coffee
            dat2=water[0:10]
            dat3=coffee[0:10]
            if dt==dat2:
                glass=water[13:14]
            if dt!=dat2:
                glass=0
            if dt==dat3:
                cup=coffee[13:14]
            if dt!=dat3:
                cup=0
            food=0
            gm=0
            exercise=0
            infor={'info':'Added to your chart',
                    'login':'active',
                    'calculate':'active',
                    'water':glass,
                    'coffee':cup,
                    'food':food,
                    'gm':gm,
                    'calculate':'active',
                    'exercise':exercise,
                    'username':username
                     }
            return render(request,'calculate.html',infor)
        
            

        
        if 'water' in request.POST:
            water=us.calculation_water
            dtt1=date.today()
            dtt1=dtt1.strftime("%d-%m-%Y")
            coffee=us.calculation_coffee
            dat3=coffee[0:10]
            dtt2=water[0:10]
            food=0
            gm=0
            exercise=0
            if dtt1==dat3:
                cup=coffee[13:14]
            if dtt1!=dat3:
                cup=0
            if dtt1==dtt2:
                glass=water[13:14]
                glass=int(glass)+1
                water1=(f"{dtt1} : {glass}")
                water2=water.replace(water[0:14],water1)
                regs=Userinformation(user=userinfocollect,image=us.image,calculation_history=us.calculation_history,calculation_water=water2,calculation_coffee=us.calculation_coffee,calculation_exercise=us.calculation_exercise,posted_date=us.posted_date)
                regs.save()
                water={'water':glass,
                        'coffee':cup,
                        'food':food,
                        'gm':gm,
                        'calculate':'active',
                        'exercise':exercise,
                        'username':username }
                return render(request,'calculate.html',water)

            if dtt1!=dtt2:
                glass=1
                water1=(f"{dtt1} : {glass}")
                water2=water1+'\n'+water
                regs=Userinformation(user=userinfocollect,image=us.image,calculation_history=us.calculation_history,calculation_water=water2,calculation_coffee=us.calculation_coffee,calculation_exercise=us.calculation_exercise,posted_date=us.posted_date)
                regs.save()
                water={'water':glass,
                       'coffee':cup,
                       'food':food,
                       'gm':gm,
                       'calculate':'active',
                        'exercise':exercise,
                        'username':username }
                return render(request,'calculate.html',water)



        if 'cofe' in request.POST:
            cofe=us.calculation_coffee
            dtt1=date.today()
            dtt1=dtt1.strftime("%d-%m-%Y")
            water=us.calculation_water
            dat2=water[0:10]
            dtt2=cofe[0:10]
            food=0
            gm=0
            exercise=0
            if dtt1==dat2:
                glass=water[13:14]
            if dtt1!=dat2:
                glass=0
            if dtt1==dtt2:
                cup=cofe[13:14]
                cup=int(cup)+1
                cofe1=(f"{dtt1} : {cup}")
                cofe2=cofe.replace(cofe[0:14],cofe1)
                regs=Userinformation(user=userinfocollect,image=us.image,calculation_history=us.calculation_history,calculation_water=us.calculation_water,calculation_coffee=cofe2,calculation_exercise=us.calculation_exercise,posted_date=us.posted_date)
                regs.save()
                coffee={'coffee':cup,
                        'water':glass,
                        'food':food,
                        'gm':gm,
                        'calculate':'active',
                        'exercise':exercise,
                        'username':username }
                return render(request,'calculate.html',coffee)
            if dtt1!=dtt2:
                cup=1
                cofe1=(f"{dtt1} : {cup}")
                cofe2=cofe1+'\n'+cofe
                regs=Userinformation(user=userinfocollect,image=us.image,calculation_history=us.calculation_history,calculation_water=us.calculation_water,calculation_coffee=cofe2,calculation_exercise=us.calculation_exercise,posted_date=us.posted_date)
                regs.save()
                coffee={'coffee':cup,
                        'water':glass,
                        'food':food,
                        'gm':gm,
                        'calculate':'active',
                        'exercise':exercise,
                        'username':username }
                return render(request,'calculate.html',coffee)


        
        if 'exercise' in request.POST:
            exercise1=us.calculation_exercise
            exercise2=request.POST['exercise']
            time=request.POST['time']
            weight=request.POST['weight']
            time=''.join(x for x in time if x.isdigit())
            time=int(time)
            weight=''.join(x for x in weight if x.isdigit())
            weight=int(weight)
            dtt1=date.today()
            dtt1=dtt1.strftime("%d-%m-%Y")
            water=us.calculation_water
            coffee=us.calculation_coffee
            dat2=water[0:10]
            dat3=coffee[0:10]
            if dtt1==dat2:
                glass=water[13:14]
            if dtt1!=dat2:
                glass=0
            if dtt1==dat3:
                cup=coffee[13:14]
            if dtt1!=dat3:
                cup=0
            food=0
            gm=0  
            if time<10 or weight<10:
                messages.info(request,"Not valid data less than 10 ")
                burntcal=0
                contes={
                        'login':'active',
                        'calculate':'active',
                        'food':food,
                        'gm':gm,
                        'water':glass,
                        'coffee':cup,
                        'calculate':'active',
                        'exercise':burntcal,
                        'username':username
                        }
                return render(request,'calculate.html',contes)
                

            else:
                time1=time/10
                weigh1=weight/10
                calorie=Data.objects.get(exercise=exercise2).amount
                burntcal=calorie*weigh1*time1
                exercise3=(f"{dtt1} : {exercise2} {burntcal}")
                exercise4=exercise3+'\n'+ exercise1
                regs=Userinformation(user=userinfocollect,image=us.image,calculation_history=us.calculation_history,calculation_water=us.calculation_water,calculation_coffee=us.calculation_coffee,calculation_exercise=exercise4,posted_date=us.posted_date)
                regs.save()
                contes={
                        'login':'active',
                        'calculate':'active',
                        'food':food,
                        'gm':gm,
                        'water':glass,
                        'coffee':cup,
                        'calculate':'active',
                        'exercise':burntcal,
                        'exercisename':exercise2,
                        'username':username
                        }
                return render(request,'calculate.html',contes) 


    else:
        dat1=date.today()
        dat1=dat1.strftime("%d-%m-%Y")
        water=us.calculation_water
        coffee=us.calculation_coffee
        dat2=water[0:10]
        dat3=coffee[0:10]
        if dat1==dat2:
            glass=water[13:14]
        if dat1!=dat2:
            glass=0
        if dat1==dat3:
            cup=coffee[13:14]
        if dat1!=dat3:
            cup=0
        food=0
        gm=0
        exercise=0
        contes={
            'login':'active',
            'calculate':'active',
            'food':food,
            'gm':gm,
            'water':glass,
            'coffee':cup,
            'calculate':'active',
            'exercise':exercise,
            'username':username

        }
        return render(request,'calculate.html',contes)



def historyday(request,username):
    dtt=date.today()
    dtt=dtt.strftime("%d-%m-%Y")
    userinfocollect=User.objects.get(name=username)
    us=Userinformation.objects.get(user=userinfocollect.id)
    foodhistory=us.calculation_history
    waterhistory=us.calculation_water
    coffeehistory=us.calculation_coffee
    exercisehistory=us.calculation_exercise
    listfood=list(foodhistory.split('\n'))
    listwater=list(waterhistory.split('\n'))
    listcoffee=list(coffeehistory.split('\n'))
    listexercise=list(exercisehistory.split('\n'))
    datelistfood=[]
    datelistwater=[]
    datelistcoffee=[]
    datelistexercise=[]
    removelistfood=[]
    removelistwater=[]
    removelistcoffee=[]
    removelistexercise=[]
    foodlist=[]
    cal_list=[]
    waterlist=[]
    coffeelist=[]
    exercisenamelist=[]
    exercisecallist=[]
    ziplist1=[]
    ziplist2=[]
    ziplist3=[]
    ziplist4=[]
    for items in listfood:
        if items[0:10]==dtt:
            datelistfood.append(items[0:10])
            removelistfood=items.replace(items[0:12],'')
            removelistfood=removelistfood.split(',')
            foodlist.append(removelistfood[1])
            cal_list.append(removelistfood[0])
            ziplist1=zip(datelistfood,foodlist,cal_list)
        else:
            break


    for items in listwater:
        if items[0:10]==dtt:
            datelistwater.append(items[0:10])
            removelistwater=items.replace(items[0:12],'')
            removelistwater=list(removelistwater)
            waterlist.append(removelistwater[1])
            ziplist2=zip(datelistwater,waterlist)
        else:
            break


    for items in listcoffee:
        if items[0:10]==dtt:
            datelistcoffee.append(items[0:10])
            removelistcoffee=items.replace(items[0:12],'')
            removelistcoffee=list(removelistcoffee)
            coffeelist.append(removelistcoffee[1])
            ziplist3=zip(datelistcoffee,coffeelist)
        else:
            break

    
    for items in listexercise:
        if items[0:10]==dtt:
            datelistexercise.append(items[0:10])
            removelistexercise=items.replace(items[0:12],'')
            removelistexercise=removelistexercise.split(' ')
            exercisenamelist.append(removelistexercise[1])
            exercisecallist.append(removelistexercise[2])
            ziplist4=zip(datelistexercise,exercisenamelist,exercisecallist)

        else:
            break


    
    if ziplist1==[]:
        datelistfood=['No']
        foodlist=['Food consumed']
        cal_list=['Today']
        ziplist1=zip(datelistfood,foodlist,cal_list)

    if ziplist2==[]:
        datelistwater=['Not drank']
        waterlist=['water today']
        ziplist2=zip(datelistwater,waterlist)
    

    if ziplist3==[]:
        datelistcoffee=['No cup']
        coffeelist=['of caffiene ']
        ziplist3=zip(datelistcoffee,coffeelist)

    if ziplist4==[]:
        datelistexercise=['No']
        exercisenamelist=['Exercise']
        exercisecallist=['Today']
        ziplist4=zip(datelistexercise,exercisenamelist,exercisecallist)
    

    foodcal={'ziplist1':ziplist1,
              'ziplist2':ziplist2,
              'ziplist3':ziplist3,
              'ziplist4':ziplist4,
               'historyday':'active',
               'history':'active',
               'login':'active',
               'username':username}
    return render(request,'historyday.html',foodcal)   




def historyweek(request,username):
    week_day=datetime.datetime.now().isocalendar()[2]
    start_date=datetime.datetime.now() - datetime.timedelta(days=week_day)
    dates=[(start_date + datetime.timedelta(days=i)).date() for i in range(7)]
    userinfocollect=User.objects.get(name=username)
    us=Userinformation.objects.get(user=userinfocollect.id)
    foodhistory=us.calculation_history
    waterhistory=us.calculation_water
    coffeehistory=us.calculation_coffee
    exercisehistory=us.calculation_exercise
    listfood=list(foodhistory.split('\n'))
    listwater=list(waterhistory.split('\n'))
    listcoffee=list(coffeehistory.split('\n'))
    listexercise=list(exercisehistory.split('\n'))
    datelistfood=[]
    datelistwater=[]
    datelistcoffee=[]
    datelistexercise=[]
    removelistfood=[]
    removelistwater=[]
    removelistcoffee=[]
    removelistexercise=[]
    foodlist=[]
    cal_list=[]
    waterlist=[]
    coffeelist=[]
    exercisenamelist=[]
    exercisecallist=[]
    ziplist1=[]
    ziplist2=[]
    ziplist3=[]
    ziplist4=[]
    sumfood=0
    sumwater=0
    sumcoffee=0
    sumexercise=0
    sumcoffee=0
    sumexercise=0
    for dtt in dates:
        dtt=dtt.strftime("%d-%m-%Y")
        for items in listfood:
            if items[0:10]==dtt:
                datelistfood.append(items[0:10])
                removelistfood=items.replace(items[0:12],'')
                removelistfood=removelistfood.split(',')
                foodlist.append(removelistfood[1])
                cal_list.append(removelistfood[0])
                try:
                    sumfood=sumfood+int(''.join(x for x in removelistfood[0] if x.isdigit()))
                    ziplist1=zip(datelistfood,foodlist,cal_list)
                except ValueError:
                    sumfood=0
                    ziplist1=zip(datelistfood,foodlist,cal_list)


    for dtt in dates:
        dtt=dtt.strftime("%d-%m-%Y")
        for items in listwater:
            if items[0:10]==dtt:
                datelistwater.append(items[0:10])
                removelistwater=items.replace(items[0:12],'')
                removelistwater=list(removelistwater)
                waterlist.append(removelistwater[1])
                sumwater=sumwater+int(''.join(x for x in removelistwater[1] if x.isdigit()))
                ziplist2=zip(datelistwater,waterlist)
            

    for dtt in dates:
        dtt=dtt.strftime("%d-%m-%Y")
        for items in listcoffee:
            if items[0:10]==dtt:
                datelistcoffee.append(items[0:10])
                removelistcoffee=items.replace(items[0:12],'')
                removelistcoffee=list(removelistcoffee)
                coffeelist.append(removelistcoffee[1])
                sumcoffee=sumcoffee+int(''.join(x for x in removelistcoffee[1] if x.isdigit()))
                ziplist3=zip(datelistcoffee,coffeelist)
        

    for dtt in dates:
        dtt=dtt.strftime("%d-%m-%Y")
        for items in listexercise:
            if items[0:10]==dtt:
                datelistexercise.append(items[0:10])
                removelistexercise=items.replace(items[0:12],'')
                removelistexercise=removelistexercise.split(' ')
                exercisenamelist.append(removelistexercise[1])
                exercisecallist.append(removelistexercise[2])
                sumexercise=sumexercise+int(''.join(x for x in removelistexercise[2] if x.isdigit()))
                ziplist4=zip(datelistexercise,exercisenamelist,exercisecallist)

        


    
    if ziplist1==[]:
        datelistfood=['No']
        foodlist=['Food consumed']
        cal_list=['This week']
        ziplist1=zip(datelistfood,foodlist,cal_list)

    if ziplist2==[]:
        datelistwater=['Not drank']
        waterlist=['water ']
        ziplist2=zip(datelistwater,waterlist)
    

    if ziplist3==[]:
        datelistcoffee=['No cup']
        coffeelist=['of caffiene ']
        ziplist3=zip(datelistcoffee,coffeelist)

    if ziplist4==[]:
        datelistexercise=['No']
        exercisenamelist=['Exercise']
        exercisecallist=['This week']
        ziplist4=zip(datelistexercise,exercisenamelist,exercisecallist)
    

    foodcal={'ziplist1':ziplist1,
              'ziplist2':ziplist2,
              'ziplist3':ziplist3,
              'ziplist4':ziplist4,
              'sumfood':sumfood,
              'sumwater':sumwater,
              'sumcoffee':sumcoffee,
              'sumexercise':sumexercise/10,
               'historyday':'active',
               'history':'active',
               'login':'active',
               'username':username}
    return render(request,'historyweek.html',foodcal)   




def historymonth(request,username):
    userinfocollect=User.objects.get(name=username)
    us=Userinformation.objects.get(user=userinfocollect.id)
    foodhistory=us.calculation_history
    waterhistory=us.calculation_water
    coffeehistory=us.calculation_coffee
    exercisehistory=us.calculation_exercise
    listfood=list(foodhistory.split('\n'))
    listwater=list(waterhistory.split('\n'))
    listcoffee=list(coffeehistory.split('\n'))
    listexercise=list(exercisehistory.split('\n'))
    removelistfood=[]
    removelistwater=[]
    removelistcoffee=[]
    removelistexercise=[]
    monthlistfoodint=[]
    monthlistfoodname=[]
    monthlistwaterint=[]
    monthlistwatername=[]
    monthlistcoffeeint=[]
    monthlistcoffeename=[]
    monthlistexerciseint=[]
    monthlistexercisename=[]
    sumfoodlist=[]
    sumwaterlist=[]
    sumcoffeelist=[]
    sumexerciselist=[]
    yearlist1=[]
    yearlist2=[]
    yearlist3=[]
    yearlist4=[]
    ziplist1=[]
    ziplist2=[]
    ziplist3=[]
    ziplist4=[]
    sumfood=0
    sumwater=0
    sumcoffee=0
    sumexercise=0
    for items in listfood:
        if items=='':
            break
        else:
            monthinteger=int(items[3:5])
            monthlistfoodint.append(monthinteger)
    monthlistfoodint=set(monthlistfoodint)
    monthlistfoodint=list(monthlistfoodint)
    monthlistfoodint.sort(reverse=True)
    for mon in monthlistfoodint:
        for items in listfood:
            if items=='':
                pass
            elif int(items[3:5])==mon:
                removelistfood=items.replace(items[0:12],'')
                removelistfood=removelistfood.split(',')
                try:
                    sumfood=sumfood+int(''.join(x for x in removelistfood[0] if x.isdigit()))
                    year=items[6:10]
                    ziplist1=zip(monthlistfoodname,sumfoodlist,yearlist1)
                except ValueError:
                    sumfood=0
                    ziplist1=zip(monthlistfoodname,sumfoodlist,yearlist1)

        else:
            yearlist1.append(year)
            sumfoodlist.append(sumfood)
            sumfood=0
            year=0
            month = calendar.month_name[mon]
            monthlistfoodname.append(month)
            ziplist1=zip(monthlistfoodname,sumfoodlist,yearlist1)
        
                
    
    for items in listwater:
        if items=='':
            break
        else:
            monthinteger=int(items[3:5])
            monthlistwaterint.append(monthinteger)
    monthlistwaterint=set(monthlistwaterint)
    monthlistwaterint=list(monthlistwaterint)
    monthlistwaterint.sort(reverse=True)
    for mon in monthlistwaterint:
        for items in listwater:
            if items=='':
                pass
            elif int(items[3:5])==mon:
                removelistwater=items.replace(items[0:12],'')
                removelistwater=removelistwater.split(',')
                sumwater=sumwater+int(''.join(x for x in removelistwater[0] if x.isdigit()))
                year=items[6:10]
        else:
            yearlist2.append(year)
            sumwaterlist.append(sumwater)
            sumwater=0
            month = calendar.month_name[mon]
            monthlistwatername.append(month)
            ziplist2=zip(monthlistwatername,sumwaterlist,yearlist2)


    for items in listcoffee:
        if items=='':
            break
        else:
            monthinteger=int(items[3:5])
            monthlistcoffeeint.append(monthinteger)
    monthlistcoffeeint=set(monthlistcoffeeint)
    monthlistcoffeeint=list(monthlistcoffeeint)
    monthlistcoffeeint.sort(reverse=True)
    for mon in monthlistcoffeeint:
        for items in listcoffee:
            if items=='':
                pass
            elif int(items[3:5])==mon:
                removelistcoffee=items.replace(items[0:12],'')
                removelistcoffee=removelistcoffee.split(',')
                sumcoffee=sumcoffee+int(''.join(x for x in removelistcoffee[0] if x.isdigit()))
                year=items[6:10]
        else:
            yearlist3.append(year)
            sumcoffeelist.append(sumcoffee)
            sumcoffee=0
            month = calendar.month_name[mon]
            monthlistcoffeename.append(month)
            ziplist3=zip(monthlistcoffeename,sumcoffeelist,yearlist3)
        

    for items in listexercise:
        if items=='':
            break
        else:
            monthinteger=int(items[3:5])
            monthlistexerciseint.append(monthinteger)
    monthlistexerciseint=set(monthlistexerciseint)
    monthlistexerciseint=list(monthlistexerciseint)
    monthlistexerciseint.sort(reverse=True)
    for mon in monthlistexerciseint:
        for items in listexercise:
            if items=='':
                pass
            elif int(items[3:5])==mon:
                removelistexercise=items.replace(items[0:12],'')
                removelistexercise=removelistexercise.split(' ')
                sumexercise=sumexercise+int(''.join(x for x in removelistexercise[2] if x.isdigit()))
                year=items[6:10]
        else:
            yearlist4.append(year)
            sumexerciselist.append(sumexercise/10)
            sumexercise=0
            month = calendar.month_name[mon]
            monthlistexercisename.append(month)
            ziplist4=zip(monthlistexercisename,sumexerciselist,yearlist4)
        


    if ziplist1==[]:
        monthlistfoodname=['NO']
        sumfoodlist=['Count']
        yearlist1=['Calorie']
        ziplist1=zip(monthlistfoodname,sumfoodlist,yearlist1)

    if ziplist2==[]:
        monthlistwatername=['NO']
        sumwaterlist=[' Count']
        yearlist2=['Glass']
        ziplist2=zip(monthlistwatername,sumwaterlist,yearlist2)
    

    if ziplist3==[]:
        monthlistcoffeename=['No ']
        sumcoffeelist=['of caffiene ']
        yearlist3=['cup']
        ziplist3=zip(monthlistcoffeename,sumcoffeelist,yearlist3)

    if ziplist4==[]:
        monthlistexercisename=['NO']
        sumexerciselist=['Burned']
        yearlist4=['calorie']
        ziplist4=zip(monthlistexercisename,sumexerciselist,yearlist4)
    

    foodcal={'ziplist1':ziplist1,
              'ziplist2':ziplist2,
              'ziplist3':ziplist3,
              'ziplist4':ziplist4,
               'historymonth':'active',
               'history':'active',
               'login':'active',
               'username':username}
    return render(request,'historymonth.html',foodcal)   


    






        






       

    





