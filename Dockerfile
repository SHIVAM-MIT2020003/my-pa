FROM ubuntu:16.04


RUN apt-get -y update && apt-get install -y python3-virtualenv virtualenv python3-pip && pip3 install --upgrade pip
ENV WORKDIR /opt 

WORKDIR $WORKDIR
ADD requirements $WORKDIR/requirements

RUN pip3 install -r requirements/production.txt
RUN python3 -m nltk.downloader all
ADD ./ $WORKDIR
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate


CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:$PORT"]



