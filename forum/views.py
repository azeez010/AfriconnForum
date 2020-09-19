from django.shortcuts import render, redirect
from .forms import Register_user, create_comment, report, create_thread, create_thread_category 
from .models import Thread, Comment, like_dislike, Favourite, Category, Reply, Chat, ChatMessage, ThreadSeen, Report, Members, ReportThread, Homepage,waitingHomeThread
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from root.models import TransactionType, Messages, Advert, Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User 
from blog.models import Blog
from polls.models import Poll
from job.models import Job
from django.utils import timezone
from django.contrib import messages
import threading, re, datetime, json
from PIL import Image
from django.db.models import Q
from itertools import chain
from operator import itemgetter
from django.core import serializers
from time import time
from random import randint, choice, sample
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_deny

def generate_recommendation(title):
    recommend_list = []
    stop_words_list = ["a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder"]
    title_in_list = title.split(" ")   
    for each_word_in_list in title_in_list:
        if each_word_in_list.lower() not in stop_words_list:
            recommend_list.append(each_word_in_list)
    recommend_text = " ".join(recommend_list)  
    return recommend_text

def create_category(request):
    if request.method == "POST":
        check_community_price = TransactionType.objects.filter(activity="communities")
        community_cost = check_community_price.first().cost
        userProfile = Profile.objects.get(user_id=request.user.id)
        user_ADs = userProfile.afrika_deeds
        
        if len(check_community_price) > 0:
            if user_ADs < community_cost:
                messages.error(request, f"{request.user.username}, you don't have enough ADSs, you can earn them through referrals and being liked for now")
                return redirect("/forum/all-categories/")
            else:   
                form = create_thread_category(request.POST, request.FILES)
                    
                if form.is_valid():
                    creating_category = form.save(commit=False)
                    creating_category.created_by_id = request.user.id
                    creating_category.name_of_creator = request.user.username                    
                    creating_category.save()
                    
                    Members.objects.create(user_id=request.user.id, hamlet_id=creating_category.id, is_admin=True)
                    # deduct points from ADS
                    userProfile.afrika_deeds -= community_cost
                    userProfile.save()
                    # send message to the client
                    send_messages = Messages(sender_id=1, msg=f"<p style='color: green'>Your community titled <b>{form.cleaned_data['title']}</b> has being created, Make sure you stay true to your community</p>", receiver_id=request.user.id, msg_type="community created successfully", receiver_seen=False)
                    send_messages.save()
                    messages.success(request, f"you have successfully a community titled {form.cleaned_data['title']}")
                    return redirect(f"/forum/hamlet/{creating_category.title}/{creating_category.id}/")
                else:
                    messages.error(request, "Something went wrong")
                    return redirect("/forum/all-categories/")
        else:
            messages.error(request, "You are not allowed to create a community yet")
            return redirect("/forum/all-categories/")
       
    else:
        check_community_price = TransactionType.objects.filter(activity="communities")
        community_cost = check_community_price.first().cost
        userProfile = Profile.objects.get(user_id=request.user.id)
        user_ADs = userProfile.afrika_deeds

        context = {"form": create_thread_category, "warning": "you are currently not allow to create a community" }
        
        if len(check_community_price) > 0:
            context = {"form": create_thread_category, "community_cost": community_cost, "user_ADs": user_ADs }    
        
        return render(request, "forum/create_category.html", context) 


