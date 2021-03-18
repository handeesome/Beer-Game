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
    for role in list_roles:
        print(role.role_name)
    game_created = Game.objects.filter(admin=request.user.userprofile)
    context={'message': 'Welcome to the main Page', 'list_roles': list_roles, 'game_created': game_created, 'user': request.user.userprofile}
    return render(request, 'game/main.html', context)

@login_required(login_url='game:login')
def home(request):
    game_created = Game.objects.filter(admin=request.user.userprofile)
    context={'game_created': game_created, 'user': request.user.userprofile}
    return render(request, 'game/main.html', context)

def assignedGames(request):
    list_roles = Role.objects.filter(userprofile=request.user.userprofile)
    for role in list_roles:
        print(role.role_name)

    context={'list_roles': list_roles, 'user': request.user.userprofile}
    return render(request, 'game/assignedGames.html', context)


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
                r2 = Role(role_name="wholesaler")
                r2.save()
                r1.upstream_player = r2.id
                r2.downstream_player = r1.id
            if isWholesaler:
                r3 = Role(role_name="distributor")
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
        
        k=1
        for customer_demand in demands:
            week1 = Week.objects.get(role__game=game, number=k, role__role_name="retailer")
            week1.demand = customer_demand
            week1.save()
            k+=1
        return redirect('game:home')

    context = {'game': game, 'user': request.user.userprofile}
    return render(request, 'game/demandPattern.html', context)


# helper function for constructing the graph
def return_graph(last_weeks, dataType):
    inventories = []
    demands = []
    incoming_shipments = []
    outgoing_shipments = []
    orders = []
    weeknr = []
    if(dataType == 'inventory'):
        i = 0
        for week in last_weeks:
            inventories.append(week.inventory-week.backlog)
            i+=1
            weeknr.append(i)
        fig = plt.figure()
        plt.ylabel('Inventory')
        # plt.xlabel('Week Nr')
        plt.title('Inventory')
        plt.plot(weeknr,inventories)
    elif dataType == 'demand':
        i = 0
        for week in last_weeks:
            demands.append(week.demand)
            i+=1
            weeknr.append(i)
        fig = plt.figure()
        plt.ylabel('Demand')
        # plt.xlabel('Week Nr')
        plt.title('Demand')
        plt.plot(weeknr,demands)
    elif dataType == 'incoming_shipment':
        i = 0
        for week in last_weeks:
            incoming_shipments.append(week.incoming_shipment)
            i+=1
            weeknr.append(i)
        fig = plt.figure()
        plt.ylabel('Incoming Shipment')
        # plt.xlabel('Week Nr')
        plt.title('Incoming Shipment')
        plt.plot(weeknr,incoming_shipments)
    elif dataType == 'outgoing_shipment':
        i = 0
        for week in last_weeks:
            outgoing_shipments.append(week.outgoing_shipment)
            i+=1
            weeknr.append(i)
        fig = plt.figure()
        plt.ylabel('Outgoing Shipment')
        # plt.xlabel('Week Nr')
        plt.title('Outgoing Shipment')
        plt.plot(weeknr,outgoing_shipments)
    elif dataType == 'order':
        i = 0
        for week in last_weeks:
            orders.append(week.order_placed)
            i+=1
            weeknr.append(i)
        fig = plt.figure()
        plt.ylabel('Order')
        # plt.xlabel('Week Nr')
        plt.title('Order')
        plt.plot(weeknr,orders)
    else:
        i = 0
        for week in last_weeks:
            outgoing_shipments.append(week.outgoing_shipment)
            demands.append(week.demand)
            incoming_shipments.append(week.incoming_shipment)
            inventories.append(week.inventory-week.backlog)
            orders.append(week.order_placed)
            i+=1
            weeknr.append(i)
        fig = plt.figure()
        # plt.xlabel('Week Nr')
        
        plt.plot(weeknr,inventories, label='Inventory')
        plt.plot(weeknr,outgoing_shipments, label = 'Outgoing Shipment')
        plt.plot(weeknr,demands, label= 'Demand')
        plt.plot(weeknr,incoming_shipments, label = 'Incoming Shipment')
        plt.plot(weeknr,orders, label = 'Orders')
        legend = plt.legend(loc='upper center', shadow=True)

    

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data



