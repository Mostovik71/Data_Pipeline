from kafka import KafkaProducer
from data_generator import generate_message
import json
import time

# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer

producer = KafkaProducer(
    bootstrap_servers='localhost:9094',
    value_serializer=serializer
)

if __name__ == '__main__':
    while True:
        test_message = generate_message()

        producer.send('test-topic', 
                      value=test_message)
        time.sleep(2)