def register(request):
    if request.method == "POST":
        form = Register_user(request.POST)
        # check if email already exist
        email = request.POST["email"]
        check_mail = User.objects.filter(email=email)
        if len(check_mail):
            messages.error(request, "User(E-mail) already exists, kindly reset your password")
            return redirect("/forum/signup/")
        
        name = request.POST["username"]
        if form.is_valid():
            if "ref" in request.POST:
                ref = request.POST["ref"]
                try:
                    referral = User.objects.get(id=ref)    
                    referral.profile.afrika_deeds += 10
                    referral.save()
                    msg = f"Thank you for referring {name}, you have been rewarded with 10 ADs"
                    message_to_referral = Messages(sender_id=1, msg=msg, receiver_id=ref, msg_type="referral", receiver_seen=False)    
                    message_to_referral.save()
                except:
                    messages.error(request, "referer does not exist")
                    return redirect("/forum/signup")
            post_signup = form.save(commit=False)
            lower_name = post_signup.username.lower()
            post_signup.username = lower_name
            # save the changes
            post_signup.save()
            try:
                introductory_thread = Thread.objects.get(id=7)
                msg = f"Welcome to Africonn and thanks for joining this wonderful platform, the link below is the guide on how and why to use Africonn <br> <a class='tweet-color' href='/forum/thread/?hamlet={introductory_thread.thread_category.id}&slug={introductory_thread.threadSlug}&thread_no={introductory_thread.id}'>{introductory_thread.title}</a>"
                introduction_msg = Messages(sender_id=1, msg=msg, receiver_id=post_signup.id, msg_type="platform introduction", receiver_seen=False)    
                introduction_msg.save()
            except:
                print("no such thread exist")
            messages.success(request, "your account has been sucessfully created")
            return redirect("/login")
        else:
            messages.error(request, form.errors)
            return redirect("/forum/signup")
    else:
        if request.user.is_authenticated:
            messages.error(request, "you are already logged in")
            return redirect("/forum/home/")
        else:
            try:
                ref = request.GET["ref"]
                form = Register_user()
                context = {"form": form, "ref": ref}
                return render(request, "forum/signup.html", context) 
            except: 
                form = Register_user()
                context = {"form": form}
                return render(request, "forum/signup.html", context) 

    
def home(request):
        homeThreadAll = Homepage.objects.all()
        expiredThread = Homepage.objects.filter(Q(expiryDate__lte = time()))
        expired = len(expiredThread)
        waitingthread = waitingHomeThread.objects.all()[:expired]
    
        popular_categories_created = Category.objects.all().order_by("-no_of_member", "-no_of_thread" )[:5]
        
        # making trending threads
        trending_threads = Thread.objects.all().order_by("-last_comment_datetime", "-last_comment_length")[:10]
        
        if expired > 0:
            for each_waiting_thread in waitingthread:
                homethread = Homepage(user_id=each_waiting_thread.user_id, thread_id=each_waiting_thread.thread_id, expiryDate=each_waiting_thread.time + int(time()))
                homethread.save()
                each_waiting_thread.delete()
            
            expiredThread.delete()
            
        # reserialized ads from ads manager
        if request.user.id:
            serialized_ad = ads_manager("home", 3, request.user.id, request.user.profile.country)
        else:
            serialized_ad = ads_manager("home", 3, None, "all")
            
        page = request.GET.get('page', 1)
        paginator = Paginator(homeThreadAll, 15)
        try:
            homethread = paginator.page(page)
        except PageNotAnInteger:
            homethread = paginator.page(1)
        except Emptyage:
            homethread = paginator.page(paginator.num_pages)
        # this is for ads and promo
        all_members = Category.objects.all() 
        
        context = {"thread_post": homethread, 'serialized_ad': serialized_ad, "all_members": serializers.serialize("json", all_members), "popular_hamlets": popular_categories_created, "category": category, "serialized_ad": serialized_ad, "trending_threads": trending_threads }
        return render(request, "forum/home.html", context)
 
def allCategories(request):
    all_categories_created = Category.objects.all().order_by("-no_of_thread", "-no_of_member")
    
    page = request.GET.get('page', 1)
    paginator = Paginator(all_categories_created, 15)
    try:
        all_communities = paginator.page(page)
    except PageNotAnInteger:
        all_communities = paginator.page(1)
    except Emptyage:
        all_communities = paginator.page(paginator.num_pages)

    context = {"all_communities": all_communities}
    return render(request, "forum/allCategories.html", context)

def category(request, title, pk):
    all_members = Category.objects.all() 
    threads = Thread.objects.filter(thread_category_id=pk)
    category_title = "all"
    if len(threads) > 0:
        category_title = threads.first().thread_category.title
    
    if request.user.id:
        serialized_ad = ads_manager(category_title, 2, request.user.id, request.user.profile.country)
    else:
        serialized_ad = ads_manager(category_title, 2, None, "all")
        
    hamlet_details = Category.objects.filter(id=pk)
    check_if_are_you_a_member = Members.objects.filter(user_id=request.user.id, hamlet_id=pk)
    
    are_you_a_member = False
    if check_if_are_you_a_member.exists():
        are_you_a_member = True
    
    thread_post = threads.order_by("-datetime")
    page = request.GET.get('page', 1)
    paginator = Paginator(thread_post, 20)
    try:
        thread_paginator = paginator.page(page)
    except PageNotAnInteger:
        thread_paginator = paginator.page(1)
    except EmptyPage:
        thread_paginator = paginator.page(paginator.num_pages)

    context = {"thread_post": thread_paginator, "are_you_a_member": are_you_a_member, "hamlet_details": hamlet_details, "title": title, "hamletID": pk, "serialized_ad": serialized_ad, "all_members": serializers.serialize("json", all_members)}
    return render(request, "forum/threads.html", context)

