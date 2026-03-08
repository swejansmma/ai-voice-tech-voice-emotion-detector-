from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
analyzer = SentimentIntensityAnalyzer()
INTENTS = {
    "account inquiry": ["account", "profile", "login", "password", "details", "sign in", "user", "access"],
    "billing dispute": ["charge", "billed", "invoice", "refund", "overcharge", "double", "money", "payment", "cost", "fee"],
    "payment issue": ["pay", "card", "decline", "visa", "mastercard", "transaction", "bank", "checking"],
    "technical support": ["broken", "error", "bug", "not working", "fail", "slow", "freeze", "crash", "website"],
    "service complaint": ["bad", "terrible", "unhappy", "resolving", "wait", "useless", "disappointed", "poor"]
}
TOPICS = {
    "credit card charges": ["card", "charged", "credit", "bank", "statement"],
    "account access issues": ["login", "password", "locked", "reset", "email"],
    "subscription cancellation": ["cancel", "unsubscribe", "stop", "membership", "billing cycle"],
    "service outage": ["down", "offline", "unavailable", "server", "connectivity"]
}
TONES = {
    "angry": ["angry", "mad", "frustrated", "hate", "terrible", "worst", "unacceptable", "ridiculous", "fix"],
    "happy": ["happy", "great", "thanks", "awesome", "good", "solved", "love", "perfect", "appreciate"],
    "confused": ["why", "how", "what", "question", "confused", "understand", "explain"],
    "urgent": ["immediately", "now", "quick", "asap", "hurry", "urgent", "fast", "priority", "emergency"]
}
ESCALATION_PHRASES = ["manager", "not been resolved", "unacceptable", "immediately", "legal", "lawsuit", "supervisor", "complain", "better support"]
def get_best_match(text, mapping, default="unknown"):
    scores = {k: 0 for k in mapping}
    for category, keywords in mapping.items():
        for kw in keywords:
            if re.search(rf'\b{kw}\b', text):
                scores[category] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else default
def analyze_conversation(full_text: str):
    text_lower = full_text.lower()
    vs = analyzer.polarity_scores(full_text)
    compound = vs['compound']
    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    intent = get_best_match(text_lower, INTENTS, "general inquiry")
    topic = get_best_match(text_lower, TOPICS, "general service")
    tone = get_best_match(text_lower, TONES, "neutral")
    risk = "low"
    for p in ESCALATION_PHRASES:
        if p in text_lower:
            risk = "high"
            break
    return {
        "intent": intent,
        "topic": topic,
        "sentiment": sentiment,
        "tone": tone,
        "escalation_risk": risk
    }
