# Create your views here.
import re
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import create_job, ResumeForm
from .models import Applicant, Job, AlreadyApplied
from root.models import Profile, Messages
from forum.models import Favourite
from django.views.generic import UpdateView
from django.utils import timezone
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags    

# from django.contrib.admin.decorators import login_required
def home(request):
    getJob = Job.objects.filter(fulfilled=False).order_by("-datetime")[0:10]
    fav = Favourite.objects.all()
    context = {"getJob": getJob, "fav": fav }
    return render(request, "job/home.html", context) 

def update_job(request, pk):
    if request.method == "POST":
        job = Job.objects.get(id=pk)
        jobForm = create_job(request.POST, request.FILES, instance=job)
        if jobForm.is_valid():
            jobForm.save()
        
        messages.success(request, "updated successfully")
        return redirect(f"/jobs/applicant/?title={job.slugTitle}&value={job.id}")
        

class updateJobs(UpdateView):
    model = Job
    template_name = 'job/updateJob.html'
    form_class = create_job

def joblist(request):
    if "category" in request.GET:
        category = request.GET["category"]
        if category not in ["artisans", "programming", "finance", "others", "gigs", "graphic_designers"]:
            messages.error(request, f"No such category")
            return redirect("/jobs/home/")
    
    getJob = Job.objects.filter(fulfilled=False, category=category).order_by("-datetime")
    fav = Favourite.objects.all()
    
    hasPost = False
    if getJob.count() < 1:
        hasPost = True
    

    page = request.GET.get('page', 1)
    paginator = Paginator(getJob, 20)
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {"getJob": jobs, "fav": fav, "category":  category, "hasPost": hasPost }
    return render(request, "job/joblist.html", context) 

def generate_recommendation(title):
    recommend_list = []
    stop_words_list = ["a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder"]
    title_in_list = title.split(" ")   
    for each_word_in_list in title_in_list:
        if each_word_in_list.lower() not in stop_words_list:
            recommend_list.append(each_word_in_list)
    recommend_text = " ".join(recommend_list)  
    return recommend_text


def create(request):
    if request.user.is_authenticated:
        User_id = request.user.id
    
    #get the category through the id
    if request.method == "POST":
        createJob = create_job(request.POST)
        if "job_Image" in request.FILES:
            image = request.FILES["job_Image"]
        else:
            image = ""

        if createJob.is_valid():
            JobTitle = createJob.cleaned_data['title']
            slugTitle = JobTitle.replace(" ", "-")            
            name_of_company = createJob.cleaned_data['name_of_company'] 
            JobPost = createJob.cleaned_data['details'] 
            JobCategory = createJob.cleaned_data['category'] 
            JobPay = createJob.cleaned_data['pay']
            if not JobPay:
                JobPay = 0 
            JobPosition = createJob.cleaned_data['position'] 
            
            jobTags = generate_recommendation(JobTitle)
            string = jobTags.replace(" ", ")|(")
            jobInterest = r"({})".format(string)
            
            job = Job.objects.create(user_id=User_id, slugTitle=slugTitle, pay=JobPay, position=JobPosition, category=JobCategory, title=JobTitle, details=JobPost, name_of_company=name_of_company, jobImage=image, datetime=timezone.now())
            jobInvite = Profile.objects.filter(~Q(user_id=job.user_id), are_you_currently_unemployed=True, job_tags__iregex=jobInterest)
            summary = JobPost[:70] + "..."
            
            mailing_list = []
            mail_count = 0
            for each_invite in jobInvite:
                send_messages = Messages(sender_id=job.user_id, msg=f"{JobTitle}<br>{summary} <a href='/jobs/jobpage/{job.slugTitle}/{job.id}/'>apply</a>", receiver_id=each_invite.user_id, msg_type="job alert", receiver_seen=False)
                send_messages.save()
                if mail_count <= 12:
                    mailing_list.append(each_invite.user.email)
                    mail_count += 1
            
            url = f"/jobs/applicant/?title={job.slugTitle}&value={job.id}"
            subject = job.title
            html_message = render_to_string('job/mail_template.html', {'message': JobPost,  'subject': subject, "url": url, "getJob": job})
            plain_message = strip_tags(html_message)
            mail.send_mail(subject, plain_message, from_email="dataslid@gmail.com", recipient_list=mailing_list, html_message=html_message, fail_silently=False)
                                
            messages.success(request, f"{request.user.username}, you have sucessfully created a job, you will soon start recieving applications as interested candidates are being notified ")
            return redirect(f'/jobs/applicant/?title={job.slugTitle}&value={job.id}') 
        else:                
            messages.error(request, f"Invalid form ")
            return redirect(f'/jobs/create/') 


    else:
        context = {"job": create_job}
        return render(request, "job/create.html", context) 
    
