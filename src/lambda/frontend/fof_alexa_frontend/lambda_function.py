# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK.
import logging

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model import ui
from ask_sdk_model.interfaces.display import (
    RenderTemplateDirective, BodyTemplate7, BackButtonBehavior,
    ImageInstance, Image)
from ask_sdk_model.interfaces.connections import SendRequestDirective

import sfn_ctl
import util

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_user_id(handler_input):
    return handler_input.request_envelope.context.system.user.user_id


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        destinations_choice = handler_input.attributes_manager.session_attributes.get(
            'destinations_choice')
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'state': 'launch',
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input)
            }
        response = sfn_ctl.execute(fof_sfn_input)
        if response.get('destinations_choice'):
            handler_input.attributes_manager.session_attributes[
                'destinations_choice'] = response['destinations_choice']
        handler_input.attributes_manager.session_attributes['state'] = \
            response['state']

        if response.get('node'):
            handler_input.attributes_manager.session_attributes['node'] = \
                response['node']

        print(f'response: {response}, type: {type(response)}')
        speech_text = response["response_text"]

        image_url = response.get('image_url')
        bg_image_url = response.get('bg_image_url')
        image_title = response.get('image_title')
        image_text = response.get('image_text')
        if image_url:
            img_obj = Image(sources=[ImageInstance(url=image_url)])
            bg_img_obj = Image(sources=[ImageInstance(url=bg_image_url)])
            if util.is_support_display(handler_input):
                handler_input.response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate7(
                            back_button=BackButtonBehavior.VISIBLE,
                            image=img_obj,
                            background_image=bg_img_obj,
                            title=image_title)
                        )
                    )
            else:
                handler_input.response_builder.set_card(
                    ui.StandardCard(
                        title=image_title,
                        text=image_text,
                        image=ui.Image(
                            small_image_url=image_url,
                            large_image_url=image_url
                            )
                        )
                    )

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(
            response.get('set_should_end_session', True))
        return handler_input.response_builder.response


class DestinationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):  # type: (HandlerInput) -> bool
        return is_intent_name("DestinationIntent")(handler_input)

    def handle(self,
               handler_input):  # type: (HandlerInput) -> Union[None, Response]
        village = handler_input.request_envelope.request.intent.slots[
            'village'].value
        destinations_choice = handler_input.attributes_manager.session_attributes.get(
            'destinations_choice')
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'state': 'Oracle',
            'destination': village,
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input),
            }

        node = handler_input.attributes_manager.session_attributes.get(
            'node')
        if node:
            fof_sfn_input['node'] = node

        response = sfn_ctl.execute(fof_sfn_input)
        speech_text = response["response_text"]

        if response.get('node'):
            handler_input.attributes_manager.session_attributes['node'] = \
                response['node']

        image_url = response.get('image_url')
        if image_url:
            handler_input.response_builder.set_card(
                ui.StandardCard(
                    title='title sample',
                    text='text sample',
                    image=ui.Image(
                        small_image_url=image_url,
                        large_image_url=image_url
                        )
                    )
                )

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(
            response.get('set_should_end_session', True))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': True,
            'intent': 'HelpIntent',
            'destinations_choice':
                handler_input.attributes_manager.session_attributes.get(
                    'destinations_choice'),
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)
        speech_text = response["response_text"]
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': True,
            'intent': 'CancelOrStopIntent',
            'env_type': util.get_env_type(handler_input)
            }
        response = sfn_ctl.execute(fof_sfn_input)
        handler_input.response_builder.speak(response["response_text"])

        image_url = response.get('image_url')
        if image_url:
            handler_input.response_builder.set_card(
                ui.StandardCard(
                    title='title sample',
                    text='text sample',
                    image=ui.Image(
                        small_image_url=image_url,
                        large_image_url=image_url
                        )
                    )
                )

        handler_input.response_builder.set_should_end_session(True)

        return handler_input.response_builder.response


class BuyHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name('BuyIntent')(handler_input)

    def handle(self, handler_input: HandlerInput):
        purchase_product = util.get_purchase_product(
            handler_input, 'product_category')

        if not purchase_product:
            speech_text = 'すみません、分かりませんでした。'
            ask = 'もう一度お願いできますか？'
            handler_input.response_builder.speak(speech_text + ask).ask(
                ask).set_should_end_session(False)
            return handler_input.response_builder.response

        in_skill_response = util.in_skill_product_response(handler_input)
        if not in_skill_response:
            raise ValueError('購入できる商品を見つけられませんでした。')

        skill_product = util.get_skill_product(
            in_skill_response, purchase_product.id)

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name='Buy',
                payload={
                    'InSkillProduct': {
                        'productId': skill_product.product_id
                        }
                    },
                token='correlationToken'
                )
            ).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


# The intent reflector is used for interaction model testing and debugging.
# It will simply repeat the intent the user said. You can create custom handlers
# for your intents by defining them above, then also adding them to the request
# handler chain below.
class IntentReflectorHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = ("You just triggered {}").format(intent_name)
        handler_input.response_builder.speak(
            speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
class ErrorHandler(AbstractExceptionHandler):
    """Catch-all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech_text = "Sorry, I couldn't understand what you said. Please try again."
        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


# This handler acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = StandardSkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DestinationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(BuyHandler())

sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(ErrorHandler())

handler = sb.lambda_handler()
