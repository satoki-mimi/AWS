import json
import os
import boto3

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = "{public.key}"

def verify_signature(event):
    raw_body = event.get("raw-body")
    auth_sig = event["params"]["header"].get("x-signature-ed25519")
    auth_ts = event["params"]["header"].get("x-signature-timestamp")
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig))


def start_ec2_instance():
    instance_id = [os.environ['INSTANCE_ID']]
    region = os.environ['REGION_NAME']
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=[instance_id])
    print('started your instances: ' + str(instance_id))


def stop_ec2_instance():
    instance_id = [os.environ['INSTANCE_ID']]
    region = os.environ['REGION_NAME']
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=[instance_id])
    print('stopped your instances: ' + str(instance_id))


def lambda_handler(event, context):
    print(f"event {event}")
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    body = event.get("body-json")
    # InteractionType.Ping
    if body.get("type") == 1:
        return {"type": 1}
    # InteractionResponseType.ChannelMessageWithSource
    elif body.get("type") == 2:
        value = body.get("data").get("options")[0].get("value")
        if value == "control_start":
            start_ec2_instance()
            return {
                "type": 4,
                "data": {
                    "content": "Starting minecraft server...",
                },
            }
        elif value == "control_stop":
            stop_ec2_instance()
            return {
                "type": 4,
                "data": {
                    "content": "Stopping minecraft server...",
                },
            }
        else:
            return {
                "type": 4,
                "data": {
                    "content": "undefined",
                },
            }
    else:
        return {
            "type": 4,
            "data": {
                "content": "undefined",
            },
        }
