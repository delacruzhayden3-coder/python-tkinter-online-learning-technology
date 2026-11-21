import tkinter as tk
from tkinter import messagebox
import random
import os

QUESTIONS = [
    {"question": "What is the main purpose of an online learning platform?",
     "choices": ["A. To support learning through the internet", "B. To repair computer hardware", "C. To create printed newspapers", "D. To replace electricity"],
     "answer": "A"},
    {"question": "Which of these is an example of a Learning Management System (LMS)?",
     "choices": ["A. Paint", "B. Moodle", "C. Calculator", "D. File Explorer"],
     "answer": "B"},
    {"question": "What does synchronous online learning mean?",
     "choices": ["A. Students study without any materials", "B. Students learn only from books", "C. Teachers and students meet online at the same time", "D. Students submit work once a year"],
     "answer": "C"},
    {"question": "Which tool is commonly used for live online classes?",
     "choices": ["A. Disk Cleanup", "B. Notepad", "C. File Manager", "D. Zoom"],
     "answer": "D"},
    {"question": "What is an advantage of asynchronous learning?",
     "choices": ["A. Learners can access lessons at a flexible time", "B. Everyone must log in at exactly the same time", "C. It does not use learning materials", "D. It prevents students from reviewing lessons"],
     "answer": "A"},
    {"question": "Why should students use strong passwords for learning accounts?",
     "choices": ["A. To make the screen brighter", "B. To protect their accounts and personal information", "C. To increase internet speed", "D. To remove assignments"],
     "answer": "B"},
    {"question": "Which action shows good digital citizenship during an online class?",
     "choices": ["A. Sharing another student's password", "B. Posting insulting comments", "C. Respecting others and communicating politely", "D. Interrupting every speaker"],
     "answer": "C"},
    {"question": "What is the purpose of a discussion forum in an online course?",
     "choices": ["A. To shut down the learning platform", "B. To change computer settings", "C. To store music files only", "D. To share ideas and ask questions"],
     "answer": "D"},
    {"question": "Which is a useful way to check whether information online is reliable?",
     "choices": ["A. Check the author, date, evidence, and source", "B. Believe every post immediately", "C. Choose the first result without checking", "D. Ignore the source"],
     "answer": "A"},
    {"question": "What should a student do if the internet connection fails during an online lesson?",
     "choices": ["A. Delete the course account", "B. Reconnect and contact the teacher if needed", "C. Share their password publicly", "D. Stop studying permanently"],
     "answer": "B"},
]

TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")

BG = "#F3F5FF"
CARD = "#FFFFFF"
NAVY = "#202A44"
PURPLE = "#6750A4"
BLUE = "#4263EB"
GREEN = "#16865B"
RED = "#D64545"
MUTED = "#68738A"

root = tk.Tk()
root.title("Online Learning Technology Quiz")
root.geometry("820x700")
root.configure(bg=BG)
root.resizable(False, False)

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=34, pady=24)

quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
selected_answer = tk.StringVar()

timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0
    return 0

def save_high_score(new_score):
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
            file.write(str(new_score))
        return True
    return False

def clear_screen():
    for widget in main.winfo_children():
        widget.destroy()

def get_choice_text(question, letter):
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"

def make_label(parent, text, size=12, color=NAVY, bold=False, **kwargs):
    return tk.Label(parent, text=text, font=("Arial", size, "bold" if bold else "normal"),
                    bg=kwargs.pop("bg", CARD), fg=color, **kwargs)