def ads_manager(category, numba_of_ads, user_id, your_country):
    if category == "feeds":
        advert = Advert.objects.filter(advert_category__iregex=f'(feeds)|(all)', ad_country__iregex=f'({your_country})|(all)', approved=True)#.values("advert_title", "advert_details", "advert_url", "advert",'advert_category', 'ad_country')
        expiredAdvert = Advert.objects.filter(expiryDate__lte=time(), approved=True)
    
    elif category == "home":
        advert = Advert.objects.filter(advert_category__iregex=f'(home)|(all)', ad_country__iregex=f'({your_country})|(all)', approved=True)#.values("advert_title", "advert_details", "advert_url", "advert", 'ad_country', 'advert_category')
        expiredAdvert = Advert.objects.filter(expiryDate__lte=time(), approved=True)
    else:
        advert = Advert.objects.filter(advert_category__iregex=f'({category})|(all)', ad_country__iregex=f'({your_country})|(all)', approved=True)#.values("advert_title", "advert_details", "advert_url", "advert", 'ad_country', 'advert_category')
        expiredAdvert = Advert.objects.filter(expiryDate__lte=time(), approved=True)
   
    if not user_id:  
        # # selecting advert through random process
        random_ads = len(advert) - numba_of_ads
        if random_ads < 0:
            random_ads = 0 
        
        start = randint(0, random_ads)
        end = start + numba_of_ads
        advert = advert[start:end]
        
        # #this is not ideal it is to be change later
        for expired in expiredAdvert:
            send_messages = Messages(sender_id=1, msg=f"<p class='tweet-this'>Your ads has expired on {expired.ad_expirydatetime.strftime('%d %b %Y %I-%M%p')}</p>", receiver_id=expired.user_id, msg_type="ads expired", receiver_seen=False)
            send_messages.save() 
        
        expiredAdvert.delete()
        
        serialized_ad = []
        if len(advert) > 0:
            serialized_ad = advert
        
        shuffled_content = sample(serialized_ad, len(serialized_ad)) 
    
    else:
        users_category = Members.objects.filter(user_id=user_id)
        hamlet_u_re_not_part_of = []
        if len(users_category) > 0:
            pred_category = choice(users_category)
            recommended_hamlet = generate_recommendation(pred_category.description)
            string = recommended_hamlet.replace(" ", ")|(")
            # recommend nothing string if string is empty
            search = string
            if string != "":
                search = r"({})".format(string)
                hamlet_u_re_not_part_of = Members.objects.filter(~Q(user_id=user_id), description__iregex=r'{}'.format(search))               
        else:
            users_category = Members.objects.all()
            
            if len(users_category) > 0:
                pred_category = choice(users_category)
                recommended_hamlet = generate_recommendation(pred_category.description)
                string = recommended_hamlet.replace(" ", ")|(")
                # recommend nothing string if string is empty
                search = string
                if string != "":
                    search = r"({})".format(string)
                    hamlet_u_re_not_part_of = Members.objects.filter(~Q(user_id=user_id), description__iregex=r'{}'.format(search))
 
        # # selecting advert through random process
        random_ads = len(advert) - numba_of_ads
        if random_ads < 0:
            random_ads = 0 
        
        start = randint(0, random_ads)
        end = start + numba_of_ads
        advert = advert[start:end]
        
        # #this is not ideal it is to be change later
        for expired in expiredAdvert:
            send_messages = Messages(sender_id=1, msg=f"<p class='tweet-this'>Your ads has expired on {expired.ad_expirydatetime.strftime('%d %b %Y %I-%M%p')}</p>", receiver_id=expired.user_id, msg_type="ads expired", receiver_seen=False)
            send_messages.save() 
        
        expiredAdvert.delete()
        
        serialized_ad = []
        if len(advert) > 0:
            serialized_ad = advert
        
        hamlet_u_re_not_part_of_trimmed = hamlet_u_re_not_part_of[0:2]
        
        served_promo = [*serialized_ad, *hamlet_u_re_not_part_of_trimmed]
        
        shuffled_content = sample(served_promo, len(served_promo)) 
       
    return serializers.serialize("json", shuffled_content)

