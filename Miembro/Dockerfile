FROM bitnami/python:3.8.13

RUN pip install kafka-python
RUN pip3 install nest_asyncio

EXPOSE 5003
COPY . .

CMD ["python3", "api_miembro.py"]