from fof_sdk import hero
from fof_sdk import util
from fof_sdk.user import User


def launch(user: User):
    if user.has_todays_oracle:
        return {
            'type': 'use',
            'original_texts': [
                {
                    'text': 'CONFIRM_CHRONUS_TICKET'
                }
            ]
        }
    return {
        'type': 'oracle',
        'original_texts': [
            {
                'text': 'PLEASE_ORACLE'
            },
            {
                'text': hero.message()
            },
            {
                'text': hero.ask_oracle(util.get_destinations_choice())
            }
        ]
    }


def use_ticket(user: User):
    return {
        'type': 'oracle',
        'original_texts': [
            {
                'text': 'AUDIO_TIME_PASS'
            },
            {
                'text': 'EARTH_TIME_PASSED'
            },
            {
                'text': hero.message()
            },
            {
                'text': hero.ask_oracle(util.get_destinations_choice())
            }
        ]
    }
