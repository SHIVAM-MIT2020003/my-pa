from __future__ import unicode_literals, absolute_import
from celery.result import AsyncResult
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
import time
from urllib.parse import unquote
from django.contrib.auth.decorators import login_required
import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk import pos_tag, ne_chunk
from numpy import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import requests
import re
from django.core.mail import EmailMessage
from datetime import datetime
from social_django.utils import load_strategy
from .audio_recorder.models import *
from twilio.rest import Client
from twilio.rest.api.v2010.account.call import CallInstance
nltk.data.path.append('/root/nltk_data/')
from multiprocessing.dummy import Pool


# Learning..
# Sentimental Analysis
positive_vocab = set([ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ])
negative_vocab = set([ 'bad', 'terrible','useless', 'hate', 'disliked'])
neutral_vocab = set([ 'movie','the','sound','was','is','actors','did','know','words','not' ])

# Fetch important sentence
relevant = set([
'extract',
'work',
'complete', 
'proposal',
'spoil',
'forget',
'reach',
'do',
'roadblock',
'roadblocks',
'road block',
'road blocks',
'expect',
'unexpect',
'plan',
'integrate',
'assign',
'onboard',
'task',
'code',
'organize',
'perfect',
'coding',
'client',
'call',
'requirement',
'module',
'django',
'technology',
'use',
'react',
'javascript',
'json',
'package',
'github',
'git',
'worked',
'assigned',
'summarized',
'summary',
'vpn',
'machine',
'local',
'docker',
'deliver',
'adorable',
'accepted',
'acclaimed',
'accomplish',
'accomplishment',
'achievement',
'action',
'active',
'admire'
'affirmative',
'affluent',
'agree',
'agreeable'
'amazing'
'angelic'
'appealing'
'approve'
'aptitude'
'attractive',
'beneficial',
'choice',
'creative',
'distinguish',
'effective',
'effective',
'essential',
'imagine',
'impressive',
'innovate',
'prominent'
])


irrelevant = set(
[
'fun',
'adventure',
'play',
'enjoy',
'entertain',
'entertainment',
'hang out',
])


question = set(['which', 'when', 'how', 'where', 'what', 'why', "what's", "?"])
helping_verbs = set(['do', 'does', 'is', 'am', 'are', 'has', 'have', 'did', 'was', 'were', 'had', 'will', 'shall'])

name_regex = r"(?:Hi|hi) [a-zA-Z]+"

def health_check(request):
    return HttpResponse("OK", status=200)

@csrf_exempt
def show_summary(request):
    res = request.POST.get('final_data', None)
    return HttpResponse(res)


@csrf_exempt
def get_processed_data(request):
    text = request.POST.get('buffer_data', None)
    sentences = get_sentences(text)
    relevant_sentences = get_important_sentence(sentences)
    relevant_sentences = " ".join(relevant_sentences)
    return JsonResponse({'data' : relevant_sentences + " ", 'name_list': ""})

# Natural language processing functions
def word_feats(words):
    return dict([(word, True) for word in words])

# sentimental analysis
def sentiment_analysis(sentence="The movie was good."):
    positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
    negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
    neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
    train_set = negative_features + positive_features + neutral_features
    classifier = NaiveBayesClassifier.train(train_set)
    neg = 0
    pos = 0
    sentence = sentence.lower()
    words = sentence.split(' ')
    for word in words:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1

    positive_result = float(pos) / len(words)
    negative_result = float(neg) / len(words)
    if(positive_result > negative_result):
        pass
    elif negative_result > positive_result:
        pass
    else:
        pass


# pull entities from text
def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
         if type(i) == nltk.Tree:
             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
         elif current_chunk:
             named_entity = " ".join(current_chunk)
             if named_entity not in continuous_chunk:
                 continuous_chunk.append(named_entity)
                 current_chunk = []
         else:
             continue
    return continuous_chunk


# Split whole text into list of sentence(list of words).
def get_sentences(text):
    global imp_sent
    res = punctuator(text)
    sentences = sent_tokenize(res)
    final_sentences = []
    imp_sent = []
    for sentence in sentences:
        temp = sentence.split(" ")
        temp = trim_sentence(temp)
        if sentence_type_question(temp):
            continue
        if re.search(name_regex, sentence):
            match = re.search(name_regex,  sentence)
            imp_sent.append('<br />' + '<span style="color:green">@' +match.group(0)[3:] + '</span>' + '<br />')
        if len(temp) > 0 and temp[len(temp) - 1].strip()[-1] != '?':
            final_sentences.append(temp)
    return final_sentences


