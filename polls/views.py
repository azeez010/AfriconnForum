from .form import PollForm
from .models import Poll, PollChoice, Voter
from root.models import Messages
from forum.models import Favourite 
from datetime import datetime, timedelta
from time import time
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
import json, os
from django.db.models import Q
from django.core.mail import send_mail
from django.core.paginator import Paginator
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your views here.
def create(request):
    if request.user.is_authenticated:
        User_id = request.user.id
    
    if request.method == "POST":
        poll = PollForm(request.POST, request.FILES)
        if poll.is_valid():
            poll = request.POST["poll"]
            choices = request.POST["choices"]
            slugTitle = poll.replace(" ", "-")
            date = request.POST["expiryDate"]
            expiryDate = time() + int(date)
            pollchoices = json.loads(choices)
            if "image" in request.FILES: 
                image = request.FILES["image"] 
            else:
                image = False
            if image:
                pollModel = Poll(user_id=User_id, slugTitle=slugTitle, title=poll, expiryDate=expiryDate, image=image)
                pollModel.save()
                for choice in pollchoices:
                    pollchoices = PollChoice(poll_id=pollModel.id, choice=choice["choice"])
                    pollchoices.save()
            
            else:
                pollModel = Poll(user_id=User_id, slugTitle=slugTitle, title=poll, expiryDate=expiryDate)
                pollModel.save()
                for choice in pollchoices:
                    pollchoices = PollChoice(poll_id=pollModel.id, choice=choice["choice"])
                    pollchoices.save()
                
            
            messages.success(request, "a poll has being created share this page for people to cast their votes")
            return redirect(f"/polls/poll/?title={pollModel.slugTitle}&value={pollModel.id}")
            
    context = {"poll": PollForm}
    return render(request, "polls/create.html", context)

def new(request):
    currentDate = time()
    expiredPolls = Poll.objects.filter(Q(expiryDate__lte=currentDate))
    expiredPolls.update(settled=True)
    newPolls = Poll.objects.filter(settled=False)          
    fav = Favourite.objects.all()
    
    hasPost = False
    if newPolls.count() < 1:
        hasPost = True
    

    page = request.GET.get('page', 1)
    paginator = Paginator(newPolls, 20)
    try:
        Polls = paginator.page(page)
    except PageNotAnInteger:
        Polls = paginator.page(1)
    except Emptyage:
        Polls = paginator.page(paginator.num_pages)
    
    context = {"newpolls": Polls, "hasPost": hasPost, "fav": fav }
    return render(request, "polls/new.html", context)


def your_polls(request):
    yourPolls = Poll.objects.filter(user_id = request.user.id).order_by("-expiryDate")          
    fav = Favourite.objects.all()
    
    hasPost = False
    if yourPolls.count() < 1:
        hasPost = True
    

    page = request.GET.get('page', 1)
    paginator = Paginator(yourPolls, 20)
    try:
        Polls = paginator.page(page)
    except PageNotAnInteger:
        Polls = paginator.page(1)
    except Emptyage:
        Polls = paginator.page(paginator.num_pages)
    
    context = {"newpolls": Polls, "hasPost": hasPost, "fav": fav }
    return render(request, "polls/your_polls.html", context)


def poll(request):
    poll_id=request.GET["value"]
    slug=request.GET["title"]
    poll = Poll.objects.get(id=poll_id)
    pollchoice = PollChoice.objects.filter(poll_id=poll_id)
    fav = Favourite.objects.filter(fav_thread__iregex='/polls/', user_id=request.user.id, title=poll.title, fav_id=poll.id )
    fav_bool = True if len(fav) > 0 else False
    context = {"poll": poll, "pollchoice": pollchoice, "fav_bool": fav_bool}
    return render(request, "polls/poll.html", context)

def vote(request):
    poll_id=request.GET["value"]
    slug=request.GET["title"]
    
    send_result = False
    if "sendResult" in request.POST:
        do_want_send_mail = request.POST['sendResult']
        send_result = True if do_want_send_mail == "on" else False
        
    choice = ""
    if choice in request.POST: 
        choice = request.POST['choice']
    
    voter = Voter.objects.filter(user_id=request.user.id, poll_id=poll_id)
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.pollchoice_set.get(pk=request.POST['choice'])
    except (KeyError, PollChoice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice")
        return redirect(f"/polls/poll/?title={slug}&value={poll_id}")
        
    else:
        if len(voter) > 0:
            print(voter)
            messages.error(request, f"You already voted for  {voter.first().choice}.")
            return redirect(f"/polls/poll/?title={slug}&value={poll_id}")
        
        voters = Voter(user_id=request.user.id, poll_id=poll_id, choice=selected_choice.choice, notify=send_result )
        voters.save()
        selected_choice.votes += 1
        selected_choice.save()
        
        messages.success(request, f"You have voted for {selected_choice.choice}")
        return redirect(f"/polls/poll/?title={slug}&value={poll_id}")
        
        
def results(request):
    pollsresult = Poll.objects.filter(settled=True)
    context = {"pollresult": pollsresult}
    return render(request, "polls/results.html", context)


def result(request):
    result_id=request.GET["value"]
    slug=request.GET["title"]
    pollresult = Poll.objects.filter(settled=True, id=result_id)
    
    check = Poll.objects.filter(settled=True, id=result_id, graph_made=False)
   
    if check.exists():
        all_voters = check.first().voter_set.all()
        for each_voter in all_voters:
            send_messages = Messages(sender_id=1, msg=f"The poll that you participated in has expired click below to check result<br><a class='tweet-color' href='/polls/poll/?title={each_voter.poll.slugTitle}&value={each_voter.poll.id}'>poll result</a>", receiver_id=each_voter.user_id, msg_type="poll expiry", receiver_seen=False)
            send_messages.save()
                
        
        poll_first_result = pollresult.first()
        choices = poll_first_result.pollchoice_set.all()
        
        choices_data = []
        get_choice_name = []
        
        for each_choice in choices:
            each_data = {each_choice.choice: each_choice.votes}
            choices_data.append(each_data)
            get_choice_name.append(each_choice.choice)
        
        df = pd.DataFrame(choices_data, index=get_choice_name) 
        #  visualise data
        df.plot(kind="bar", title=f"{poll_first_result.title}")
        output = BytesIO()
        # Resize/modify the image
        plt.savefig(output, format='png')
        output.seek(0)
        poll_first_result.graph = InMemoryUploadedFile(output, 'ImageField', f"{poll_first_result.title}-{poll_first_result.id}.png", 'image/png',
                                                    sys.getsizeof(output), None)
        poll_first_result.graph_made = True
        poll_first_result.save()
        
    context = {"pollresult": pollresult.first()}
    return render(request, "polls/result.html", context)

def search(request):
    if request.method == "GET":
        context = {"keyword": "None"}
        return render(request, "polls/search_poll.html", context)
    
    query = request.POST["search"]
    if query == "":
        # rregex manipulator i want no result
        query = "~#$%^!@#$&$*"
    polls = Poll.objects.filter(title__iregex=query)
    if len(polls) == 0:
        messages.error(request, "oops no result...")
        return redirect("/polls/search-poll/")

    
    page = request.GET.get('page', 1)
    paginator = Paginator(polls, 20)
    try:
        Polls = paginator.page(page)
    except PageNotAnInteger:
        Polls = paginator.page(1)
    except Emptyage:
        Polls = paginator.page(paginator.num_pages)
    
    context = {"searches": Polls, "keyword": query }
    return render(request, "polls/search_poll.html", context)
    