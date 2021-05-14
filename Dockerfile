FROM python
WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade -r /tmp/requirements.txt
 
COPY . /app
ENV FLASK_APP=server/__init__.py
CMD ["python", "manage.py", "start", "0.0.0.0:3000"]