def show_start_screen():
    clear_screen()
    card = tk.Frame(main, bg=CARD, highlightthickness=1, highlightbackground="#E1E5F2")
    card.pack(fill="both", expand=True)
    tk.Label(card, text="✦  LEARN • PLAY • GROW  ✦", font=("Arial", 11, "bold"),
             bg=CARD, fg=PURPLE).pack(pady=(52, 18))
    tk.Label(card, text="ONLINE LEARNING", font=("Arial", 29, "bold"),
             bg=CARD, fg=NAVY).pack()
    tk.Label(card, text="TECHNOLOGY QUIZ", font=("Arial", 29, "bold"),
             bg=CARD, fg=BLUE).pack(pady=(0, 16))
    tk.Label(card, text="Test your knowledge of digital learning tools, online classes,",
             font=("Arial", 12), bg=CARD, fg=MUTED).pack()
    tk.Label(card, text="internet safety, and effective learning practices.",
             font=("Arial", 12), bg=CARD, fg=MUTED).pack(pady=(2, 25))

    info = tk.Frame(card, bg="#F0F2FF", padx=25, pady=18)
    info.pack(pady=8)
    tk.Label(info, text="10 QUESTIONS     •     4 CHOICES EACH     •     15 SECONDS",
             font=("Arial", 11, "bold"), bg="#F0F2FF", fg=NAVY).pack()
    tk.Label(card, text=f"PERSONAL BEST: {get_high_score()} / 10",
             font=("Arial", 14, "bold"), bg=CARD, fg=GREEN).pack(pady=22)
    tk.Button(card, text="START QUIZ  →", font=("Arial", 13, "bold"),
              bg=PURPLE, fg="white", activebackground=BLUE, activeforeground="white",
              relief="flat", padx=30, pady=13, cursor="hand2",
              command=start_quiz).pack(pady=10)
    tk.Label(card, text="Choose an answer before the timer reaches zero.",
             font=("Arial", 10), bg=CARD, fg=MUTED).pack(pady=(18, 0))

def start_quiz():
    global quiz_questions, current_question, score, wrong_answers
    stop_timer()
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()

def show_question():
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons
    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    header = tk.Frame(main, bg=BG)
    header.pack(fill="x", pady=(0, 14))
    tk.Label(header, text="ONLINE LEARNING TECHNOLOGY", font=("Arial", 11, "bold"),
             bg=BG, fg=PURPLE).pack(side="left")
    tk.Label(header, text=f"SCORE  {score}", font=("Arial", 11, "bold"),
             bg=BG, fg=NAVY).pack(side="right")

    card = tk.Frame(main, bg=CARD, padx=30, pady=24,
                    highlightthickness=1, highlightbackground="#E1E5F2")
    card.pack(fill="both", expand=True)

    top = tk.Frame(card, bg=CARD)
    top.pack(fill="x")
    tk.Label(top, text=f"QUESTION {current_question + 1} OF 10",
             font=("Arial", 11, "bold"), bg=CARD, fg=BLUE).pack(side="left")
    timer_label = tk.Label(top, text="", font=("Arial", 12, "bold"),
                           bg="#FFF0F0", fg=RED, padx=12, pady=7)
    timer_label.pack(side="right")

    progress = tk.Frame(card, bg="#E8EBF5", height=8)
    progress.pack(fill="x", pady=(18, 28))
    progress.pack_propagate(False)
    tk.Frame(progress, bg=BLUE, width=int(700 * (current_question + 1) / 10)).pack(side="left", fill="y")

    tk.Label(card, text=question["question"], font=("Arial", 19, "bold"),
             bg=CARD, fg=NAVY, wraplength=690, justify="left",
             anchor="w").pack(fill="x", pady=(0, 24))

    tk.Label(card, text="SELECT ONE ANSWER", font=("Arial", 10, "bold"),
             bg=CARD, fg=MUTED).pack(anchor="w", pady=(0, 10))

    global choice_buttons
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        rb = tk.Radiobutton(card, text=choice, variable=selected_answer, value=letter,
                            font=("Arial", 12), bg="#F7F8FC", fg=NAVY,
                            activebackground="#EEF0FF", selectcolor="#DDE3FF",
                            anchor="w", padx=14, pady=11, relief="flat",
                            highlightthickness=0, wraplength=660, justify="left")
        rb.pack(fill="x", pady=5)
        choice_buttons.append(rb)

    feedback_label = tk.Label(card, text="", font=("Arial", 11, "bold"),
                              bg=CARD, fg=GREEN, wraplength=680)
    feedback_label.pack(pady=12)

    buttons = tk.Frame(card, bg=CARD)
    buttons.pack(pady=(4, 0))
    submit_button = tk.Button(buttons, text="SUBMIT ANSWER", font=("Arial", 11, "bold"),
                              bg=PURPLE, fg="white", relief="flat", padx=22, pady=10,
                              cursor="hand2", command=submit_answer)
    submit_button.pack(side="left", padx=8)
    next_button = tk.Button(buttons, text="NEXT  →" if current_question < 9 else "SEE RESULTS  →",
                            font=("Arial", 11, "bold"), bg="#E8EBF5", fg=NAVY,
                            relief="flat", padx=22, pady=10, state="disabled",
                            command=next_question)
    next_button.pack(side="left", padx=8)

    update_timer()

