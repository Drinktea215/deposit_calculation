FROM python:3.10.6

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD main.py /main.py

ADD src /src

ADD tests /tests

RUN python -m unittest tests.tests

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]