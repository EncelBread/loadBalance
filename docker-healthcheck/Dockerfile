FROM python:3

RUN pip install redis
RUN pip install requests
RUN pip install time
RUN pip install threading
RUN pip install traceback
COPY ./healthcheck.py ./app/healthcheck.py

CMD ["python", "/app/healthcheck.py"]