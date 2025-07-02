import streamlit as st
import random


# --- Game State Initialization ---
if "board" not in st.session_state:
    st.session_state.board = ["-"] * 9
if "currentPlayer" not in st.session_state:
    st.session_state.currentPlayer = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "gameRunning" not in st.session_state:
    st.session_state.gameRunning = True
if "tie" not in st.session_state:
    st.session_state.tie = False

# --- Game Logic ---
def check_winner():
    b = st.session_state.board
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for a, b1, c in lines:
        if b[a] == b[b1] == b[c] != "-":
            st.session_state.winner = b[a]
            st.session_state.gameRunning = False
            return

def check_tie():
    if "-" not in st.session_state.board and st.session_state.winner is None:
        st.session_state.tie = True
        st.session_state.gameRunning = False

def switch_player():
    st.session_state.currentPlayer = "O" if st.session_state.currentPlayer == "X" else "X"

def computer_move():
    if st.session_state.gameRunning and st.session_state.currentPlayer == "O":
        empty = [i for i, val in enumerate(st.session_state.board) if val == "-"]
        if empty:
            pos = random.choice(empty)
            st.session_state.board[pos] = "O"
            check_winner()
            check_tie()
            if st.session_state.gameRunning:
                switch_player()

def player_move(i):
    if st.session_state.board[i] == "-" and st.session_state.gameRunning and st.session_state.currentPlayer == "X":
        st.session_state.board[i] = "X"
        check_winner()
        check_tie()
        if st.session_state.gameRunning:
            switch_player()
            computer_move()

def reset_game():
    st.session_state.board = ["-"] * 9
    st.session_state.currentPlayer = "X"
    st.session_state.winner = None
    st.session_state.gameRunning = True
    st.session_state.tie = False

# --- Page Setup ---
st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# --- Custom CSS for Background and Result Banner ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #dbeafe, #f0f9ff);
        font-family: 'Segoe UI', sans-serif;
        position: relative;
    }
    .title {
        text-align: center;
        font-size: 36px;
        color: #0f172a;
    }
    .overlay {
        position: fixed;
        top: 45%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 30px 60px;
        font-size: 32px;
        font-weight: bold;
        border-radius: 10px;
        z-index: 9999;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 class='title'>🎮 Tic Tac Toe - Player vs Computer</h1>", unsafe_allow_html=True)

# --- Rules ---
with st.expander("📘 Rules of the Game"):
    st.markdown("""
    - The game is played on a 3×3 grid.
    - You are **X** and the computer is **O**.
    - Take turns placing marks in empty squares.
    - First to get 3 in a row wins.
    - If all 9 are filled and no winner, it's a tie.
    """)

# --- 3x3 Grid Board ---
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        cell = st.session_state.board[i]
        with cols[col]:
            if cell == "-":
                if st.button(" ", key=i, help=f"Click to place at {i+1}", use_container_width=True):
                    player_move(i)
                    st.rerun()
            else:
                st.markdown(
                    f"<div style='text-align: center; font-size: 36px; font-weight: bold; color:#1e293b'>{cell}</div>",
                    unsafe_allow_html=True
                )

# --- Overlay Result Banner (Win or Tie) ---
if st.session_state.winner:
    st.markdown(f"<div class='overlay'>🏆 Winner: {st.session_state.winner}!</div>", unsafe_allow_html=True)
elif st.session_state.tie:
    st.markdown("<div class='overlay'>🤝 It's a tie!</div>", unsafe_allow_html=True)

# --- Restart Button ---
st.markdown("###")
st.button("🔁 Restart Game", on_click=reset_game)