def create(request, hamletTitle, hamletID):
    if request.user.is_authenticated:
        User_id = request.user.id
    
    if request.method == "POST":
        thread = create_thread(request.POST, request.FILES)
        if thread.is_valid():
            title = thread.cleaned_data['title']                    
            slug = title.replace(" ", "-")
            image = thread.cleaned_data['image']
            details = thread.cleaned_data['details']
            recommendation_text = generate_recommendation(title)
            try:
                if image:
                    check_new_thread = Thread.objects.filter(title=title, user_id=User_id, details=details,  thread_category_id=hamletID)
                    if len(check_new_thread) == 0:
                        new_thread  = Thread(title=title, user_id=User_id, recommendation=recommendation_text, thread_category_id=hamletID, details=details, threadSlug=slug, image=image, category=thread_name)
                        new_thread.save()
                        update_category = Category.objects.get(id=hamletID)
                        update_category.no_of_thread = Thread.objects.filter(thread_category=hamletID).count()
                        update_category.save()
                else:
                    new_thread  = Thread(title=title, user_id=User_id, details=details, threadSlug=slug, recommendation=recommendation_text, thread_category_id=hamletID, datetime=timezone.now())
                    new_thread.save()
                    update_category = Category.objects.get(id=hamletID)
                    update_category.no_of_thread = Thread.objects.filter(thread_category=hamletID).count()
                    update_category.save()
            
            except Exception as e:
                print(e)
            
        
        return redirect(f"/forum/hamlet/{hamletTitle}/{hamletID}/")
    else:
        context = {"form": create_thread, "hamletTitle": hamletTitle, "hamletID": hamletID}
        return render(request, "forum/create.html", context)


def comment(request, thread_id):
    #user id
    if request.user.is_authenticated:
        User_id = request.user.id
    
        #get the category through the id
        thread = Thread.objects.get(pk=thread_id)
        if request.method == "POST":
            comment = create_comment(request.POST, request.FILES)
            if comment.is_valid():
                commentpost = comment.cleaned_data['comment']
                image = comment.cleaned_data['image']
                try:
                    if image:
                        new_comment = thread.comment_set.create(comment=commentpost, image=image, user_id=User_id, datetime=timezone.now(), thread_id=thread_id)
                        new_comment.save()
                        
                        # Update trending threading from comments
                        comments_of_the_thread = Comment.objects.filter(thread_id=thread_id)
                        # length of the comments
                        len_comments_of_the_thread = len(comments_of_the_thread)
                        #last comment
                        last_comments_of_the_thread = comments_of_the_thread.last().datetime
                        #us those information to update the thread
                        thread.last_comment_datetime = last_comments_of_the_thread
                        thread.last_comment_length =  len_comments_of_the_thread
                        thread.save()
                        
                        checkThread = ThreadSeen.objects.filter(thread_id=thread_id, user_id=User_id)
                        if len(checkThread) == 0:
                            threadUpdate = ThreadSeen(thread_id=thread_id, user_id=User_id, is_seen=False)
                            threadUpdate.save()
                        else:
                            ThreadSeen.objects.filter(thread_id=thread_id).update(is_seen=False)
                            
                            # making invites
                        invites = re.findall("@\w+", commentpost)
                        if invites:
                            for each_invite in invites:
                                invite = each_invite.replace("@", "")
                                receiver = User.objects.filter(username=invite)
                                if len(receiver) > 0:
                                    msg = f"<a href='/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }#{new_comment.id}'>{thread.title}</a><br><p class='tweet-color'>{commentpost}</p>"
                                
                                send_messages = Messages(sender_id=request.user.id, msg=msg, receiver_id=receiver.first().id, msg_type="mention", receiver_seen=False)
                                send_messages.save()
                        # updating timestamp
                        thread.datetime = timezone.now()
                        thread.save()
                            
                    else:
                        new_comment = thread.comment_set.create(comment=commentpost, user_id=User_id, datetime=timezone.now(), thread_id=thread_id)
                        new_comment.save()
                        
                        # Update trending threading from comments
                        comments_of_the_thread = Comment.objects.filter(thread_id=thread_id)
                        # length of the comments
                        len_comments_of_the_thread = len(comments_of_the_thread)
                        #last comment
                        last_comments_of_the_thread = comments_of_the_thread.last().datetime
                        #us those information to update the thread
                        thread.last_comment_datetime = last_comments_of_the_thread
                        thread.last_comment_length =  len_comments_of_the_thread
                        thread.save()
                        
                        # each thread that is commented on
                        checkThread = ThreadSeen.objects.filter(thread_id=thread_id, user_id=User_id)
                        if len(checkThread) == 0:
                            threadUpdate = ThreadSeen(thread_id=thread_id, user_id=User_id, is_seen=False)
                            threadUpdate.save()
                        else:
                            ThreadSeen.objects.filter(thread_id=thread_id).update(is_seen=False)
                        
                        # making invites
                        invites = re.findall("@\w+", commentpost)
                        if invites:
                            for each_invite in invites:
                                invite = each_invite.replace("@", "")
                                receiver = User.objects.filter(username=invite)
                                if len(receiver) > 0:
                                    msg = f"<a href='/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }/#{new_comment.id}'>{thread.title}</a><br>{commentpost}"
                                
                                send_messages = Messages(sender_id=request.user.id, msg=msg, receiver_id=receiver.first().id, msg_type="mention", receiver_seen=False)
                                send_messages.save()

                        # updating timestamp
                        thread.datetime = timezone.now()
                        thread.save()
                except Exception as e:
                    print(e)
            
            return redirect(f"/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }")
        else:
            context = {"form": create_comment, "thread_id": thread_id, "thread_name": thread.thread_category.id}# "comments": comments}
            return render(request, "forum/comment.html", context)
    else:
        return redirect("/login/")

