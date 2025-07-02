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
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    for a, b1, c in lines:
        if st.session_state.board[a] == st.session_state.board[b1] == st.session_state.board[c] != "-":
            st.session_state.winner = st.session_state.board[a]
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

# --- UI Layout ---
st.set_page_config(page_title="Tic Tac Toe", layout="centered")
st.title("🎮 Tic Tac Toe - Player vs Computer")
st.markdown("#### Click a square to place your ❌")

# Create 3x3 grid using rows
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
                    f"<div style='text-align: center; font-size: 36px; font-weight: bold;'>{cell}</div>",
                    unsafe_allow_html=True
                )

# Show result
if st.session_state.winner:
    st.success(f"🎉 Winner: {st.session_state.winner}!")
elif not st.session_state.gameRunning:
    st.info("It's a tie!")

# Restart Button
st.button("🔁 Restart Game", on_click=reset_game)
