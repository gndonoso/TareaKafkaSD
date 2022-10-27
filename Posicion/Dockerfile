FROM bitnami/python:3.8.13

RUN pip install flask
RUN pip install kafka-python
ENV FLASK_APP=api_ubicaciones.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002

EXPOSE 5002
COPY . .

CMD ["flask", "run"]