from __future__ import absolute_import, unicode_literals
from celery import shared_task
from twilio.rest import Client
from twilio import twiml
import requests
import wave

@shared_task
def call_twilio():
    #MYPA FREE ACCOUNT
    account_sid = "AC480bbd770e3c24349cd83e83031467b7"
    auth_token = "81c207af96c5c4c8badb757808204083"
    client = Client(account_sid, auth_token)
    call = client.calls.create(to="+91", from_="+17014012648",
                               url="https://handler.twilio.com/twiml/EH1c0e7919937bee9132d865ecf716e419"
                               ,send_digits="wwwwwwwwwwwwwwwwwwww845740959#")
    # MypA FREE ACCOUNT
    flag = True
    print("I am entering the if function\n\n\n\n")

    while flag:
        if (call.status == "queued" or call.status == "in-progress" or call.status == "ringing" or call.status == "answered"):
            calls = client.calls.list(status="completed")
            flag = True
            for c in calls:
                # print(c.sid)
                # print(call.sid)
                # print()
                if c.sid == call.sid or call.status == "canceled":
                    flag = False
                    break
        else:
            flag = False
    print("I am outside the if functions\n\n")
    calls = client.calls.list(status="completed")[0]
    print("I was the call in progress", calls.sid, "\n\n\n")
    # recording_sid = client.recordings.list()[0].sid
    # recording = client.api.v2010.accounts(sid=account_sid).recordings(sid=recording_sid).fetch()
    # uri = (recording.uri[:-5:])
    # url = "https://api.twilio.com" + uri;
    # print(url)
    infile = []
    recording_list = client.recordings.list()
    for record in recording_list:

        if record.call_sid == calls.sid:
            url = ""
            recording = client.api.v2010.accounts(sid=account_sid).recordings(sid=record.sid).fetch()
            uri = (recording.uri[:-5:])
            url = "https://api.twilio.com" + uri;
            file_name = str(record.sid) + ".wav"
            infile.append(file_name)
            res = requests.get(url, stream=True)
            with open(file_name, 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            res.close()
    outfile = str(calls.sid)+".wav"
    data = []
    infile.reverse()
    for infile in infile:
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for c in range(0,len(data)):
     output.writeframes(data[c][1])
    output.close()
    return True
