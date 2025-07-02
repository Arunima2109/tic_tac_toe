import streamlit as st
import random

# Initialize game state
if "board" not in st.session_state:
    st.session_state.board = ["-"] * 9
if "currentPlayer" not in st.session_state:
    st.session_state.currentPlayer = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "gameRunning" not in st.session_state:
    st.session_state.gameRunning = True

# Game logic functions
def check_winner():
    b = st.session_state.board
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for line in lines:
        a, b1, c = line
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
        empty_positions = [i for i, val in enumerate(st.session_state.board) if val == "-"]
        if empty_positions:
            pos = random.choice(empty_positions)
            st.session_state.board[pos] = "O"
            check_winner()
            check_tie()
            if st.session_state.gameRunning:
                switch_player()

def player_move(index):
    if st.session_state.gameRunning and st.session_state.board[index] == "-" and st.session_state.currentPlayer == "X":
        st.session_state.board[index] = "X"
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

# Title
st.title("🎮 Tic Tac Toe - Player vs Computer")

# Board layout
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        # Display either "X", "O", or show a button
        cell = st.session_state.board[i]
        if cell == "-":
            if st.button(" ", key=i):
                player_move(i)
                st.rerun()  # 🔁 Ensures UI updates instantly after move
        else:
            st.markdown(f"<h2 style='text-align: center'>{cell}</h2>", unsafe_allow_html=True)

# Game status
if st.session_state.winner:
    st.success(f"🎉 The winner is {st.session_state.winner}!")
elif not st.session_state.gameRunning:
    st.info("It's a tie!")

# Reset button
st.button("🔁 Restart Game", on_click=reset_game)
