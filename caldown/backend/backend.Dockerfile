FROM python:3.9-alpine
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
copy ./backend/app /app
CMD ["flask", "run"]