def punctuator(text):
    url = 'http://bark.phon.ioc.ee/punctuator'
    payload = {'text': text}
    headers = {}
    res = requests.post(url, data=payload, headers=headers)
    return str(res.content)[2:-1]


def sentence_type_question(sentence):
    if sentence[0].lower() in helping_verbs:
        return True
    for word in sentence:
        if word.lower() in question:
            return True
    return False


def trim_sentence(word_tokens):
    l = []
    for word in word_tokens:
        if word[len(word) - 1] == ',' or word[len(word) - 1] == '.':
            l.append(word[:-1])
        else:
            l.append(word)
    return l


def get_important_sentence(sentences):
    lemmetized_sentences = get_lemmetized_sentences(sentences)
    for i in range(len(lemmetized_sentences)):
        relevant_count = 0
        irrelevant_count = 0

        for word in relevant:
            for j in range(len(lemmetized_sentences[i])):
                if(lemmetized_sentences[i][j] == word):
                    relevant_count += 1
                    sentences[i][j] = '<span style="color:red;font-style: italic">' + sentences[i][j] + '</span>'

        for word in irrelevant:
            if word in lemmetized_sentences[i]:
                irrelevant_count += 1

        if relevant_count > 0:
            temp = '<img src="/static/bulletpoint.png">  ' + (" ".join(sentences[i])) + ". "
            imp_sent.append(temp + "<br />")

        elif relevant_count > 0 and irrelevant_count > 0:
            relevant_features = [(word_feats(rel), 'rel') for rel in relevant]
            irrelevant_features = [(word_feats(irre), 'irre') for irre in irrelevant]
            train_set = relevant_features + irrelevant_features
            classifier = NaiveBayesClassifier.train(train_set)
            rel_res = 0
            irre_res = 0
            for word in lemmetized_sentences[i]:
                classifier_res = classifier.classify(word_feats(word))
                if classifier_res == 'rel':
                    rel_res += 1
                else:
                    irre_res += 1
            if (rel_res > irre_res):
                temp = '<img src="/static/bulletpoint.png">  ' + (" ".join(sentences[i])) + " ."
                imp_sent.append(temp + "<br />")
    return imp_sent


def get_lemmetized_sentences(sentences):
    lemmetizer = WordNetLemmatizer()
    swords = set(stopwords.words("english"))
    sents = []
    lwords = []
    for sent in sentences:
        for word in sent:
            word = lemmetizer.lemmatize(word, pos = "v")
            if word not in swords:
               lwords.append(word)
            else:
                lwords.append('-')
        sents.append(lwords)
        lwords = []
    return sents


