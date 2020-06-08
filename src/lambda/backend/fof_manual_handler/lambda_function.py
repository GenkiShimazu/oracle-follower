import random
from fof_sdk.dynamo_ctl import DynamoCtl
from fof_sdk import user
from fof_sdk import hero
from fof_sdk import util


def main(alexa_user_id, intent, destinations):
    action = {
        'type': 'end'
        }
    if intent == 'HelpIntent':
        with DynamoCtl(alexa_user_id) as dynamo_ctl:
            _user = user.get_user(alexa_user_id, dynamo_ctl.attr)
            dynamo_ctl.attr = _user.attr

            if not destinations:
                destinations = random.sample(util.get_village_names(), 2)
            return {
                'type': 'help',
                'original_texts': [
                    {'text': 'SKILL_SUMMARY'},
                    hero.total_followers(_user.follower_total_amount),
                    hero.ask_oracle(destinations)
                    ]
                }
    elif intent == 'CancelOrStopIntent':
        return {
            'type': 'cancel_or_stop',
            'image_url': util.get_image('hero_anticipation'),
            'original_texts': [
                {
                    'text': 'APPRECIATE_ON_STOP',
                    'kwargs': {
                        'appreciate': hero.get_appreciate_message()
                        }
                    },
                {'text': 'PLEASE_AGAIN_ON_STOP'}
                ]
            }
    return action


def lambda_handler(event, context):
    alexa_user_id = event['alexa_user_id']
    intent = event['intent']
    destinations = event.get('destinations_choice')
    response = main(alexa_user_id, intent, destinations)
    return response
