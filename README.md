# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  It is a number-guessing game built with Streamlit. The player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), guesses the secret number, and gets optional "Go HIGHER / Go LOWER" hints until they win or run out of attempts.

- [x] **Detail which bugs you found.**
  1. **New Game didn't fully reset.** Clicking "New Game" only reset `attempts` and the secret — `score`, `status`, and `history` carried over from the previous game.

  2. **Secret out of range on difficulty change.** Switching to Easy (1–20) kept a secret from the old range (e.g. 28), because the secret was only generated on first load and on New Game, never when difficulty changed.

  3. **Lying hints.** On even attempts the code did `secret = str(secret)`, so `check_guess` compared an int guess to a string secret lexicographically (`"6" > "20"`) and returned the wrong HIGHER/LOWER hint.

  4. **Attempts counter lagged by one.** "Attempts left" was rendered at the top of the script, before the submit handler incremented the counter, so it always showed the state before the current guess.

- [x] **Explain what fixes you applied.**
  1. New Game now also resets `score`, `status`, and `history`, and generates the secret with `random.randint(low, high)`.

  2. Added a block that stores the active difficulty in session state and regenerates the secret + resets the round whenever the difficulty changes, keeping the secret in range.

  3. Removed the `str(secret)` conversion so the integer secret is always passed to `check_guess`, making the comparison numeric.
  
  4. Moved "Attempts left" into an `st.empty()` placeholder that is filled *after* the submit handler runs, and initialized `attempts` to `0` for consistency with the resets.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Pick a difficulty in the sidebar (Easy, Normal, or Hard). The range and attempt limit update, and a fresh secret is generated within that range.
2. Enter a guess and click "Submit Guess". The game tells you "Go HIGHER!" or "Go LOWER!" if you use the hint. On every attempt, "Attempts left" decreases by exactly one each guess.
3. Winning shows a balloon animation, the secret, and your final score.
4. Click "New Game" to start over: score, status, history, attempts, and the secret are all reset cleanly.
5. Optional: Open "Developer Debug Info" at any time to verify the game is tracking correctly.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

collected 5 items

tests/test_game_logic.py .....                                           [100%]

============================== 5 passed in 0.02s ===============================

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
