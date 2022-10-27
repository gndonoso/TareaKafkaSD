from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import asyncio
import nest_asyncio

nest_asyncio.apply()
loop = asyncio.get_event_loop()

async def consume():

    topic = 'Stock'
    bootstrap_servers = 'kafka:9092'
    
    premium = KafkaConsumer(bootstrap_servers=bootstrap_servers, auto_offset_reset='latest', group_id='stockInsuficiente')
    
    premium.assign([TopicPartition(topic, 1)])

    for message in premium:
        print ("Stock Insuficiente ->%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))

loop.run_until_complete(consume())