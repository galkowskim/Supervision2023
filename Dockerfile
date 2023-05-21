FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev build-essential
RUN mkdir Supervision2023
COPY . .
RUN pip install -r requirements.txt

ENV PYTHONIOENCODING=utf-8

WORKDIR Supervision2023

# Expose port 8000
EXPOSE 8000

CMD cd ../backend
CMD source ../venv/bin/activate

CMD ["bash", "-c", "cd ../backend && source ../venv/bin/activate && python3 manage.py runserver 0.0.0.0:8000"]