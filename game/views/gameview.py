from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import datetime
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from game.models import *
from game.forms import *



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
            


            # #if no errors than save the game, set the admin
            game = form1.save(commit = False)
            user31 = UserProfile.objects.get(user_id=request.user.id)
            game.admin = user31
            game.save()


            #create the respective roles and specify the relationship between them
            r1 = r2 = r3 = r4 = None
            
            r1 = Role(role_name="retailer")
            r1.save()
            r4 = Role(role_name="factory")
            r4.save()
            if isWholesaler:
                r2 = Role(role_name="wholesaler")
                r2.save()
                r2.downstream_player = r1.id
                r1.upstream_player = r2.id
                if isDistributor:
                    r3 = Role(role_name="distributor")
                    r3.save()
                    r3.downstream_player = r2.id
                    r2.upstream_player = r3.id
                    r4.downstream_player = r3.id
                    r3.upstream_player = r4.id
                else:
                    r4.downstream_player = r2.id
                    r2.upstream_player = r4.id
            else:
                if isDistributor:
                    r3 = Role(role_name="distributor")
                    r3.save()
                    r3.downstream_player = r1.id
                    r1.upstream_player = r3.id
                    r3.upstream_player = r4.id
                    r4.downstream_player = r3.id
                else:
                    r1.upstream_player = r4.id
                    r4.downstream_player = r1.id
            
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
                user2 = UserProfile.objects.get(user__pk=wholesaler.id)
                user2.roles.add(r2)
                game.roles.add(r2)
            if r3 != None:
                user3 = UserProfile.objects.get(user__pk=distributor.id)
                user3.roles.add(r3)
                game.roles.add(r3)


            #create the weeks, with the respective times, number and starting inventory
            # and add them to the role
            for i in range(nrRounds):
                week1 = Week(date=timezone.now()+datetime.timedelta(minutes=i*3), number= i+1, inventory=startingInventory)
                week1.save()
                r1.weeks.add(week1)
                if(r2): 
                    week2 = Week(date=timezone.now()+datetime.timedelta(minutes=i*3), number= i+1, inventory=startingInventory)
                    week2.save()
                    r2.weeks.add(week2)
                if(r3): 
                    week3 = Week(date=timezone.now()+datetime.timedelta(minutes=i*3), number= i+1, inventory=startingInventory)
                    week3.save()
                    r3.weeks.add(week3)
                week4 = Week(date=timezone.now()+datetime.timedelta(minutes=i*3), number= i+1, inventory=startingInventory)
                week4.save()
                r4.weeks.add(week4)
    
            return HttpResponseRedirect(reverse('game:demand', args=(game.id,)))
    else:
        form2 = ExtendedGameCreationForm()
        form1 = GameCreationForm()	
    
    context = {'form1':form1, 'form2':form2, 'user': request.user.userprofile}
    return render(request, 'game/createGame.html', context)


@login_required(login_url='game:login')
def createDemand(request, game_id):
    game = Game.objects.get(pk=game_id)
    if request.method == "POST":
        text = request.POST['demand']
        demands = text.split(", ")
        if len(demands) != game.nr_rounds:
            messages.info(request, 'You have not specified all rounds')
            return HttpResponseRedirect(reverse('game:demand', args=(game_id,)))
        
        k=1
        for customer_demand in demands:
            week1 = Week.objects.get(role__game=game, number=k, role__role_name="retailer")
            week1.demand = customer_demand
            week1.save()
            k+=1
        return redirect('game:home')

    context = {'game': game, 'user': request.user.userprofile}
    return render(request, 'game/demandPattern.html', context)

@login_required(login_url='game:login')
def deleteGame(request, game_id):
    # delete all the related roles, weeks related to the game
    game = Game.objects.get(pk=game_id)
    roles = Role.objects.filter(game__id = game_id)
    
    for role in roles:
        weeks = Week.objects.filter(role__id=role.id)
        for week in weeks:
            week.delete()
        role.delete()
    game.delete()
    return redirect('game:home')


@login_required(login_url='game:login')
def updateGame(request, game_id):
    # delete all the related roles, weeks related to the game
    game = Game.objects.get(pk=game_id)
    roles = Role.objects.filter(game__id = game_id)
    
    for role in roles:
        weeks = Week.objects.filter(role__id=role.id)
        for week in weeks:
            week.delete()
        role.delete()
    game.delete()
    return redirect('game:home')