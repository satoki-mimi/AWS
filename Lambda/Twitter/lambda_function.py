import boto3
import os
import tweepy

def lambda_handler(event, context):
    CONSUMER_KEY = os.environ['consumer_key']
    CONSUMER_SECRET = os.environ['consumer_secret']
    ACCESS_TOKEN = os.environ['access_token']
    ACCESS_SECRET = os.environ['access_secret']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    try:
        screen_name = os.environ['screen_name']
        user = api.get_user(screen_name=screen_name)
        message = 'That twitter account still exists.' 
        print(message)
    except:
        message = 'That twitter account is deleted!'
        print(message)
        publish_sns(message)
        disable_schedule()
        
def publish_sns(message):
    client = boto3.client('sns')
    params = {
        'TopicArn': os.environ['topic_arn'],
        'Message': message
    }
    client.publish(**params)
    
def disable_schedule():
    client = boto3.client('scheduler')
    schedule_name = os.environ['schedule_name']
    update_schedule(client, schedule_name, State="DISABLED")
    
def update_schedule(client, schedule_name, **kwargs):
    current_params = client.get_schedule(Name=schedule_name)
    unnecessaries = ["ResponseMetadata", "Arn", "CreationDate", "LastModificationDate"]
    keys = [x for x in current_params if x not in unnecessaries]
    params = {}
    for key in keys:
        params[key] = current_params[key]
    for k, v in kwargs.items():
        params[k] = v
    client.update_schedule(**params)
