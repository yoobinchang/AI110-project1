# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game fell apart as soon as I played. The "Attempts left" count was already off before I had guessed anything, and the hints pointed me the wrong way.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1) the allowed attempt and attempt left was different. 
    - it already assumed that I took one guess.
  2) the secret key did not match to the range when difficulty is changed
    - when I changed to easy level (range 1-20), secret key was still 28
  3) the hints were backwards

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| clicked "new game" | resets history | previous history remains |
| clicked "new game" | resets score | previous score remains |
| submit guess | adds to history | it does not go to history sometimes when I continuously guess <- possibly a glitch
| guess of 60 | hint : too high | hint : too low | 


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Cluade Code agent on this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
When the hints were backwards, the AI traced it to a line that did `secret = str(secret)` on even attempts, which made `check_guess` compare an int guess to a string secret lexicographically. It removed the conversion so the integer secret is always passed. I verified this by replaying my exact sequence (guess 6 against secret 20) and seeing it now say "Go HIGHER!" correctly.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
After I asked it to fix the "New Game" reset, the AI also switched the secret to `random.randint(low, high)`, which made it look like the difficulty/range bug was handled too. However, that change only ran on the New Game button, so simply switching difficulty still left an out-of-range secret. When I ran the game, the Debug panel still showed 28 after I changed to Easy (1–20). Only after I pointed it out did the AI add a feature to regenerate the secret on a difficulty change.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
For each bug I re-ran the exact scenario that triggered it instead of trusting that the code on sight. For the backwards hints I replayed guess 6 against secret 20. For the range bug, I switched difficulty and watched the secret in the Debug panel. Lastly, for the attempts lag, I counted that "Attempts left" dropped by exactly one per guess.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran using pytest after adding a regression test for the hint bug. It showed 5 passed, but more importantly the first run revealed that the 3 original tests were failing for a reason unrelated to the fix: they compared `check_guess(...)` to a bare string when the function actually returns a `(outcome, message)` tuple. That taught me to read a function's real return type before run on it.

- Did AI help you design or understand any tests? How?
Yes. I asked the AI to write a pytest case that specifically targeted the bugs I fixed, and it produced the tests using my real failing values that I gave example of when fixing the bug. It also explained that the existing tests were a test bug (tuple vs string), not a code bug, so the right fix was to unpack the tuple rather than fix the code.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every time you interact with a Streamlit app, such as clicking a button or typing in a box, Streamlit re-runs whole script from top to bottom like reloading the page. Because of that, any normal variable resets on every interaction. Session state is the one place values survive between reruns, so anything you want to remember (the secret, score, attempts, history) has to live there.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? This could be a testing habit, a prompting strategy, or a way you used Git.
Reporting bugs to the AI one at a time with the exact input and the expected vs. actual behavior. That made the AI's diagnoses more precise and gave me a concrete thing. I want to keep writing a small reproduction case as little bug test before asking for a fix.

- What is one thing you would do differently next time you work with AI on a coding task?
I'd ask the AI to explain why a change is needed before accepting it every time. I did this once (I rejected a placeholder edit until it justified the rerun ordering), and that one explanation taught me more than several silent edits did.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI generated code can look polished and still be wrong. The original app even claimed it was "production-ready." I now treat AI output as a confident draft to verify by reproducing the actual behavior and running tests, not as something to trust on sight.
