FROM bitnami/python:3.8.13

RUN pip install flask
RUN pip install kafka-python
ENV FLASK_APP=api_ventas.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000
COPY . .

CMD ["flask", "run"]