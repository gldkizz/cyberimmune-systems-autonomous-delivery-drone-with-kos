import json
from extensions import mqtt_client as mqtt
from utils import sign, generate_forbidden_zones_string
from db.dao import get_entity_by_key
from db.models import Uav
from constants import MQTTTopic, KeyGroup, FORBIDDEN_ZONES_PATH

def mqtt_publish_flight_state(id: str, *args, **kwargs):
    uav_entity = get_entity_by_key(Uav, id)
    if not uav_entity:
        return
    else:
        if uav_entity.kill_switch_state:
            message = '$Flight -1'
        elif uav_entity.is_armed:
            message = '$Flight 0'
        else:
            message = '$Flight 1'
            
    message = f'{message}#{hex(sign(message, KeyGroup.ORVD))[2:]}'
    mqtt.publish_message(MQTTTopic.FLIGHT_STATUS.format(id=id), message)
    
def mqtt_publish_ping(id: str, *args, **kwargs):
    uav_entity = get_entity_by_key(Uav, id)
    if not uav_entity:
        return
    else:
        message = f'$Delay {uav_entity.delay}'
    message = f'{message}#{hex(sign(message, KeyGroup.ORVD))[2:]}'
    mqtt.publish_message(MQTTTopic.PING.format(id=id), message)

def mqtt_publish_forbidden_zones(*args, **kwargs):
    try:
        with open(FORBIDDEN_ZONES_PATH, 'r', encoding='utf-8') as f:
            forbidden_zones = json.load(f)
            message = generate_forbidden_zones_string(forbidden_zones)
            message = f'{message}#{hex(sign(message, KeyGroup.ORVD))[2:]}'
            mqtt.publish_message(MQTTTopic.FORBIDDEN_ZONES, message)

    except Exception as e:
        print(e)
        return
