from django.utils.html import strip_tags
from django import template
import datetime
from datetime import timedelta
# from urllib.parse import urlparse
import re
import time
import pytz
import math

register = template.Library()

@register.filter
def getdata(obj, id):
    d = obj.filter(user_id=id)
    return obj.filter(user_id=id).first()

@register.filter
def getuserdata(obj, id):
    data = obj.filter(id=id)
    return data.first()


@register.filter
def getfollowdata(obj, id):
    data = obj.filter(follower_id=id)
    return data.first()


@register.filter
def likenum(obj, bools):
    bools = bool(bools)
    return obj.filter(each_like=bools).count()


@register.filter
def bloglikenum(obj, bools):
    bools = bool(bools)
    return obj.filter(blog_like=bools).count()

@register.filter
def follownum(obj, bools):
    bools = bool(bools)
    return obj.filter(follow=bools).count()


@register.filter
def dislikenum(obj, bools):
    bools = bool(bools)
    return obj.filter(each_dislike=bools).count()

@register.filter
def trunc(string):
    strip_string = strip_tags(string)
    return strip_string[:100] + "..."

@register.filter
def colorText(text, string):
    regex = re.compile(string, re.IGNORECASE)
    return regex.sub(f'<span style="color: rgb(29, 161, 242);"><b>{string}</b></span>', text )


@register.filter
def colorInvites(text):
    invites = re.findall("@\w+", text)
    for invite in invites:
        name_of_invited = invite[1:]
        text = text.replace(invite, f"<a href='/profile/{name_of_invited}/' style='font-size: 16px; color: rgb(29, 161, 242);'><b>{invite}</b></a>")
    return text
    

@register.filter
def app(path, string):
    path = path.replace("/", "") 
    path = path.replace("-", "")
    value = re.match(string, path)
    if value:
        return string
    return None

@register.filter
def default_pic(string):
    text = string[0].upper()
    return text    

@register.filter
def  new_threads(old_date):
    utc=pytz.UTC
    date = old_date
    new = utc.localize(datetime.datetime.now() +  datetime.timedelta(days=-3))
    if date > new:
        return True
    else:
        return False

@register.filter
def  pollTime(expiredTime):
    expiryTime = expiredTime
    currentTime = time.time()
    if currentTime < expiredTime:
        return True
    else:
        return False

@register.filter
def  pollNewExpiryTime(expiredTime):
    currentTime = time.time()
    expiryTime = expiredTime
    expiry = expiryTime - currentTime
    return expiry * 1000

@register.filter
def  ExpiredFinalTime(expiredTime):
    expirytime = datetime.datetime.fromtimestamp(expiredTime)
    Date = expirytime.strftime("%d %b %Y")
    return Date

@register.filter
def blogDate(date):
    Date = date.strftime("%d %b %Y")
    if Date[0] == "0":
        Date = Date[1:]
    return Date


@register.filter
def forumDate(date):
    Date = date.strftime("%d %b %Y %I:%M %p")
    if Date[0] == "0":
        Date = Date[1:]
    return Date


@register.filter
def blogReadTime(words):
    readTime = len(words)
    readTime //= 200
    return readTime

@register.filter
def GetFav(obj, ID):
    data = obj.filter(fav_thread__iregex="/jobs/", fav_id=ID)
    if data:
        return data.first().user_id
    return data.first()

@register.filter
def GetFavPoll(obj, ID):
    data = obj.filter(fav_thread__iregex="/polls/", fav_id=ID)
    if data:
        return data.first().user_id
    return data.first()

@register.filter
def GetFavBlog(obj, ID):
    data = obj.filter(fav_thread__iregex="/blog/", fav_id=ID)
    if data:
        return data.first().user_id
    return data.first()

@register.filter
def removeUrl(path):
    url = path.replace("%20", "-") 
    return url


@register.filter
def httpUrl(path):
    checkUrl = re.match("http://", path)
    if checkUrl:
        return path
    else:
        return f"http://{path}"

@register.filter
def numba_of_views(num):
    if num > 999:
        return f'{num / 1000}K'
    else:
        return num

@register.filter
def check_following(obj, id):
    data = obj.filter(following_id=id)
    if data.exists():
        return True
    else:
        return False

@register.filter
def keywords(string):
    return string.replace(" ", ", ")

@register.filter
def onlineStatus(old_date):
    utc=pytz.UTC
    date = old_date
    new = utc.localize(datetime.datetime.now() +  datetime.timedelta(minutes=-64))
    if date > new:
        return True
    else:
        return False

@register.filter
def urlFilter(text):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"    
    url = re.findall(regex, text)
    for each_url in url:
        web_url = each_url[0]

        youtube_pattern = re.match("^.*(youtu.be\/|v\/|embed\/|watch\?|youtube.com\/user\/[^#]*#([^\/]*?\/)*)\??v?=?([^#\&\?]*).*", web_url)
        if(youtube_pattern):
            youtube_id = youtube_pattern.group(3) 
            text = text.replace(f"{web_url}", f"<iframe width='100%' src='http://www.youtube.com/embed/{youtube_id}'></iframe>" ) 
        else:
            if (re.match("(http(s)?:\/\/)", web_url)):
                text = text.replace(f"{web_url}", f"<a style='word-wrap: word-break; word-break: break-all' class='tweet-color' target='_blank' href='{web_url}'>{web_url}</a>" ) 
            else:
                text = text.replace(f"{web_url}", f"<a class='tweet-color' style='word-wrap: word-break; word-break: break-all' target='_blank' href='http://{web_url}'>{web_url}</a>" ) 
    return text

