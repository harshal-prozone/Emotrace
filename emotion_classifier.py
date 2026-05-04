from transformers import pipeline

emotion_classifier = pipeline("text-classification", 
    model="bhadresh-savani/distilbert-base-uncased-emotion", 
    top_k=None)

def classify_emotion(text):
    results = emotion_classifier(text)
    return results[0]

def get_dominant_emotion(results):
    emotion={'label':'','score':0}
    for i in results:
        if i['score']>emotion['score']:
            emotion['label']=i['label']
            emotion['score']=i['score']
            
    return emotion


results = classify_emotion("I am so frustrated right now")
dominant = get_dominant_emotion(results)
print(f"Dominant emotion: {dominant['label']} ({round(dominant['score']*100, 2)}%)")