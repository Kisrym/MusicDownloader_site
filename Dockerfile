FROM python:3.11-bullseye
WORKDIR /musicdownloader-site
COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]