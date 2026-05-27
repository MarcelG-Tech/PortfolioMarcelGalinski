import tkinter as tk
from consts import *
from checkers_logic import Board

class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Warcaby - Projekt Studencki")
        
        # Inicjalizacja logiki gry
        self.game_logic = Board()
        
        # Konfiguracja GUI
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        self.selected_pos = None  # Pozycja wybranego pionka (row, col)
        self.valid_moves = []     # Lista dostępnych ruchów dla wybranego pionka
        self.turn = WHITE         # Zaczynają białe (1)
        
        self.draw_everything()
        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        """Obsługa kliknięcia myszką."""
        col, row = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
        
        # 1. Sprawdź, czy gracz kliknął w zieloną kropkę (dostępny ruch)
        for move in self.valid_moves:
            if move['dest'] == (row, col):
                self.execute_move(move)
                return

        # 2. Wybieranie/zmiana wybranego pionka
        piece = self.game_logic.get_piece(row, col)
        # Sprawdzamy, czy kliknięto pionek aktualnego gracza
        if (self.turn == WHITE and piece > 0) or (self.turn == BLACK and piece < 0):
            self.selected_pos = (row, col)
            all_possible = self.game_logic.get_valid_moves(self.turn)
            # Filtrujemy ruchy tylko dla tego klikniętego pionka
            self.valid_moves = [m for m in all_possible if m['origin'] == (row, col)]
        else:
            # Kliknięcie w puste pole lub pionek przeciwnika usuwa zaznaczenie
            self.selected_pos = None
            self.valid_moves = []
            
        self.draw_everything()

    def execute_move(self, move):
        # 1. Fizyczne wykonanie ruchu w logice
        self.game_logic.move(move['origin'], move['dest'])
        for r, c in move['captured']:
            self.game_logic.board[r][c] = EMPTY
            
        # 2. KLUCZOWE: Czyścimy listę ruchów i zaznaczenie ZANIM odświeżymy ekran
        self.valid_moves = []
        self.selected_pos = None
        
        # 3. Odświeżamy widok (draw_everything wyczyści stare kropki dzięki canvas.delete("all"))
        self.draw_everything()
        self.root.update() # Wymuszamy natychmiastowe przerysowanie okna

        # 4. Sprawdzenie zwycięstwa
        if self.check_game_over():
            return # Jeśli ktoś wygrał, przerywamy, nie robimy ruchu AI

        # 5. Kolej na AI (Czarne)
        if self.turn == WHITE:
            self.turn = BLACK
            self.root.after(500, self.ai_turn)

    def ai_turn(self):
        from ai import minimax
        # Wywołanie AI - przekazujemy głęboką kopię, żeby AI nie "brudziło" w oryginale
        value, new_board = minimax(self.game_logic, AI_DEPTH, -float('inf'), float('inf'), False)
        
        if new_board:
            # Podmieniamy cały obiekt logiki na ten wyliczony przez AI
            self.game_logic = new_board
            self.selected_pos = None
            self.valid_moves = []
            self.draw_everything()
            self.check_game_over()
            
        self.turn = WHITE # Oddajemy turę graczowi

    def check_game_over(self):
        winner = self.game_logic.check_winner()
        if winner is not None:
            winner_text = "Białe wygrywają!" if winner == WHITE else "Czarne wygrywają!"
            # Wyświetlamy napis na środku planszy
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text=winner_text, 
                                   fill="red", font=("Arial", 40, "bold"), tags="msg")
            # Blokujemy dalszą grę
            self.canvas.unbind("<Button-1>")

    def draw_piece(self, row, col, piece_type):
        """Rysuje pionek lub damkę."""
        padding = 10
        x1 = col * SQUARE_SIZE + padding
        y1 = row * SQUARE_SIZE + padding
        x2 = (col + 1) * SQUARE_SIZE - padding
        y2 = (row + 1) * SQUARE_SIZE - padding
        
        color = WHITE_PIECE if piece_type > 0 else BLACK_PIECE
        outline = "grey" if piece_type > 0 else "white"
        
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, width=2)
        
        # Oznaczenie damki (KING)
        if abs(piece_type) == 2:
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            self.canvas.create_text(mid_x, mid_y, text="K", fill=CROWN_COLOR, font=("Arial", 20, "bold"))

    def draw_everything(self):
        """Odświeża cały widok."""
        self.canvas.delete("all")
        
        # Rysowanie pól planszy
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * SQUARE_SIZE, r * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                
                # Kolor bazowy
                color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
                
                # Podświetlenie jeśli pionek jest wybrany
                if self.selected_pos == (r, c):
                    color = SELECTED_COLOR
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Rysowanie kropek podpowiedzi (możliwe ruchy)
        for move in self.valid_moves:
            r, c = move['dest']
            cx, cy = c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2
            self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill=HIGHLIGHT_COLOR)

        # Rysowanie pionków
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.game_logic.get_piece(r, c)
                if piece != EMPTY:
                    self.draw_piece(r, c, piece)

if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()