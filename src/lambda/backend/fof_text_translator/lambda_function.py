import tutorial
import hero
import help
import cancel_or_stop
import buy_response
import ganesha_shop
import intent_use
import what_have_i_got

text_map = {}
text_map.update(tutorial.text_map)
text_map.update(hero.text_map)
text_map.update(help.text_map)
text_map.update(what_have_i_got.text_map)
text_map.update(cancel_or_stop.text_map)
text_map.update(buy_response.text_map)
text_map.update(ganesha_shop.text_map)
text_map.update(intent_use.text_map)


def translate_text(text_key: str, **kwargs) -> str:
    """
    :param text_key: TUTORIAL_SEND_OUT
    :param kwargs: ex.) ** {'destination': 'マゼンタコート'}
    """
    parameters = {}
    for k, kwarg in kwargs.items():
        parameters[k] = text_map.get(kwarg, kwarg)

    base_text: str = text_map.get(text_key, text_key)
    return base_text.format(**parameters)


def main(original_texts) -> str:
    response_texts = []
    for original_text in original_texts:
        text_key = original_text.get('text')
        parameters = original_text.get('kwargs', {})
        translated_text = translate_text(text_key, **parameters)
        response_texts.append(translated_text)
    return ''.join(response_texts)


def lambda_handler(event, context):
    original_texts = event.get('original_texts')
    response_text = main(original_texts)
    return response_text
