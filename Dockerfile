FROM python:3

RUN pip install flask
RUN pip install redis
RUN pip install requests
COPY ./app.py /app/app.py
ENV FLASK_APP=/app/app.py

CMD ["python", "/app/app.py"]