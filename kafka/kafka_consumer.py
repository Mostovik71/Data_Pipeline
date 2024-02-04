import json
from kafka import KafkaConsumer

if __name__ == '__main__':
    consumer = KafkaConsumer('test-topic',
                             bootstrap_servers='localhost:9094',
                             auto_offset_reset='earliest'
                             )
    
    for message in consumer:
        print(json.loads(message.value))