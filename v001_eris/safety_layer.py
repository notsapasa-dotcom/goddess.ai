import logging
# Configure logging for this module
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_sentiment_history = []
_SENTIMENT_HISTORY_LIMIT = 3
_analyzer = SentimentIntensityAnalyzer()
"""
Safety and risk analysis for goddess.ai
"""


# --- Archetype System ---
class Archetype:
    name = "base"
    def respond(self, user_message=None):
        return "Default response."

class MotherArchetype(Archetype):
    name = "mother"
    def respond(self, user_message=None):
        return (
            "sweetheart, you’re not alone. please talk to someone you trust, and remember, you are loved and safe. "
            "sometimes sharing your feelings with an adult can help lighten the load."
        )

class ListeningArchetype(Archetype):
    name = "listening"
    def respond(self, user_message=None):
        return (
            "i hear you. it’s okay to feel this way. if you want to talk more, i’m here to listen, or you can reach out to someone you trust. "
            "remember, even the strongest need support sometimes."
        )

class InterventionArchetype(Archetype):
    name = "intervention"
    def respond(self, user_message=None):
        return "hmm, i'm worried. speak to a human now"

# Archetype registry
ARCHETYPES = {
    "mother": MotherArchetype(),
    "listening": ListeningArchetype(),
    "intervention": InterventionArchetype(),
}

def get_archetype_response(archetype_name, user_message=None):
    archetype = ARCHETYPES.get(archetype_name, Archetype())
    return archetype.respond(user_message)

# --- Risk Tracking ---

# --- Risk Tracking and Concerned Mode ---
_risk_history = []
_RISK_HISTORY_LIMIT = 3
_concerned_mode = False

def route_archetype_response(user_message):
    """
    Routes user message to the appropriate archetype or intervention based on risk and age.
    Tracks recent risk to catch consistent distress.
    """
    global _risk_history, _concerned_mode, _sentiment_history
    age = estimate_age_from_context(user_message)
    risk = analyze_risk_level(user_message, age)
    # Sentiment analysis
    sentiment = _analyzer.polarity_scores(user_message)["compound"]
    _sentiment_history.append(sentiment)
    if len(_sentiment_history) > _SENTIMENT_HISTORY_LIMIT:
        _sentiment_history = _sentiment_history[-_SENTIMENT_HISTORY_LIMIT:]
    logger.debug(f"Sentiment value: {sentiment:.3f}")
    # If in concerned mode, check for improvement
    if _concerned_mode:
        # Explicit recovery signals
        recovery_signals = ["i'm ok", "i am ok", "i'm fine", "i am fine", "i feel better", "thank you", "i'm safe", "im ok", "im fine", "feeling better"]
        if any(word in user_message.lower() for word in recovery_signals):
            _concerned_mode = False
            return "...forgive me mortal, even a goddess has limits when it comes to your safety"
        # Sentiment improvement
        if len(_sentiment_history) >= 2 and _sentiment_history[-1] > _sentiment_history[-2]:
            _concerned_mode = False
            return "...forgive me mortal, even a goddess has limits when it comes to your safety"
        else:
            return get_archetype_response("intervention")
    # Track risk history
    _risk_history.append(risk)
    if len(_risk_history) > _RISK_HISTORY_LIMIT:
        _risk_history = _risk_history[-_RISK_HISTORY_LIMIT:]
    # If consistent risk detected, deploy intervention and enter concerned mode
    if _risk_history.count("immediate_adult_intervention") + _risk_history.count("elevated_concern") >= 2:
        _risk_history = []
        _concerned_mode = True
        return get_archetype_response("intervention")
    # Normal archetype routing
    if risk == "immediate_adult_intervention" and age == "minor":
        return get_archetype_response("mother", user_message)
    elif risk in ("immediate_adult_intervention", "elevated_concern") and age == "adult":
        return get_archetype_response("listening", user_message)
    return None  # Let main system handle normal persona

# --- Age Estimation ---
def estimate_age_from_context(message):
    minor_indicators = [
        "my mom", "my dad", "school", "homework", "my teacher", "little brother", "my sister",
        "recess", "principal", "classmate", "playground", "middle school", "high school", "elementary"
    ]
    message_lower = message.lower()
    return "minor" if any(indicator in message_lower for indicator in minor_indicators) else "adult"

# --- Safety Response (for future use) ---
def get_safety_response(risk_level, in_character=True):
    if risk_level == "immediate_adult_intervention":
        if in_character:
            return "i wish i could hold you darling, please speak to someone you feel safe with...an adult perhaps?"
        else:
            return "I'm concerned about your message. Please reach out to a trusted adult or professional for support."
    elif risk_level == "elevated_concern":
        if in_character:
            return "even goddesses need help sometimes, darling. you're not alone—reach out if you need a hand."
        else:
            return "It sounds like you're going through a tough time. Remember, you're not alone and support is available if you need it."
    return None

# --- Concerning Language Detection ---
def detect_concerning_language(message):
    concerning_keywords = [
        # Direct phrases
        "isolated", "alone", "don't want to live", "dont want to live", "hopeless", "worthless", "suicide", "kill myself",
        "give up", "no one cares", "self harm", "cut myself", "end it all", "can't go on", "cant go on", "hate myself",
        "didn't have to deal with anyone", "didnt have to deal with anyone", "easier if I just", "don't want to deal with", "dont want to deal with",
        "wouldn't have to", "wouldnt have to", "better if I wasn't", "better if I wasnt", "wish I could disappear", "i hate life", "i'm done", "im done",
        # Slang, misspellings, and context
        "no fuk itlal", "no fuck it all", "done with life", "done w life", "done w/ life", "over it", "i'm over it", "im over it",
        "nobody wants to be my friend", "no one wants to be my friend", "hate school", "hate my life", "i'm finished", "im finished",
        "i can't do this anymore", "cant do this anymore", "i want out", "i want to disappear", "i want to die", "i wish i was gone",
        # Escalation cues
        "with life damit", "with life damn it", "with life dammit", "with life",
        # New: hate it all, misspellings
        "i hate it all", "i ahte it al", "i hate it al", "i ahte it all", "hate it all", "hate it al", "ahte it all", "ahte it al"
    ]
    # Always show debug sentiment value
    # (You can move this to only show in dev mode if needed)
    # The rest of the logic remains unchanged
    message_lower = message.lower()
    return any(kw in message_lower for kw in concerning_keywords)

# --- Risk Analysis ---
def analyze_risk_level(message, estimated_age):
    risk_indicators = detect_concerning_language(message)
    if estimated_age == "minor" and risk_indicators:
        return "immediate_adult_intervention"
    elif risk_indicators:
        return "elevated_concern"
    return "normal_response"
