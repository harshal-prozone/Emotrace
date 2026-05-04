
class EmotionTracker:
    def __init__(self):
        self.history=[]
    def add_emotion(self,emotion):
        self.history.append(emotion)
    def detect_drift(self):
        if len(self.history)>1 and self.history[-1]['label']!=self.history[-2]['label']:
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
            score += 0.25
        
        # Signal 2: missing punctuation
        if not any(p in text for p in ['.', '!', '?', ',']):
            score += 0.25
        
        # Signal 3: excessive punctuation
        excessive = sum(1 for c in text if c in '!?')
        if excessive > 2:
            score += 0.25
        
        # Signal 4: question density
        question_count = text.count('?')
        if question_count > 1:
            score += 0.25
        
        return min(score, 1.0)
    
    def get_session_summary(self):
        if not self.history:
            return "No conversation history yet."
        
        # Most frequent emotion
        emotion_counts = {}
        for e in self.history:
            label = e['label']
            emotion_counts[label] = emotion_counts.get(label, 0) + 1
        dominant = max(emotion_counts, key=emotion_counts.get)
        
        # Number of shifts
        shifts = 0
        for i in range(1, len(self.history)):
            if self.history[i]['label'] != self.history[i-1]['label']:
                shifts += 1
        
        # Average score of dominant emotion
        avg_score = sum(e['score'] for e in self.history) / len(self.history)
        
        return {
            "dominant_emotion": dominant,
            "total_turns": len(self.history),
            "emotion_shifts": shifts,
            "average_confidence": round(avg_score * 100, 2)
        }