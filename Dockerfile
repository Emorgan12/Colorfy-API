FROM python:slim

ADD ./main.py /main.py
ADD ./spotify_background_color.py /spotify_background_color.py
ADD ./requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y cmake && apt-get install build-essential -y
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]