def thread(request):
    thread_id = request.GET["thread_no"]
    hamletID = request.GET["hamlet"] 
    thread_slug = request.GET["slug"]
    thread_post = Thread.objects.get(pk=thread_id, threadSlug=thread_slug)
    category_title = thread_post.thread_category.title
    all_members = Category.objects.all()
    #increase the views count
    thread_post.views += 1
    thread_post.save()
    comments = Comment.objects.filter(thread_id=thread_id)
    
    home_transactionType = TransactionType.objects.filter(activity="home")
    
    fav = Favourite.objects.filter(fav_thread__iregex="/forum/", user_id=request.user.id, title=thread_post.title, fav_id=thread_post.id )
    fav_bool = True if len(fav) > 0 else False

    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 20)
    try:
        comment_paginator = paginator.page(page)
    except PageNotAnInteger:
        comment_paginator = paginator.page(1)
    except EmptyPage:
        comment_paginator = paginator.page(paginator.num_pages)
    


    if len(home_transactionType) == 0:
        home_cost = 5
    else:
        home_cost = home_transactionType.first().cost
    # Deplayig ads and promo for threads
    if request.user.id:
        serialized_ad = ads_manager(category_title, 2, request.user.id, request.user.profile.country)
    else:
        serialized_ad = ads_manager(category_title, 2, None, "all")
    
    # recommending thread similar by name
    thread_recommendation = thread_post.recommendation
    
    string = thread_recommendation.replace(" ", ")|(")
    # recommend nothing string if string is empty
    search = string
    if string != "":
        search = r"({})".format(string)
        
    recommend = Thread.objects.filter(~Q(id=thread_post.id), recommendation__iregex=r'{}'.format(search))
    recommendation = recommend.order_by("views")[0:5]
    
    likes_and_dislike = like_dislike.objects.filter(user_id = request.user.id)
   
    context = {"thread": thread_post, "serialized_ad": serialized_ad, "all_members": serializers.serialize("json", all_members), "fav_bool": fav_bool, "comments": comment_paginator, "home_cost": home_cost, "recommendations": recommendation}#, "landd": likes_and_dislike}
    return render(request, "forum/eachThread.html", context)

def update_thread(request, thread_id):
    if request.user.is_authenticated:
        User_id = request.user.id
    if request.method == "POST":
        thread = Thread.objects.get(id=thread_id)
        
    # check if user wrote the post
        if User_id != thread.user_id:
            messages.error(request, "you are not allow to edit this post")
            return redirect(f"/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }")
        else:
            update = create_thread(request.POST, request.FILES)
            if update.is_valid():
                title = update.cleaned_data['title']
                slug = title.replace(" ", "-")
                image = update.cleaned_data['image']
                details = update.cleaned_data['details']
                try:
                    if image:
                        thread.title=title
                        thread.image=image 
                        thread.threadSlug=slug 
                        thread.details=details
                        thread.user_id=User_id
                        thread.save()
                    else:
                        thread.title=title
                        thread.threadSlug=slug 
                        thread.details=details
                        thread.user_id=User_id
                        thread.save()
                
                except Exception as e:
                    print("error")
                
            return redirect(f"/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }")