# Get entities
def get_entity(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing alone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person_list.append(person[0])
        person = []

    for subtree in sentt.subtrees():
        for leaf in subtree.leaves():
            if leaf[1] == "NNP" and leaf[0] not in person_list:
                person_list.append(leaf[0])
    return person_list


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def send_email(request):
    #this section of code is to beexecuted from cron
    # pool  = Pool(1)
    # future = []
    # requests.get("https://c578ec25.ngrok.io/test_twilio")
    # future.append(pool.map(requests.get, ["https://50765fa6.ngrok.io/test_twilio"]))
    # pool.close()
    # pool.join()
    # requests.get("https://50765fa6.ngrok.io/test_twilio")
    event_id = request.POST.get('event_id')
    event = Event.objects.get(pk=event_id)
    attendees = event.member_set.all()
    info_type = request.POST.get('information_type')
    data = request.POST.get('email_raw_data')
    data=unquote(data)
    meeting_details = '{:^10}'.format("MEETING DETAILS\n\n\n")
    meeting_title = "Title : " + event.title +"\n\n"
    meeting_date = "Date : " + event.start_date + "\n\n"
    meeting_number_of_guests = "Total Guest Invited: "+ str(attendees.count())+"\n\n"
    meeting_info = meeting_details + meeting_title + meeting_date + meeting_number_of_guests+"\n\n"
    if info_type == 'original':
        # subject  = "Original Transcript of meeting held on " + datetime.now().strftime('%Y-%m-%d')
        subject = "Original Transcript - \' "+event.title +"\'"
        result = meeting_info+'Original Transcript\n\n\n\n' + data
    else:
        subject  = "Meeting Summary - \' "+event.title +"\'"
        result =meeting_info+'Summary\n\n\n\n' + data
    to = [attendee.email_id for attendee in attendees]
    body = "Hi,\n\n Please find the "+info_type+" details of the meeting attached below.\n\n\n\n\n\n\n Cheers,\n MyPA Team"
    email = EmailMessage(subject, body , to=["assistant.mypa@gmail.com"])
    attachment_name = info_type+" details - " + datetime.now().strftime('%Y-%m-%d')
    email.attach(attachment_name,result)
    email.send()
    return JsonResponse({'data': 'success'})


@csrf_exempt
def dialog(request):
    response_text = "successful"
    return JsonResponse(status=200, data={'fulfillmentText': response_text})


def get_current_event():
    events = Event.objects.all()
    current_time = datetime.strftime(datetime.now(), "%I:%M %p")
    for event in events:
        if current_time == event.start_time:
            return event
    return "NO"



def dashboard(request):
    get_current_event()
    if request.user.is_authenticated:
        user = request.user
        social = user.social_auth.get(provider='google-oauth2')

        access_token = social.get_access_token(load_strategy())
        response = requests.get(
            'https://www.googleapis.com/calendar/v3/calendars/primary/events',
            params={'access_token': access_token}
        )
        events = response.json()["items"]

        Event.objects.all().delete()
        for event in events:
            try:
                print(event["start"]["dateTime"])
                end_date = event["end"]["dateTime"][:10]
                date1 = time.strptime(end_date,"%Y-%m-%d")
                temp = datetime.now()
                current_year = temp.year
                current_month =temp.month
                current_day = temp.day
                date_form = str(current_year) +"-"+str(current_month) +"-"+str(current_day)
                date2 = time.strptime(date_form, "%Y-%m-%d")
                time1 = event["start"]["dateTime"][11:16]
                d = datetime.strptime(time1, "%H:%M")
                description = event["description"]
                print(description)
                match_obj = re.match(r'Meeting ID: ((\d+[ ])+\d+)\n',description)
                # print(match_obj.group(1))
                if date1 < date2:
                    continue
                mevent = Event()
                mevent.id = event["id"]
                mevent.start_date = event["start"]["dateTime"][:10]
                mevent.start_time = d.strftime("%I:%M %p")
                mevent.end_date = event["end"]["dateTime"]
                mevent.creator = event["creator"]["email"]
                mevent.organiser = event["organizer"]["email"]
                mevent.title = event["summary"]
                mevent.save()

                for member in event["attendees"]:
                    m = Member()
                    m.email_id = str(member["email"])
                    m.user_name = m.email_id[:m.email_id.find("@")]
                    m.attendees = mevent
                    m.save()

            except KeyError:
                continue
            except TypeError:
                continue

        count = 0
        events_info = Event.objects.all()
        return render(request, '../templates/dashboard.html',{"events":events_info})
    else:
        return HttpResponseRedirect(reverse('login'))

def test_twilio(request):
    '''calls programtically to a number and records the call for a mzaximum of 60 seconds and provides speec to text transcript'''
    account_sid = "AC7cf9207859d7c0fbe3d980c94622efbf"
    auth_token = "2e51abd9a58a91dbaf99af733ba76fcc"
    client = Client(account_sid, auth_token)
    call = client.calls.create(to="+91",from_ = "+17206054588", url="https://handler.twilio.com/twiml/EH025a4d97ffed658b2a2549e0919bf2be")
    recording_sid = client.recordings.list()[0].sid
    # print(recording_sid)
    recording = client.api.v2010.accounts(sid=account_sid).recordings(sid=recording_sid).fetch()
    uri = (recording.uri[:-5:])
    url = "https://api.twilio.com" + uri;
    # print(url)
    res = requests.get(url, stream=True)
    file_name = str(recording_sid) + ".wav"
    with open(file_name, 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    tr = client.transcriptions.list()

    return redirect(url)
