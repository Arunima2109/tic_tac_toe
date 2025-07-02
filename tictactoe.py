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

# --- Game Logic ---
def check_winner():
    b = st.session_state.board
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for a, b1, c in lines:
        if b[a] == b[b1] == b[c] != "-":
            st.session_state.winner = b[a]
            st.session_state.gameRunning = False
            return

def check_tie():
    if "-" not in st.session_state.board and st.session_state.winner is None:
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

# --- Page Setup ---
st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# --- Custom Background ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #dbeafe, #f0f9ff);
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 36px;
        margin-top: -30px;
        margin-bottom: 10px;
        color: #0f172a;
    }
    .status {
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 class='title'>🎮 Tic Tac Toe - Player vs Computer</h1>", unsafe_allow_html=True)

# --- Rules Button ---
with st.expander("📘 Rules of the Game", expanded=False):
    st.markdown("""
    - The game is played on a 3×3 grid.
    - You are **X** and the computer is **O**.
    - Players take turns placing their marks in empty squares.
    - The first player to get 3 of their marks in a row (vertically, horizontally, or diagonally) wins!
    - If all 9 squares are filled and no player has 3 in a row, the game is a tie.
    """)

# --- Game Status ---
if st.session_state.winner:
    status_msg = f"🏆 Winner: {st.session_state.winner}"
elif not st.session_state.gameRunning:
    status_msg = "🤝 It's a tie!"
else:
    status_msg = f"🎯 Turn: {st.session_state.currentPlayer}"

st.button(f"🧭 Status: {status_msg}", disabled=True)

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

# --- Restart Button ---
st.button("🔁 Restart Game", on_click=reset_game)
