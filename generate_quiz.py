import streamlit as st
from google import genai
import os
import re

def initialize_session_state():
    if 'quiz' not in st.session_state:
        st.session_state.quiz = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'quiz_finished' not in st.session_state:
        st.session_state.quiz_finished = False

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

            Example:
            **Question:** What is the capital of France?
            
            A) London
            B) Berlin
            C) Paris
            D) Madrid
            
            **Correct Answer:** C
            """
        )
        
        raw_text = response.text.strip()
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        
        # Debugging line to see raw response
        # print("Raw response lines:", lines)
        # Extract question
        question = None
        for i, line in enumerate(lines):
            if "**Question:**" in line:
                question = line.replace("**Question:**", "").strip()
                if not question and i+1 < len(lines):
                    question = lines[i+1].strip()
                break

        # Extract options with more robust pattern
        options = []
        option_pattern = re.compile(r'^[A-D][).]\s*')
        for line in lines:
            if option_pattern.match(line):
                cleaned_option = option_pattern.sub('', line).strip()
                options.append(f"{chr(65 + len(options))}) {cleaned_option}")
                if len(options) == 4:
                    break

        # Ensure exactly 4 options
        if len(options) != 4:
            continue  # Skip this question and retry

        # Extract correct answer with flexible matching
        correct_letter = None
        for line in reversed(lines):
            if "correct answer" in line.lower():
                match = re.search(r'\b([A-D])\b', line, re.IGNORECASE)
                if match:
                    correct_letter = match.group(1).upper()
                    break

        if not correct_letter:
            continue  # Skip invalid questions

        # Map letter to full option text
        try:
            correct_index = ord(correct_letter) - ord('A')
            correct_answer = options[correct_index]
        except (IndexError, TypeError):
            continue  # Handle invalid letter mapping

        quiz.append({
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        })
    
    return quiz

def display_question(question_idx):
    question = st.session_state.quiz[question_idx]
    with st.container(border=True):
        st.markdown(f"### 📝 Question {question_idx + 1}")
        st.markdown(f"**{question['question']}**")
        
        cols = st.columns(2)
        option_indices = {}
        for idx, option in enumerate(question['options']):
            with cols[idx % 2]:
                if st.button(
                    f"🔘 {option}",
                    key=f"q{question_idx}_opt{idx}",
                    use_container_width=True
                ):
                    st.session_state.user_answers[question_idx] = idx
                    handle_answer_selection(question_idx, idx)

def handle_answer_selection(question_idx, selected_idx):
    question = st.session_state.quiz[question_idx]
    if question['options'][selected_idx] == question['correct_answer']:
        st.session_state.player_score += 1
    if question_idx < len(st.session_state.quiz) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.quiz_finished = True
    st.rerun()

def show_progress():
    progress = (st.session_state.current_question + 1) / len(st.session_state.quiz)
    st.progress(progress, text=f"📊 Progress: Question {st.session_state.current_question + 1} of {len(st.session_state.quiz)}")

def quiz_app():
    st.set_page_config(page_title="AI Quiz Master", page_icon="🧠")
    st.markdown("""
        <style>
        .stButton button {
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 AI Quiz Master with Gemini")
    initialize_session_state()

    with st.expander("⚙️ Quiz Settings", expanded=True):
        topic = st.text_input("📚 Enter quiz topic:")
        num_questions = st.number_input("🔢 Number of questions:", min_value=1, max_value=10)

    if st.button("🚀 Generate Quiz", use_container_width=True):
        if topic and num_questions > 0:
            st.session_state.quiz = generate_quiz(topic, num_questions)
            st.session_state.current_question = 0
            st.session_state.player_score = 0
            st.session_state.user_answers = [None] * num_questions
            st.session_state.quiz_finished = False
            st.rerun()
        else:
            st.error("❌ Please enter both a topic and number of questions")

    if st.session_state.quiz and not st.session_state.quiz_finished:
        show_progress()
        display_question(st.session_state.current_question)

    if st.session_state.quiz_finished:
        st.balloons()
        st.success(f"🏆 Quiz Completed! Final Score: {st.session_state.player_score}/{len(st.session_state.quiz)}")
        
        for i, question in enumerate(st.session_state.quiz):
            with st.container(border=True):
                st.markdown(f"### 📋 Question {i+1}")
                st.markdown(f"**{question['question']}**")
                
                user_answer_idx = st.session_state.user_answers[i]
                if user_answer_idx is not None:
                    user_answer = question['options'][user_answer_idx]
                    correct = user_answer == question['correct_answer']
                    icon = "✅" if correct else "❌"
                    
                    cols = st.columns(2)
                    with cols[0]:
                        st.markdown(f"{icon} **Your Answer:** {user_answer}")
                    with cols[1]:
                        st.markdown(f"📚 **Correct Answer:** {question['correct_answer']}")
                else:
                    st.warning("⚠️ No answer selected")

quiz_app()