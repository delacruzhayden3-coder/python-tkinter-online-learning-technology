# Online Learning Technology Quiz

**Name:** Miel Hayden D. Gabad
**Section:** BSINFOTECH SE 3-A 
**Topic:** Online Learning Technology

## Project Overview
This is a desktop multiple-choice quiz application made with Python and Tkinter. It helps learners review online learning platforms, virtual classes, digital citizenship, internet safety, and effective online study practices.

## Features
- Exactly 10 original multiple-choice questions
- Four answer choices (A–D) and one correct answer per question
- Random question order on every new game
- 15-second countdown for every question
- Automatic time-out handling
- Answer submission lock to prevent double submission
- Score and percentage calculation
- Results message based on performance
- Review of incorrect answers and correct answers
- High score saved in `high_score.txt`
- Restart and exit buttons
- Custom blue-and-purple educational interface

## How to Run
1. Install Python 3.
2. Make sure Tkinter is included with your Python installation.
3. Save `quiz.py` in a project folder.
4. Open a terminal or command prompt in that folder.
5. Run:

   ```bash
   python quiz.py
   ```

6. Click **Start Quiz**, choose one answer per question, and submit it before the 15-second timer ends.

The program creates `high_score.txt` beside `quiz.py` after a new high score is achieved.

## How Questions Are Stored and Shuffled
The 10 questions are stored in a Python list. Each question is a dictionary containing the question text, a list of four choices, and the letter of the correct answer. `random.sample(QUESTIONS, len(QUESTIONS))` creates a shuffled copy each time a quiz starts, leaving the original question list unchanged.

## How the Timer Works
Each question begins with 15 seconds. Tkinter's `root.after(1000, update_timer)` schedules the countdown function to run again after one second. When the player submits an answer, `stop_timer()` cancels the scheduled callback. If the timer reaches zero, `time_up()` records the question as incorrect and reveals the correct answer. The program does not use `time.sleep()`, so the window remains responsive.

## How the Program Identifies the Correct Answer
Every question dictionary stores the correct answer as a letter from A to D. The selected radio-button value is compared with `question["answer"]`. If the letters match, one point is added. Otherwise, the question, selected answer, and correct answer are saved for the answer review.

## How Score and High Score Work
A correct answer earns one point. The percentage is calculated using `(score / total) * 100`. The `get_high_score()` function reads the saved number from `high_score.txt`. The `save_high_score()` function writes the new score only when it is higher than the previous record. This allows the high score to remain available after the application is closed and reopened.

## Function Explanations

| Function | Purpose | Called when |
|---|---|---|
| `show_start_screen()` | Displays the title, instructions, and saved high score | Application opens |
| `start_quiz()` | Resets quiz data and randomizes the questions | Start or Restart is clicked |
| `show_question()` | Displays the current question, choices, progress, and timer | A new question begins |
| `update_timer()` | Updates the visible countdown every second | A question is displayed |
| `stop_timer()` | Cancels the scheduled countdown | An answer is submitted or the app closes |
| `submit_answer()` | Checks the selected answer and updates the score or review | Submit is clicked |
| `time_up()` | Marks the question wrong when time reaches zero | Countdown expires |
| `show_results()` | Displays the final score, percentage, message, and answer review | After question 10 |
| `get_high_score()` | Reads the saved high score from the text file | Start screen/results are shown |
| `save_high_score()` | Saves a new record if the score is higher | Results screen is shown |

## Screenshots
After running the application, capture and add these screenshots to the `screenshots` folder:

- `start.png` — start screen
- `question.png` — question screen showing the timer
- `feedback.png` — correct or incorrect answer feedback
- `results.png` — results screen and answer review
- `high_score.png` — saved high score visible after closing and reopening the application

## Challenges I Faced
Example to personalize after testing: One challenge was making the countdown stop after an answer was submitted. I solved this by storing the callback identifier returned by `root.after()` and cancelling it with `root.after_cancel()`.

## Submission Checklist
- [ ] Test all 10 questions and all four choices.
- [ ] Confirm that question order changes after restarting.
- [ ] Confirm that time-out marks a question wrong.
- [ ] Confirm that submitting twice does not increase the score twice.
- [ ] Close and reopen the app to confirm that the high score remains.
- [ ] Add the five required screenshots.
- [ ] Push the project to GitHub and submit the repository link in the LMS textbox.
