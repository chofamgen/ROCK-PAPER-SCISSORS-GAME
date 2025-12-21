import streamlit as st
import time


# --- 1. THE SHARED DICTIONARY ( The "Database" ) ---
# We use this function to create a dictionary that lives on the server.
# @st.cache_resource means "Run this once and share it with everyone."
@st.cache_resource
def get_database():
    return {}  # It starts empty!


# Get the shared dictionary
games = get_database()

st.title("Rock Paper Scissors: Online 🌎")

# --- 2. LOGIN SYSTEM (Who are you?) ---
# Simple text box to ask for a room name
room = st.text_input("Type a Room Name (e.g. 'room1'):")

if not room:
    st.stop()  # Stop here if they haven't typed anything

# Check if the room exists in our dictionary. If not, create it.
if room not in games:
    games[room] = {
        "player1_move": None,
        "player2_move": None,
        "count": 0,  # How many people are in the room?
    }

# --- 3. PLAYER ASSIGNMENT (Are you P1 or P2?) ---
# We use 'session_state' to remember who YOU are in your browser.
if "my_role" not in st.session_state:
    current_count = games[room]["count"]

    if current_count == 0:
        st.session_state.my_role = "Player 1"
        games[room]["count"] = 1
    elif current_count == 1:
        st.session_state.my_role = "Player 2"
        games[room]["count"] = 2
    else:
        st.error("Room is full!")
        st.stop()

my_role = st.session_state.my_role
st.write(f"You are: **{my_role}** in room **{room}**")

# --- 4. WAITING ROOM ---
# If you are Player 1, wait for Player 2 to enter
if games[room]["count"] < 2:
    st.warning("Waiting for Player 2 to join...")
    time.sleep(2)  # Wait 2 seconds
    st.rerun()  # Refresh the page to check again

# --- 5. THE GAME BUTTONS ---
# Determine whose move variable belongs to me
if my_role == "Player 1":
    my_move = games[room]["player1_move"]
    opp_move = games[room]["player2_move"]
else:
    my_move = games[room]["player2_move"]
    opp_move = games[room]["player1_move"]

# If I haven't moved yet, show buttons
if my_move is None:
    st.write("### Make your move:")
    c1, c2, c3 = st.columns(3)

    if c1.button("Rock"):
        if my_role == "Player 1":
            games[room]["player1_move"] = "Rock"
        else:
            games[room]["player2_move"] = "Rock"
        st.rerun()

    if c2.button("Paper"):
        if my_role == "Player 1":
            games[room]["player1_move"] = "Paper"
        else:
            games[room]["player2_move"] = "Paper"
        st.rerun()

    if c3.button("Scissors"):
        if my_role == "Player 1":
            games[room]["player1_move"] = "Scissors"
        else:
            games[room]["player2_move"] = "Scissors"
        st.rerun()

# --- 6. THE RESULTS ---
else:
    st.info("You moved! Waiting for opponent...")

    # If opponent hasn't moved, refresh every second
    if opp_move is None:
        time.sleep(1)
        st.rerun()
    else:
        # BOTH have moved. Time to check winner.
        st.success(f"You chose {my_move}. Opponent chose {opp_move}.")

        # Simple Winner Logic
        if my_move == opp_move:
            st.warning("It's a Tie!")
        elif (
            (my_move == "Rock" and opp_move == "Scissors")
            or (my_move == "Paper" and opp_move == "Rock")
            or (my_move == "Scissors" and opp_move == "Paper")
        ):
            st.balloons()
            st.success("You WIN! 🎉")
        else:
            st.error("You LOSE! 💀")

        # Reset Button
        if st.button("Play Again"):
            games[room]["player1_move"] = None
            games[room]["player2_move"] = None
            st.rerun()
