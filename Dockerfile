FROM python:3

COPY . .

ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "testDB.py" ]