class updateThread(UpdateView):
    model = Thread
    template_name = 'forum/update_thread.html'
    form_class = create_thread

class updateComment(UpdateView):
    model = Comment
    template_name = 'forum/update_comment.html'
    form_class = create_comment


def reportComment(request, comment_id):
    #user id
    if request.user.is_authenticated:
        User_id = request.user.id
    
    #get the category through the id
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        reportpost = report(request.POST)
        if reportpost.is_valid():
            reportText = reportpost.cleaned_data['report']
            reportChoice = reportpost.cleaned_data['report_type']
            try:
                checkReport = Report.objects.filter(comment=comment_id, reporter=User_id)
                if len(checkReport) == 0:
                    new_report = Report(comment_id=comment.id, report=reportText, rule_broken=reportChoice, reporter_id=request.user.id, report_time=timezone.now())
                    new_report.save()
                    msg = f"You have new report <a class='tweet-color' href='/profile/report/'>check here</a>"
                    message_to_referral = Messages(sender_id=request.user.id, msg=msg, receiver_id=1, msg_type="report", receiver_seen=False)    
                    message_to_referral.save()
                
                else:
                    messages.error(request, f"{request.user.username}, you have already reported")
                    return redirect(f"/forum/thread/?hamlet={ comment.thread.thread_category.title }&slug={ comment.thread.threadSlug }&thread_no={ comment.thread.id }")

            except Exception as e:
                print(e)
        
        messages.success(request, f"you have reported {comment.user.username} successfully action are being taken")
        return redirect(f"/forum/thread/?hamlet={ comment.thread.thread_category.title }&slug={ comment.thread.threadSlug }&thread_no={ comment.thread.id }")
    else:
        context = {"form": report, "comment_id": comment_id }
        return render(request, "forum/report.html", context)


def reportThread(request, thread_id):
    #user id
    if request.user.is_authenticated:
        User_id = request.user.id
    
    #get the category through the id
    thread = Thread.objects.get(pk=thread_id)
    if request.method == "POST":
        reportpost = report(request.POST)
        if reportpost.is_valid():
            reportText = reportpost.cleaned_data['report']
            reportChoice = reportpost.cleaned_data['report_type']
            try:
                checkReport = ReportThread.objects.filter(thread_id=thread_id, reporter=User_id)
                if len(checkReport) == 0:
                    new_report = ReportThread(thread_id=thread.id, report=reportText, rule_broken=reportChoice, reporter_id=request.user.id, report_time=timezone.now())
                    new_report.save()
                    msg = f"You have new report <a class='tweet-color' href='/profile/report/'>check here</a>"
                    message_to_referral = Messages(sender_id=request.user.id, msg=msg, receiver_id=1, msg_type="report", receiver_seen=False)    
                    message_to_referral.save()
                
                else:
                    messages.error(request, f"{request.user.username}, you have already reported")
                    return redirect(f"/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }")

            except Exception as e:
                print(e)
        
        messages.success(request, f"you have reported {thread.user.username} successfully action are being taken")
        return redirect(f"/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }")
    else:
        context = {"form": report, "thread_id": thread_id }
        return render(request, "forum/reportThread.html", context)



def update_comment(request, comment_id):
    if request.user.is_authenticated:
        User_id = request.user.id
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        thread = Thread.objects.get(id=comment.thread.id)
        # checking to see if user wrote the comment
        if User_id != comment.user.id:
            messages.error(request, "you are not allow to edit this post")
            return redirect(f"/forum/thread/{thread.thread_category.title}/{thread.threadSlug}/{thread.id}/update")
        else:
            update = create_comment(request.POST, request.FILES)
            if update.is_valid():
                commentText = update.cleaned_data['comment']
                image = update.cleaned_data['image']
                try:
                    if image:
                        comment.image=image 
                        comment.comment=commentText
                        comment.save()
                    else:
                        comment.image=image 
                        comment.comment=commentText
                        comment.save()
                except Exception as e:
                    print(e)
            return redirect(f"/forum/thread/?hamlet={ thread.thread_category.id }&slug={ thread.threadSlug }&thread_no={ thread.id }#{comment.id}")
            
