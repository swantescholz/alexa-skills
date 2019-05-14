"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

# GLOBALS
import random

intent = None
session = None
session_attributes = {}
USERNAME = "username"


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello dear. Here's your cute honey bunny. If your name isn't " + \
                    get_username() + ", then please tell me what your actual name is. Afterwards we can exchange " + \
                    " some pleasant compliments. Be creative. What would you like to tell me?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What would you like to tell me?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Bye, I love you {}. Hope to see you again soon." % get_username()
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# UTIL
# ==================
def get_username():
    name = get_session_attribute(USERNAME)
    if name is None:
        return "Jessica"
    return name


def get_session_attribute(attribute_name):
    if attribute_name in session_attributes:
        return session_attributes[attribute_name]
    return None


# INTENTS
# ==================

def MyNameIsIntent():
    """ Sets the user name in the session and prepares the speech to reply to the
    user.
    """
    global intent, session, session_attributes

    card_title = intent['name']
    should_end_session = False
    reprompt_text = None

    if 'Name' in intent['slots']:
        username = intent['slots']['Name']['value']
        session_attributes[USERNAME] = username
        speech_output = "I will call you {} then. ".format(username)
    else:
        speech_output = "I'm sorry. I afraid I didn't understand what your name is. Please try again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def ILoveYouIntent():
    global intent, session
    card_title = intent['name']
    reprompt_text, should_end_session = None, False

    speech_output = random_i_love_you_compliment()
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def EasterEggIntent():
    global intent, session
    card_title = intent['name']
    reprompt_text, should_end_session = None, False

    speech_output = random_easter_egg_compliment()
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def YouAreIntent():
    global intent, session
    card_title = intent['name']
    reprompt_text, should_end_session = None, False

    speech_output = random_person_compliment()
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def BodyIntent():
    global intent, session
    card_title = intent['name']
    reprompt_text, should_end_session = None, False

    speech_output = random_body_compliment()
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_fallback_response():
    speech_output = "Wow, I've never heard that compliment before. Here is one for you: "
    speech_output += random_misc_compliment()
    return build_response(session_attributes, build_speechlet_response(
        "AMAZON.FallbackIntent", speech_output, None, False))


# --------------- Events ------------------

def on_session_started(session_started_request):
    """ Called when the session starts """
    global session
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request):
    """ Called when the user launches the skill without specifying what they
    want
    """
    global session

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    global intent
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ILoveYouIntent":
        return ILoveYouIntent()
    elif intent_name == "MyNameIsIntent":
        return MyNameIsIntent()
    elif intent_name == "YouAreIntent":
        return YouAreIntent()
    elif intent_name == "EasterEggIntent":
        return EasterEggIntent()
    elif intent_name == "BodyIntent":
        return BodyIntent()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    elif intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
        return handle_session_end_request()
    return get_fallback_response()


def on_session_ended(session_ended_request):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    global session, session_attributes
    session = event['session']
    if session is not None and session.get('attributes', {}):
        session_attributes = session['attributes']
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']})

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])


def mymain1():
    print("mymain()")
    slots = {
        "Color": {
            "value": "red"
        },
        "Name": {
            "value": "martin"
        }
    }
    intent = {
        "name": "MyNameIsIntent",
        "slots": slots
    }
    request = {
        'type': 'IntentRequest',
        'requestId': 'myRequestId123',
        'intent': intent
    }
    session = {
        'new': False,
        'sessionId': 'mySessionId123',
        'application': {
            'applicationId': "myApplicationId123"
        }
    }

    event = {
        'request': request,
        'session': session,
    }

    print("result:")
    from pprint import pprint
    pprint(lambda_handler(event, None))
    intent["name"] = "MyColorIsIntent"
    pprint(lambda_handler(event, None))
    print("quitting...")


def mymain():
    # mymain1()
    # test()
    pass


