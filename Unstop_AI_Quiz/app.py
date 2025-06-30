from flask import Flask, render_template, request, jsonify
import os
import re
from google import genai

app = Flask(__name__)

# Configure Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyDpK2sm3b7P7tveTkLQL7sOxfNbzy-enrc"))

def generate_quiz(topic, num_questions):
    quiz = []
    for _ in range(num_questions):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
            Create a multiple choice question about {topic} with exactly four options (A-D). 
            Follow this exact format:

            **Question:** [Your question here]
            A) [Option A]
            B) [Option B]
            C) [Option C]
            D) [Option D]
            **Correct Answer:** [Letter only: A/B/C/D]
            """
        )
        
        raw_text = response.text.strip()
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

        question = None
        for i, line in enumerate(lines):
            if "**Question:**" in line:
                question = line.replace("**Question:**", "").strip()
                if not question and i+1 < len(lines):
                    question = lines[i+1].strip()
                break

        options = []
        option_pattern = re.compile(r'^[A-D][).]\s*')
        for line in lines:
            if option_pattern.match(line):
                cleaned_option = option_pattern.sub('', line).strip()
                options.append(cleaned_option)
                if len(options) == 4:
                    break

        if len(options) != 4:
            continue

        correct_letter = None
        for line in reversed(lines):
            if "correct answer" in line.lower():
                match = re.search(r'\b([A-D])\b', line, re.IGNORECASE)
                if match:
                    correct_letter = match.group(1).upper()
                    break

        if not correct_letter:
            continue

        try:
            correct_index = ord(correct_letter) - ord('A')
            correct_answer = options[correct_index]
        except (IndexError, TypeError):
            continue

        quiz.append({
            'question': question,
            'options': options,
            'correct_index': correct_index
        })

    return quiz

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/aptitude/<topic>')
def aptitude(topic):
    return render_template("aptitude.html", topic=topic)

@app.route('/reasoning/<topic>')
def reasoning(topic):
    return render_template("reasoning.html", topic=topic)

@app.route('/grammar/<topic>')
def grammar(topic):
    return render_template("grammar.html", topic=topic)

@app.route('/quantitative/<topic>')
def quantitative(topic):
    return render_template("quantitative.html", topic=topic)


@app.route('/instruction/<topic>')
def instruction(topic):
    return render_template("instruction.html", topic=topic)


@app.route('/test/<topic>')
def test(topic):
    quiz = generate_quiz(topic, 5)
    return render_template("test.html", quiz=quiz, topic=topic)


if __name__ == "__main__":
    app.run(debug=True)