def your_threads(request):
    user_id = request.GET["q"]
    user_name = request.GET["name"]
    your_posts = []
    threads = Thread.objects.filter(user_id=user_id).values("datetime", "title", "thread_category", "details", "views", "image", "user_id", "id",)
    polls = Poll.objects.filter(user_id=user_id).values("datetime", "title", "expiryDate", "slugTitle", "settled", "image", "user_id", "id",)
    jobs = Job.objects.filter(user_id=user_id).values("id", "address", "slugTitle", "name_of_company", "title", "category", "details", "jobImage", "datetime")
    blogs = Blog.objects.filter(user_id=user_id).values("datetime","tags", "slugTitle", "title", "category", "details", "image", "user_id", "id", "user")

    your_posts.append(threads)
    your_posts.append(polls)
    your_posts.append(blogs)
    your_posts.append(jobs)
    

    get_post_list = sorted(chain(*your_posts), key=itemgetter('datetime'), reverse=True)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(get_post_list, 15)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {"all_posts": posts, "poster_name": user_name, "poster_id": user_id}
    return render(request, "forum/your_threads.html", context)
        
#push thread  to home page
def push(request):
    thread_id = request.GET["thread"]
    User_id = request.user.id
    ADs = User.objects.get(id=User_id)
    all_home_threads = Homepage.objects.all()
    home_transactionType = TransactionType.objects.filter(activity="home")
    
    if len(home_transactionType) == 0:
        home_cost = 5
    else:
        home_cost = home_transactionType.first().cost

    ADs = User.objects.get(id=User_id)
    check_homepage = Homepage.objects.filter(thread_id=thread_id)
    check_waiting = waitingHomeThread.objects.filter(thread_id=thread_id)
    
    #checking to see if there are enough points 
    if ADs.profile.afrika_deeds < home_cost:
        messages.error(request, f"{ADs.username}, you do not have {home_cost} ADs to push to the front page")
        return redirect("/forum/home/") 
    
    if len(check_homepage) > 0:
        messages.error(request, f"{ADs.username}, your thread is already on the homepage")
        return redirect("/forum/home/") 
    
    if len(check_waiting) > 0:
        messages.error(request, f"{ADs.username}, your thread is on the waiting threads and will be added as soon as possible ")
        return redirect("/forum/home/") 

    elif len(all_home_threads) > 29:
        waitingThread = waitingHomeThread(user_id=User_id, thread_id=thread_id, time=86400)
        waitingThread.save()
        # deducting ADs
        ADs = User.objects.get(id=User_id)
        ADs.profile.afrika_deeds -= home_cost
        ADs.save()
        # redirecting to ?
        messages.success(request, f"{ADs.username}, your thread has been added to waiting listing and would be added to the home as soon as their is free space")
        return redirect("/forum/home/") 
    else:
        expiryDate = int(time()) + 86400
        homethread = Homepage(user_id=User_id, thread_id=thread_id, expiryDate=expiryDate)
        homethread.save()
        # deducting ADs
        ADs.profile.afrika_deeds -= home_cost
        ADs.save()
        messages.success(request, f"{ADs.username}, you have pushed your thread to the home page successfully")
        return redirect("/forum/home/")            
    
def get_messages(request):
    message = Messages.objects.filter(receiver_id=request.user.id).order_by("-time")
    # for highlight new messages, The new message won't happen until i loop and i don't know why
    for new_message in message:
        break
    # update after the context has been set
    hasPost = False
    if message.count() < 1:
        hasPost = True
    page = request.GET.get('page', 1)
    paginator = Paginator(message, 20)
    try:
        msg = paginator.page(page)
    except PageNotAnInteger:
        msg = paginator.page(1)
    except EmptyPage:
        msg = paginator.page(paginator.num_pages)

    context =  { "msgs": msg }
    seen = Messages.objects.filter(receiver_seen=False, receiver_id=request.user.id)
    seen.update(receiver_seen=True)
    return render(request, "forum/messages.html", context)