@login_required(login_url='game:login')
def enterGame(request, role_id):
    message = 'Welcome to the game'
    completed = False
    role = Role.objects.get(pk=role_id)
    upstream_role = '' 
    downstream_role = ''
    game= Game.objects.get(roles__id=role_id)
    current_week_up = False
    current_week_down = False

    last_weeks = Week.objects.filter(date__lte=timezone.now(), role__id=role_id).order_by('-date')[:11]
    # last_weeks = Week.objects.filter(role__id=role_id).order_by('date')[:10]
    current_week_role = last_weeks[0]
    last_weeks = Week.objects.filter(number__lt=current_week_role.number, role__id = role_id).order_by('date')[:10]
    game.rounds_completed = current_week_role.number
    if(game.is_completed):
        message = 'Game completed'
        completed = True
    #find whether other player have ordered in this current round
    other_weeks = Week.objects.filter(role__game=game, number=current_week_role.number).exclude(role__id = role_id).order_by('id')

    #check whether the role is factory
    if(role.upstream_player != 0):
        upstream_role = Role.objects.get(pk=role.upstream_player)
        current_week_up = Week.objects.filter(number=current_week_role.number, role__id=upstream_role.id)
    else:
        upstream_role = 'Brewery'
    
    #check whether the role is retailer
    if(role.downstream_player != 0):
        downstream_role = Role.objects.get(pk=role.downstream_player)
        current_week_down = Week.objects.filter(number=current_week_role.number, role__id=downstream_role.id)
    else:
        downstream_role='Consumer'



    # fig = go.Figure(
    #     data=[go.Bar(y=[10, 20, 40])],
    #     layout_title_text="Native Plotly rendering in Dash"
    # )
    # graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")


    if request.method == "POST":
        if(game.rounds_completed >= game.nr_rounds):
            game.is_completed = True
            game.save()
            return redirect('game:home')
        #some data taken from the game
        holding_cost = game.holding_cost
        backlog_cost = game.backlog_cost
        info_delay = game.info_delay
        order_placed = request.POST['order_placed']


        #calculating all the neccessary attributes for this current week
        total_requirements = current_week_role.demand + current_week_role.backlog
        total_available = current_week_role.inventory + current_week_role.incoming_shipment

        new_inventory = total_available - total_requirements
        new_backlog = 0
        if new_inventory < 0:
            new_backlog = abs(new_inventory)
            new_inventory = 0
            outgoing_shipment = total_available
        else:
            outgoing_shipment = total_requirements
        
        current_cost = current_week_role.cost + new_inventory * holding_cost + new_backlog*backlog_cost
        
        #saving all missing attributes to the corresponding week
        current_week_role.order_placed = order_placed
        current_week_role.inventory = new_inventory
        current_week_role.backlog = new_backlog
        current_week_role.outgoing_shipment = outgoing_shipment
        current_week_role.cost = current_cost
        current_week_role.save()


        #updating the attributes of the next week of the corresponding role according to the info obtained
        if(current_week_role.number+1 < game.nr_rounds):
            next_week = Week.objects.get(role__id=role_id, number=current_week_role.number+1)
            if(next_week):
                next_week.inventory = new_inventory
                next_week.backlog = new_backlog
                next_week.cost = current_cost
                next_week.save()
        
        
        #updating the attributes of the (future) weeks of other roles according to the 
        #corresponding relationship (upstream, downstream) and the info_delay
        
        if(current_week_role.number+info_delay < game.nr_rounds):   
            #1 and the order placed by the user, which will become the demand to the upstream player after info_delay  
            if(current_week_up):
                #not a factory
                #find the week of the upstream player, when the demand with arrive
                future_week_up = Week.objects.get(role= upstream_role, number=current_week_role.number+info_delay)
                if(future_week_up):
                    future_week_up.demand = order_placed
                    future_week_up.save()
            else:
                #factory, we will just update the week entity corresponding to the time after 2 weeks (1 + 1)
                #it does not rely on the info_delay
                future_week_role = Week.objects.get(role__id = role_id, number = current_week_role.number + 2)
                if(future_week_role):
                    future_week_role.incoming_shipment = order_placed
                    future_week_role.save()

            #2 and the outgoing shipment of the user, which will become the incoming shipment of the downstream player
            if(current_week_down):
                #not a retailer
                future_week_down = Week.objects.get(role=downstream_role, number = current_week_role.number+info_delay)
                if(future_week_down):
                    future_week_down.incoming_shipment = outgoing_shipment
                    future_week_down.save()

        game.save()
        return redirect('game:home')

    
    context = {'message': message, 'completed': completed, 'role': role, 'upstream_role':upstream_role, 
    'downstream_role': downstream_role,'last_weeks':last_weeks, 'current_week_role': current_week_role,
    'other_weeks': other_weeks,'game': game, 'graph1': return_graph(last_weeks, 'inventory')
    , 'graph2': return_graph(last_weeks, 'demand'), 'graph3': return_graph(last_weeks, 'incoming_shipment'), 
    'graph4': return_graph(last_weeks, 'outgoing_shipment'), 'graph5': return_graph(last_weeks, 'order'), 
    'graph6': return_graph(last_weeks, 'all')
    # 'graph_div': graph_div
    }
    return render(request, 'game/enterGame.html', context)


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