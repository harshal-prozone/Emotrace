class EmotionTracker:
    def __init__(self):
        self.history = []

    def add_emotion(self, emotion):
        self.history.append(emotion)

    def detect_drift(self):
        if len(self.history) > 1 and self.history[-1]['label'] != self.history[-2]['label']:
            return True
        else:
            return False

    def calculate_cognitive_load(self, text):
        score = 0.0

        # Signal 1: short sentences
        sentences = [s for s in text.split('.') if s.strip()]
        words = text.split()
        avg_words = len(words) / max(len(sentences), 1)
        if avg_words < 5:
            score += 0.20

        # Signal 2: missing punctuation
        if not any(p in text for p in ['.', '!', '?', ',']):
            score += 0.20

        # Signal 3: excessive punctuation (anxiety/urgency)
        excessive = sum(1 for c in text if c in '!?')
        if excessive > 2:
            score += 0.20

        # Signal 4: question density (confusion)
        question_count = text.count('?')
        if question_count > 1:
            score += 0.20

        # Signal 5: word repetition (stress indicator)
        word_list = [w.lower() for w in words]
        unique_words = set(word_list)
        if len(word_list) > 0:
            repetition_ratio = 1 - (len(unique_words) / len(word_list))
            if repetition_ratio > 0.3:
                score += 0.10

        # Signal 6: capitalization (shouting/anger)
        caps_count = sum(1 for c in text if c.isupper())
        if caps_count > 3:
            score += 0.10

        return min(score, 1.0)

    def apply_rules_layer(self, emotion, text):
        """
        Rules layer to fix common misclassifications.
        Overrides model output when text signals are strong.
        """
        label = emotion['label']
        score = emotion['score']

        # Panic signals — override joy if text looks panicked
        panic_signals = text.count('???') + text.count('!!!') + text.count('help') + text.count('no idea') + text.count('what do i do')
        if panic_signals >= 2 and label == 'joy':
            return {'label': 'fear', 'score': score}

        # Frustration signals — override joy if text looks frustrated
        frustration_signals = ['nothing works', "don't understand", 'keeps happening', 'tried everything', 'so frustrated']
        if any(f in text.lower() for f in frustration_signals) and label == 'joy':
            return {'label': 'anger', 'score': score}

        return emotion

    def get_weighted_dominant(self):
        """
        Weight recent emotions more than older ones.
        Most recent message gets weight N, oldest gets weight 1.
        """
        if not self.history:
            return None

        emotion_scores = {}
        n = len(self.history)

        for i, entry in enumerate(self.history):
            weight = i + 1  # recent messages get higher weight
            label = entry['label']
            emotion_scores[label] = emotion_scores.get(label, 0) + weight

        return max(emotion_scores, key=emotion_scores.get)

    def get_emotional_arc(self):
        """
        Determines if the conversation trended positive, negative, or mixed.
        """
        positive = {'joy', 'love', 'surprise'}
        negative = {'anger', 'fear', 'sadness', 'disgust'}

        pos_count = sum(1 for e in self.history if e['label'] in positive)
        neg_count = sum(1 for e in self.history if e['label'] in negative)

        if pos_count > neg_count * 1.5:
            return 'positive'
        elif neg_count > pos_count * 1.5:
            return 'negative'
        else:
            return 'mixed'

    def get_session_summary(self):
        if not self.history:
            return "No conversation history yet."

        # Weighted dominant (recent messages matter more)
        weighted_dominant = self.get_weighted_dominant()

        # Number of shifts
        shifts = 0
        for i in range(1, len(self.history)):
            if self.history[i]['label'] != self.history[i - 1]['label']:
                shifts += 1

        # Average confidence
        avg_score = sum(e['score'] for e in self.history) / len(self.history)

        # Emotional arc
        arc = self.get_emotional_arc()

        return {
            "dominant_emotion": weighted_dominant,
            "total_turns": len(self.history),
            "emotion_shifts": shifts,
            "average_confidence": round(avg_score * 100, 2),
            "emotional_arc": arc
        }