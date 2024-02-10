from kafka import KafkaConsumer
from avro.schema import parse_schema
from avro.io import DatumReader, BinaryDecoder
import io

schema_av = parse_schema(open("C:/Users/mosto/Desktop/DE_Pipeline/habits_schema.avsc", "rb").read())
# reader = DatumReader(schema_av)



def decode(msg_value):
    message_bytes = io.BytesIO(msg_value)
#    message_bytes.seek(2)
    decoder = BinaryDecoder(message_bytes)
    record = schema_av.read(decoder)
    #event_dict = reader.read(decoder)
    return record

if __name__ == '__main__':
    consumer = KafkaConsumer("postgres.public.reports_data",
                             bootstrap_servers=["localhost:29092"]
                             )
                             
    for message in consumer:
        data = decode(message.value)
        print(data)