def update_timer():
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"TIME LEFT: {time_left}s",
                       fg=RED if time_left <= 5 else PURPLE)
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)

def stop_timer():
    global timer_job
    if timer_job is not None:
        try:
            root.after_cancel(timer_job)
        except tk.TclError:
            pass
        timer_job = None

def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")

def submit_answer():
    global score, answered
    if answered:
        return
    choice = selected_answer.get()
    if not choice:
        messagebox.showwarning("Choose an answer", "Please select one answer before submitting.")
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")
    question = quiz_questions[current_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="✓ Correct! Great job.", fg=GREEN)
    else:
        correct = get_choice_text(question, question["answer"])
        wrong_answers.append({"question": question["question"],
                              "your_answer": get_choice_text(question, choice),
                              "correct_answer": correct})
        feedback_label.config(text=f"✕ Not quite. Correct answer: {correct}", fg=RED)
    next_button.config(state="normal")

def time_up():
    global answered
    if answered:
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")
    question = quiz_questions[current_question]
    correct = get_choice_text(question, question["answer"])
    wrong_answers.append({"question": question["question"],
                          "your_answer": "No answer (time is up)",
                          "correct_answer": correct})
    feedback_label.config(text=f"⌛ Time is up! Correct answer: {correct}", fg=RED)
    next_button.config(state="normal")

def next_question():
    global current_question
    if not answered:
        return
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()

def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)
    if percentage >= 90:
        message = "Excellent work! You are an online learning star."
    elif percentage >= 70:
        message = "Great job! You understand the essentials."
    elif percentage >= 50:
        message = "Good effort! Review the topics and keep practicing."
    else:
        message = "Keep learning! A little practice will help you improve."

    card = tk.Frame(main, bg=CARD, padx=28, pady=20,
                    highlightthickness=1, highlightbackground="#E1E5F2")
    card.pack(fill="both", expand=True)
    tk.Label(card, text="QUIZ COMPLETED", font=("Arial", 24, "bold"),
             bg=CARD, fg=NAVY).pack(pady=(2, 4))
    tk.Label(card, text=f"{score} / {total}", font=("Arial", 35, "bold"),
             bg=CARD, fg=BLUE).pack()
    tk.Label(card, text=f"FINAL SCORE: {percentage:.0f}%", font=("Arial", 13, "bold"),
             bg=CARD, fg=PURPLE).pack(pady=4)
    tk.Label(card, text=message, font=("Arial", 11), bg=CARD, fg=MUTED).pack(pady=5)
    high_text = "NEW PERSONAL BEST!" if new_record else f"PERSONAL BEST: {get_high_score()} / 10"
    tk.Label(card, text=high_text, font=("Arial", 11, "bold"),
             bg=CARD, fg=GREEN).pack(pady=(4, 10))

    tk.Label(card, text="ANSWER REVIEW — INCORRECT ANSWERS",
             font=("Arial", 10, "bold"), bg=CARD, fg=NAVY).pack(anchor="w", pady=(5, 5))
    review_frame = tk.Frame(card, bg=CARD)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review = tk.Text(review_frame, height=9, wrap="word", font=("Arial", 10),
                     bg="#F7F8FC", fg=NAVY, yscrollcommand=scrollbar.set,
                     padx=10, pady=8, relief="flat")
    review.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review.yview)
    if not wrong_answers:
        review.insert("end", "Perfect! You answered all 10 questions correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review.insert("end", f"{number}. {item['question']}\n")
            review.insert("end", f"   Your answer: {item['your_answer']}\n")
            review.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")
    review.config(state="disabled")

    buttons = tk.Frame(card, bg=CARD)
    buttons.pack(pady=(12, 0))
    tk.Button(buttons, text="RESTART QUIZ", font=("Arial", 10, "bold"),
              bg=PURPLE, fg="white", relief="flat", padx=20, pady=9,
              command=start_quiz).pack(side="left", padx=8)
    tk.Button(buttons, text="EXIT", font=("Arial", 10, "bold"),
              bg="#E8EBF5", fg=NAVY, relief="flat", padx=20, pady=9,
              command=on_close).pack(side="left", padx=8)

def on_close():
    stop_timer()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()
