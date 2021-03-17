from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *

def registerPage(request):
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
                   
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
          
            return redirect('game:login')
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()	
    
    context = {'form':form, 'profile_form': profile_form}
    return render(request, 'game/register.html', context)



def loginPage(request):
    if request.user.is_authenticated:
	    return redirect('game:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('game:home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        
        context = {}
        return render(request, 'game/login.html', context)



def logoutUser(request):
	logout(request)
	return redirect('game:login')



@login_required(login_url='game:login')
def home(request):

    list_roles = Role.objects.filter(userprofile=request.user.userprofile)
    game_created = Game.objects.filter(admin=request.user.userprofile)
    context={'message': 'Welcome to the main Page', 'list_roles': list_roles, 'game_created': game_created, 'user': request.user.userprofile}
    return render(request, 'game/main.html', context)


@login_required(login_url='game:login')
def createGame(request):
    if request.method == "POST":
        form1 = GameCreationForm(request.POST)
        form2 = ExtendedGameCreationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            # get the data from the forms
            retailer = form2.cleaned_data.get("retailer")
            wholesaler = form2.cleaned_data.get("wholesaler")
            distributor = form2.cleaned_data.get("distributor")
            factory = form2.cleaned_data.get("factory")

            isDistributor = form1.cleaned_data['distributor_present']
            isWholesaler = form1.cleaned_data['wholesaler_present']
            startingInventory = form1.cleaned_data['starting_inventory']
            nrRounds = form1.cleaned_data['nr_rounds']


            # ## check for the errors
            # # check if we have selected more than specified
            if(isDistributor==False and distributor):
                messages.info(request, 'Distributor is not selected')
                return render(request, 'game/createGame.html', {})
            if(isWholesaler==False and wholesaler):
                messages.info(request, 'Wholesaler is not selected')
                return render(request, 'game/createGame.html', {})
            #check if the user has selected the same student for more than 1 role
            if(retailer == wholesaler or retailer == distributor or 
            retailer == factory or wholesaler==distributor or wholesaler == factory
            or distributor == factory):
                messages.info(request, 'A student can not have more than 1 role.')
                return render(request, 'game/createGame.html', {})
            


            # #if no errors than save the game, set the admin
            game = form1.save(commit = False)
            user31 = UserProfile.objects.get(user_id=request.user.id)
            game.admin = user31
            game.save()


            #create the respective roles
            r1 = r2 = r3 = r4 = None
            r1 = Role(role_name="retailer")
            r1.save()
            print(r1.id)
            if isDistributor:
                r2 = Role(role_name="distributor")
                r2.save()
                r1.upstream_player = r2.id
                r2.downstream_player = r1.id
            if isWholesaler:
                r3 = Role(role_name="wholesaler")
                r3.save()
                if isDistributor:
                    r2.upstream_player = r3.id
                    r3.downstream_player = r2.id
            r4 = Role(role_name="factory")
            r4.save()
            if isWholesaler:
                r4.downstream_player = r3.id
                r3.upstream_player = r4.id

            r1.save()
            if(r2): r2.save()
            if(r3): r3.save()
            r4.save()

            #add the roles to the userProfile and the game
            user1 = UserProfile.objects.get(user__pk=retailer.id)
            user1.roles.add(r1)
            user4 = UserProfile.objects.get(user__pk=factory.id)
            user4.roles.add(r4)
            game.roles.add(r1, r4)

            if r2 != None:
                user2 = UserProfile.objects.get(user__pk=distributor.id)
                user2.roles.add(r2)
                game.roles.add(r2)
            if r3 != None:
                user3 = UserProfile.objects.get(user__pk=wholesaler.id)
                user3.roles.add(r3)
                game.roles.add(r3)


            #create the weeks, with the respective times, number and starting inventory
            # and add them to the role
            for i in range(nrRounds):
                week1 = Week(date=timezone.now()+datetime.timedelta(weeks=i), number= i+1, inventory=startingInventory)
                week1.save()
                r1.weeks.add(week1)
                if(r2): 
                    week2 = Week(date=timezone.now()+datetime.timedelta(weeks=i), number= i+1, inventory=startingInventory)
                    week2.save()
                    r2.weeks.add(week2)
                if(r3): 
                    week3 = Week(date=timezone.now()+datetime.timedelta(weeks=i), number= i+1, inventory=startingInventory)
                    week3.save()
                    r3.weeks.add(week3)
                week4 = Week(date=timezone.now()+datetime.timedelta(weeks=i), number= i+1, inventory=startingInventory)
                week4.save()
                r4.weeks.add(week4)
    
            return HttpResponseRedirect(reverse('game:demand', args=(game.id,)))
    else:
        form2 = ExtendedGameCreationForm()
        form1 = GameCreationForm()	
    
    context = {'form1':form1, 'form2':form2}
    return render(request, 'game/createGame.html', context)


@login_required(login_url='game:login')
def createDemand(request, game_id):
    print("bbb")
    game = Game.objects.get(pk=game_id)
    if request.method == "POST":
        text = request.POST['demand']
        demands = text.split(", ")
        if len(demands) != game.nr_rounds:
            messages.info(request, 'You have not specified all rounds')
        
        k=1
        for customer_demand in demands:
            week1 = Week.objects.get(role__game=game, number=k, role__role_name="retailer")
            week1.demand = customer_demand
            week1.save()
            k+=1
        return redirect('game:home')

    context = {'game': game}
    return render(request, 'game/demandPattern.html', context)


@login_required(login_url='game:login')
def enterGame(request, role_id):
    context = {'message': 'You are at the game now', 'role_id': role_id}
    return render(request, 'game/enterGame.html', context)

