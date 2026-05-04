from flask import Flask, request, jsonify, render_template
from emotion_classifier import classify_emotion, get_dominant_emotion
from emotion_tracker import EmotionTracker

app = Flask(__name__)
tracker = EmotionTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.json
    text = data.get('message', '')

    if not text:
        return jsonify({'error': 'No message provided'}), 400

    # Step 1: classify emotion
    results = classify_emotion(text)

    # Step 2: get dominant emotion
    dominant = get_dominant_emotion(results)

    # Step 3: calculate cognitive load
    cognitive_load = tracker.calculate_cognitive_load(text)

    # Step 4: add to tracker history
    tracker.add_emotion(dominant)

    # Step 5: detect drift
    drift = tracker.detect_drift()

    # Step 6: get session summary
    summary = tracker.get_session_summary()

    return jsonify({
        'message': text,
        'all_emotions': results,
        'dominant_emotion': dominant['label'],
        'confidence': round(dominant['score'] * 100, 2),
        'cognitive_load': round(cognitive_load * 100, 2),
        'drift_detected': drift,
        'session_summary': summary
    })

@app.route('/reset', methods=['POST'])
def reset():
    global tracker
    tracker = EmotionTracker()
    return jsonify({'status': 'Session reset'})

if __name__ == '__main__':
    app.run(debug=True)