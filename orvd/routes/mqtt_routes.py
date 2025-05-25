import json
from urllib.parse import parse_qs
from constants import MQTTTopic
from extensions import mqtt_client as mqtt
from utils import regular_request
from handlers.api_handlers import telemetry_handler
from handlers.general_handlers import fmission_ms_handler

def extract_id_from_kwargs(kwargs):
    id = kwargs.get('id')
    if id:
        return id
    else:
        raise Exception("No id provided.")

@mqtt.topic(f"{MQTTTopic.TELEMETRY}/{{id}}")
def handle_telemetry_message(client, userdata, msg, **kwargs):
    try:
        query_string = msg.payload.decode()
        query_params = parse_qs(query_string)
        single_value_params = {k: v[0] for k, v in query_params.items()}
        single_value_params['id'] = extract_id_from_kwargs(kwargs)
        regular_request(handler_func=telemetry_handler, **single_value_params)
    except Exception as e:
        print(f"Error handling telemetry message: {e}")

@mqtt.topic(f"{MQTTTopic.MISSION}/{{id}}")
def handle_mission_message(client, userdata, msg, **kwargs):
    try:
        payload_str = msg.payload.decode()
        payload = json.loads(payload_str)
        payload['id'] = extract_id_from_kwargs(kwargs)
        regular_request(handler_func=fmission_ms_handler, **payload)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from mission message: {e}. Payload: {payload_str}")
    except Exception as e:
        print(f"Error handling mission message: {e}")