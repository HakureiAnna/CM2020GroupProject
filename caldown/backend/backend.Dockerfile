FROM python:3.9-alpine
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV JWT_SECRET=p@ssw0rd123
ENV JWT_DELTA=86400
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 9000
copy ./backend/app /app
CMD ["uwsgi", "app.ini"]