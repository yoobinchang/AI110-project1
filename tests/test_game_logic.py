from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Regression test for the int/string secret bug ---------------------------
# The app used to convert the secret to a string on even attempts:
#     secret = str(st.session_state.secret)
# That made check_guess(6, "20") compare values lexicographically:
# "6" > "20" (because '6' > '2'), so it wrongly returned "Too High" and
# told the player to go LOWER when the secret (20) was actually HIGHER.
# This is the exact sequence the user hit: guess 6 against secret 20.
def test_below_secret_returns_too_low_with_int_secret():
    outcome, _ = check_guess(6, 20)
    assert outcome == "Too Low"


def test_string_secret_would_have_given_wrong_answer():
    # Documents *why* the secret must stay an int: with a string secret the
    # lexicographic comparison misfires, so 6 is reported as "Too High".
    # If this ever returns "Too Low", the fragile fallback changed and the
    # int-only contract is what protects us.
    outcome, _ = check_guess(6, "20")
    assert outcome == "Too High"