def generate_recommendation(title):
    recommend_list = []
    stop_words_list = ["a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder"]
    title_in_list = title.split(" ")   
    for each_word_in_list in title_in_list:
        if each_word_in_list.lower() not in stop_words_list:
            recommend_list.append(each_word_in_list)
    recommend_text = " ".join(recommend_list)  
    return recommend_text


def jobpage(request):
    slug = request.GET["title"]
    job_id = request.GET['value']
    User_id = request.user.id
    getJob = Job.objects.get(id=job_id)
    already_applied = AlreadyApplied.objects.filter(user_id=request.user.id, job_id=job_id)
    #get the category through the id
    if request.method == "POST":  
        applyJob = request.FILES['files']
        if not applyJob.name.endswith(".pdf"):
            messages.error(request, "Only PDF allowed here")
            return redirect(f"/jobs/jobpage/?title={getJob.slugTitle}&value={getJob.id}")
            
        
        if len(already_applied) > 0:
            messages.error(request, "You have already applied for this" )
            return redirect(f"/jobs/jobpage/?title={getJob.slugTitle}&value={getJob.id}")
        
        applicant = Applicant(user_id=User_id, doc=applyJob, job_id=job_id, applydate=timezone.now())
        appliedJob = AlreadyApplied(user_id=request.user.id, job_id=job_id)
        
        send_messages = Messages(sender_id=request.user.id, msg=f"{request.user.username} applied to your Job post click <a style='font-weight: 900'class='tweet-this' href='/jobs/applicant/?title={getJob.slugTitle}&value={getJob.id}'>here</a> to see", receiver_id=getJob.user_id, msg_type="application submitted", receiver_seen=False)
        send_messages.save()
    
        applicant.save()
        appliedJob.save()        
         
        messages.success(request, "Job application submitted sucessfully")
        return redirect(f"/jobs/jobpage/?title={getJob.slugTitle}&value={getJob.id}")
    else:
        Job_title = generate_recommendation(getJob.title)
        string = Job_title.replace(" ", ")|(")
        search = r"({})".format(string)
        recommend = Job.objects.filter(~Q(id=job_id), title__iregex=r'{}'.format(search))
        recommendation = recommend.order_by("-datetime")[0:5] 
        
        fav = Favourite.objects.all()
        context = {"getJob": getJob, "fav": fav, "recommendation": recommendation}
        return render(request, "job/jobpage.html", context) 

def yourjobs(request):
    getJob = Job.objects.filter(user_id=request.user.id, fulfilled=False).order_by("-datetime")
    fav = Favourite.objects.all()
    
    hasPost = False
    if getJob.count() < 1:
        hasPost = True
    

    page = request.GET.get('page', 1)
    paginator = Paginator(getJob, 20)
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {"getJob": jobs, "hasPost": hasPost }
    return render(request, "job/yourjobs.html", context) 

def eachJobs(request):
    # Getting the queries
    slug = request.GET["title"]
    job_id = request.GET['value']

    User_id = request.user.id
    if request.method == "POST":
        getJob = Job.objects.get(id=job_id, user_id=User_id)
        try:
            choice = request.POST["fulfilled"]
            fulfilled = True
            getJob.delete()
            messages.success(request, "we are glad you got someone")
            return redirect(f"/jobs/yourjobs/")
        
        except Exception as error:
            fulfilled = False
        
        messages.info(request, "You didn't select anything")
        return redirect(f"/jobs/applicant/?title={slug}&value={job_id}")
            
    else:
        getJob = Job.objects.get(id=job_id, user_id=User_id, fulfilled=False)
        getApplicants = Applicant.objects.filter(job_id=job_id)
        fav = Favourite.objects.filter(fav_thread__iregex='/jobs/', user_id=request.user.id, title=getJob.title, fav_id=getJob.id )
        fav_bool = True if len(fav) > 0 else False
   
        context = {"job": getJob, "applicants": getApplicants}
        return render(request, "job/application_page.html", context) 
 
def resume(request):
    resumeForm = ResumeForm()
    context = {"resumeForm": resumeForm } 
    return render(request, "job/resume.html", context)
    
def show_resume(request):
    applicant = request.GET["applicant"]
    job = request.GET["job"]
    applicant_resume = Applicant.objects.get(user_id=applicant, job_id=job)
    context = {"resume": applicant_resume } 
    return render(request, "job/show_resume.html", context)

def search_job(request):
    if request.method == "POST":
        query = request.POST["search"]
        if query == "":
            messages.error(request, "oops no result...")
            return redirect("/jobs/search-job/")

        jobs = Job.objects.filter(title__iregex=query)
        
        if len(jobs) == 0:
            messages.error(request, "oops no result...")
            return redirect("/jobs/search-job/")
        fav = Favourite.objects.all()

        context = {"searches": jobs, "fav": fav, "keyword": query, }
        return render(request, "job/search_job.html", context)
    else:
        return render(request, "job/search_job.html")