def get_replies(request):
    reply = Reply.objects.filter(receiver_id=request.user.id, you_send=False).order_by("-datetime")
    # for highlight new replys, The new reply won't happen until i loop and i don't know why
    for new_reply in reply:
        break
    # update after the context has been set
    context =  { "replies": reply }
    seen = Reply.objects.filter(is_seen=False, receiver_id=request.user.id)
    seen.update(is_seen=True)
    return render(request, "forum/reply.html", context)

def get_new_threads_comment(request):
    new_comments = ThreadSeen.objects.filter(user_id=request.user.id)#is_seen=False)
     # for highlight new replys, The new reply won't happen until i loop and i don't know why
    for new_comment in new_comments:
        break
    # update after the context has been set
    context =  { "Thread": new_comments }
    updateThreadComment = ThreadSeen.objects.filter(user_id=request.user.id) 
    updateThreadComment.update(is_seen=True)
    return render(request, "forum/thread_comments.html", context)


def search_forum(request):
    if request.method == "GET":
        context = {"keyword": "None"}
        return render(request, "forum/search_forum.html", context)
    
    query = request.POST["search"]
    if query == "":
        # rregex manipulator i want no result
        messages.error(request, "oops no result...")
        return redirect("/forum/search-forum/")
    
    threads = Thread.objects.filter(title__iregex=query).values("datetime", "title", "thread_category", "details", "views", "image", "user_id", "id",)
    comments = Comment.objects.filter(comment__iregex=query).values("id", "comment", "thread_id", "datetime")
    
    search = sorted(chain(threads, comments), key=itemgetter('datetime'), reverse=True)
    search_user = User.objects.filter(username__iregex=query)
    if len(threads) == 0 and len(comments) == 0 and len(search_user) == 0 :
        messages.error(request, "oops no result...")
        return redirect("/forum/search-forum/")
          
    context = {"searches": search, "keyword": query, "search_user": search_user }
    return render(request, "forum/search_forum.html", context)
    


def search(request):
    if request.method == "POST":
        keyword = request.POST["search"]
        if keyword == "":
            messages.error(request, "enter something...")
            return redirect("/forum/search-forum/")
        pattern = keyword.replace(" ", "|")
        blog = Blog.objects.filter(title__iregex=pattern).values("datetime", "title", "category", "details", "views", "image")
        forum = Thread.objects.filter(title__iregex=pattern).values("datetime", "title", "thread_category", "details", "views", "image")
        polls = Poll.objects.filter(title__iregex=pattern)
        jobs = Job.objects.filter(title__iregex=pattern).values("datetime", "title", "category", "details")
        res = sorted(chain(blog, jobs, forum), key=itemgetter('datetime'))
        if len(res) == 0:
            messages.error(request, "oops no result...")
            return redirect("/forum/search-forum/")
        else:
            context = {"searches": res, "keyword":keyword}
            return render(request, "forum/searchAll.html", context)
    else:
        context = {"searches": [], "keyword":""}
        return render(request, "forum/searchAll.html", context)

def chat(request, other_person_id):
    chats = []
    
    your_chats = Chat.objects.filter(chat_sender=request.user.id, chat_receiver=other_person_id)
    if your_chats.exists():
        messages = ChatMessage.objects.filter(chat_id=your_chats.first().id).values("sort", "datetime", "who_send", "message" )
        chats.append(messages)
        
    other_person_chat  = Chat.objects.filter(chat_sender=other_person_id, chat_receiver=request.user.id)
    if other_person_chat .exists():
        messages = ChatMessage.objects.filter(chat_id=other_person_chat .first().id).values("sort", "datetime", "who_send", "message" )
        chats.append(messages)
    other_person_details = User.objects.get(id=other_person_id)
    
    chat_chained = sorted(chain(*chats), key=itemgetter('sort'))
    context = {"chat_list": chat_chained, "other_person":  other_person_details }
    return render(request, "forum/chat.html", context)
    

def chat_list(request):
    all_chats = Chat.objects.filter(chat_sender=request.user.id)
    context = {"all_chats": all_chats }
    return render(request, "forum/chat-list.html", context)
    
def hamlet_list(request, user_id):
    hamlets = Members.objects.filter(user_id=user_id)
    user = User.objects.get(id=user_id)
    context = {"hamlets": hamlets,  "username": user.username }
    return render(request, "forum/your_hamlet.html", context)

class updateCategory(UpdateView):
    model = Category
    template_name = 'forum/update_category.html'
    form_class = create_thread_category