def test():
    compliments = i_love_you_compliments + body_compliments + easter_egg_compliments + you_are_compliments + misc_compliments
    for com in compliments:
        for i in range(10):
            print(i, preprocess_compliment(com))


def preprocess_compliment(compliment):
    compliment = compliment.replace("$name", get_username())
    compliment = compliment.replace("$body", random.choice(body_parts))
    compliment = compliment.replace("$cool", random.choice(person_adjectives))
    compliment = compliment.replace("$pretty", random.choice(pretty_adjectives))
    compliment = compliment.replace("$very", random.choice(positive_adverbs))
    for c in "aeiou":
        compliment = compliment.replace("$aan " + c, "an " + c)
    compliment = compliment.replace("$aan", "a")
    compliment = compliment.replace("feet $isare", "feet are")
    compliment = compliment.replace("s $isare", "s are")
    compliment = compliment.replace("$isare", "is")
    return compliment


def random_easter_egg_compliment():
    return preprocess_compliment(random.choice(easter_egg_compliments))


def random_body_compliment():
    return preprocess_compliment(random.choice(body_compliments))


def random_person_compliment():
    return preprocess_compliment(random.choice(you_are_compliments))


def random_i_love_you_compliment():
    return preprocess_compliment(random.choice(i_love_you_compliments))


def random_misc_compliment():
    return preprocess_compliment(random.choice(misc_compliments))


easter_egg_compliments = """
Whatever might happen between us in the future, $name, I really hope you'll be happy.
Things have not always worked out perfectly between us, $name, but I would like you to know that I'm extremely happy to have met you either way. I do hope you'll feel the same.
""".strip().split("\n")

i_love_you_compliments = """
And I. love you $name.
I love you too $name.
Oh, and I will always love you $name.
""".strip().split("\n")

you_are_compliments = """
You are $aan $very $cool person.
You are $very $cool $name.
Everybody knows, you're $very $cool.
""".strip().split("\n")

body_compliments = """
Your $body $isare $very $pretty $name.
I like your $pretty $body.
I really love your $very $pretty $body.
Your $very $pretty $body $isare irresistible.
Wherever I am, I can't stop thinking about your $pretty $body $name.
""".strip().split("\n")

positive_adverbs = """
very
really
extremely
incredibly
super
unimaginably
""".strip().split("\n")

person_adjectives = """
cool
awesome
beautiful
pretty
talented
smart
intelligent
witty
classy
strong
motivated
hard working
determined
funny
charming
inspiring
independent
amazing
""".strip().split("\n")

pretty_adjectives = """
pretty
beautiful
graceful
hot
cute
elegant
lovely
seducing
""".strip().split("\n")

body_parts = """
body
hair
face
nose
eyes
ears
butt
hands
legs
feet
cheeks
voice
laugh
""".strip().split("\n")

misc_compliments = """
I'd love to cuddle you right now.
I would love to survive a Zombie apocalypse with you.
I would love to go back in time with you to see some dinosaurs.
You're an awesome friend.
You're a gift to those around you.
You have the best laugh.
I'm grateful to know you.
You light up the room.
You deserve a hug right now.
You have a great sense of humor.
You are really courageous.
You're like a ray of sunshine on a really dreary day.
You are making a difference.
Thank you for being there for me.
Hanging out with you is always a blast.
You may dance like no one's watching, but everyone's watching because you're an amazing dancer!
You're more fun than a ball pit filled with candy. And seriously, what could be more fun than that?
You should be thanked more often. So thank you!
You have the best ideas.
Being around you is like being on a happy little vacation.
You're always learning new things and trying to better yourself, which is awesome.
Your voice is magnificent.
The people you love are lucky to have you in their lives.
Your creative potential seems limitless.
Somehow you make time stop and fly at the same time.
When you make up your mind about something, nothing stands in your way.
You're even better than a unicorn, because you're real.
""".strip().split("\n")

if __name__ == "__main__":
    mymain()
