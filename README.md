# EmoTrace — Emotion-Aware Dialogue Agent

## What is this?

EmoTrace is a conversational system that tracks the emotional state of a user **across multiple turns** of a dialogue — not just per message. Most emotion detection systems treat each message independently. EmoTrace maintains a running model of emotional trajectory, detecting when emotions shift, measuring cognitive load from text features, and summarising the emotional arc of an entire conversation.

## Research Question

> Can a system build a continuous model of a user's emotional state across a conversation, and use that trajectory — rather than isolated per-message signals — to better understand human cognitive and emotional experience?

## Key Features

- **Per-message emotion classification** using a pretrained DistilBERT transformer model
- **Emotion drift detection** — identifies when emotional state shifts between turns
- **Cognitive load estimation** — scores mental stress from text features (sentence length, punctuation patterns, word repetition, capitalisation)
- **Rules layer** — overrides model misclassifications using contextual text signals
- **Weighted dominant emotion** — recent messages are weighted more heavily than older ones
- **Emotional arc** — classifies the overall conversation as positive, negative, or mixed
- **Session summary** — aggregates all of the above into a end-of-conversation report

## Project Structure

```
Emotrace/
├── emotion_classifier.py   # ML layer — loads and runs DistilBERT emotion model
├── emotion_tracker.py      # Research layer — drift, cognitive load, arc, summary
├── app.py                  # Flask backend — connects classifier and tracker
├── templates/
│   └── index.html          # Frontend interface
└── README.md
```

## Installation

```bash
pip3 install transformers torch flask
```

## Running the Project

```bash
python3 app.py
```

Then open your browser at:

```
http://localhost:5000
```

## Model Used

`bhadresh-savani/distilbert-base-uncased-emotion` — a DistilBERT model fine-tuned for 6-class emotion classification: joy, sadness, anger, fear, love, surprise.

## Limitations & Future Work

- The ML model occasionally misclassifies panic as joy due to exclamation marks — partially addressed by the rules layer but not fully solved
- Cognitive load is heuristic-based, not learned — a future version could train a model on labelled cognitive load data
- Currently English-only — extending to low-resource Indian languages (Kannada, Hindi) is a planned direction
- No user evaluation conducted yet — collecting real conversation data and measuring system accuracy against human labels is the next step

## Authors

C. Harshal Rajesh — PES University, CSE, 2024–2028
