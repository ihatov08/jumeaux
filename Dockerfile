FROM python:3.6

RUN pip install jumeaux==0.34.0
WORKDIR tmp

ENTRYPOINT ["jumeaux"]

