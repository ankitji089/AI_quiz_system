import requests
import json
import re
import random

API_KEY = "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"


def extract_json(text):
    """
    Extract JSON safely from AI response
    """
    text = text.replace("```json", "").replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return json.loads(match.group())

    raise Exception("JSON parsing failed")


def shuffle_options(data):
    """
    Shuffle options so correct answer is not always same position
    """

    options = list(data["options"].items())
    random.shuffle(options)

    new_options = {}
    letters = ["A", "B", "C", "D"]

    correct_text = data["options"][data["correct_answer"]]

    for i, (_, value) in enumerate(options):

        new_options[letters[i]] = value

        if value == correct_text:
            data["correct_answer"] = letters[i]

    data["options"] = new_options

    return data


def generate_question(level):

    # difficulty logic
    if level <= 3:
        difficulty = "easy"
    elif level <= 6:
        difficulty = "medium"
    else:
        difficulty = "hard"

    # random topic selection
    topic = random.choice([
        "VOR navigation",
        "GPS navigation",
        "METAR weather reports",
        "air pressure systems",
        "wind direction in aviation",
        "dead reckoning navigation",
        "instrument landing system (ILS)",
        "altitude measurement",
        "weather fronts",
        "runway wind limitations",
        "aviation turbulence",
        "flight dispatch planning"
    ])

    prompt = f"""
You are an aviation instructor creating questions for Flight Dispatcher training.

Topic: {topic}

Difficulty Level: {difficulty}

Difficulty rules:
- EASY: Basic aviation definitions or simple concepts.
- MEDIUM: Practical aviation understanding or interpretation questions.
- HARD: Scenario-based aviation questions requiring decision-making.

Rules:
- Generate ONE unique multiple choice question.
- Correct answer must be randomly A, B, C, or D.
- Options must be realistic aviation-related answers.
- Avoid repeating common questions like simple VOR definitions.

Return ONLY JSON in this format:

{{
"question": "",
"options": {{
"A": "",
"B": "",
"C": "",
"D": ""
}},
"correct_answer": "",
"explanation": ""
}}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "AI Adaptive Quiz"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9
        }
    )

    result = response.json()

    print("AI RESPONSE:", result)

    if "choices" not in result:
        raise Exception("AI API error: " + str(result))

    text = result["choices"][0]["message"]["content"]

    data = extract_json(text)

    # shuffle options
    data = shuffle_options(data)

    return data