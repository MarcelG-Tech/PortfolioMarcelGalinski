from consts import *

class Board:
    def __init__(self):
        # Tworzymy macierz 8x8 wypełnioną zerami
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.create_board()
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0

    def create_board(self):
        """Rozstawia pionki na polach startowych."""
        for r in range(ROWS):
            for c in range(COLS):
                if (r + c) % 2 != 0: # Pionki stawiamy tylko na ciemnych polach
                    if r < 3:
                        self.board[r][c] = BLACK
                    elif r > 4:
                        self.board[r][c] = WHITE

    def move(self, piece_pos, target_pos):
        r1, c1 = piece_pos
        r2, c2 = target_pos
        
        piece = self.board[r1][c1]
        self.board[r2][c2] = piece
        self.board[r1][c1] = EMPTY  # <--- To jest kluczowe! 

        # Logika damki
        if piece == WHITE and r2 == 0:
            self.board[r2][c2] = WHITE_KING
        if piece == BLACK and r2 == ROWS - 1:
            self.board[r2][c2] = BLACK_KING

    def get_piece(self, row, col):
        return self.board[row][col]

    def is_on_board(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLS

    def evaluate(self):
        """Funkcja oceny stanu planszy dla AI."""
        # Podstawowa ocena: suma wartości pionków i damek
        score = 0
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece == WHITE: score += PIONEK_VAL
                elif piece == WHITE_KING: score += DAMKA_VAL
                elif piece == BLACK: score -= PIONEK_VAL
                elif piece == BLACK_KING: score -= DAMKA_VAL
        return score
    
    def get_valid_moves(self, player):
        all_captures = []
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                # Sprawdzamy tylko pionki gracza (np. 1 lub 2 dla białych)
                if (player == WHITE and piece > 0) or (player == BLACK and piece < 0):
                    moves = self.get_piece_captures(r, c, [])
                    if moves:
                        all_captures.extend(moves)
        
        # JEŚLI SĄ BICIA - zwracamy tylko najdłuższe 
        if all_captures:
            max_len = max(len(m['captured']) for m in all_captures)
            return [m for m in all_captures if len(m['captured']) == max_len]
        
        # JEŚLI NIE MA BIĆ - szukamy zwykłych ruchów
        simple_moves = []
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if (player == WHITE and piece > 0) or (player == BLACK and piece < 0):
                    simple_moves.extend(self.get_piece_simple_moves(r, c))
        return simple_moves

    def get_piece_captures(self, r, c, captured_already, start_pos=None):
        if start_pos is None:
            start_pos = (r, c)
            
        moves = []
        piece = self.board[r][c]
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        
        found_further_capture = False
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            mid_r, mid_c = r + dr//2, c + dc//2
            
            if self.is_on_board(nr, nc):
                mid_piece = self.board[mid_r][mid_c]
                # Czy można przeskoczyć?
                if mid_piece != EMPTY and (mid_piece * piece < 0) and self.board[nr][nc] == EMPTY:
                    if (mid_r, mid_c) not in captured_already:
                        found_further_capture = True
                        new_captured = captured_already + [(mid_r, mid_c)]
                        
                        # Symulacja bicia (przesunięcie pionka)
                        temp_piece = self.board[r][c]
                        self.board[r][c] = EMPTY
                        self.board[nr][nc] = temp_piece
                        
                        # Szukamy dalej z nowej pozycji
                        further = self.get_piece_captures(nr, nc, new_captured, start_pos)
                        moves.extend(further)
                        
                        # Cofnięcie symulacji (Backtracking)
                        self.board[r][c] = temp_piece
                        self.board[nr][nc] = EMPTY
                        
        if not found_further_capture and len(captured_already) > 0:
            # Jeśli nie ma dalszych bić, zapisujemy tę ścieżkę jako gotowy ruch
            return [{'origin': start_pos, 'dest': (r, c), 'captured': captured_already}]
            
        return moves
    
    def get_piece_simple_moves(self, r, c):
        """Zwraca zwykłe ruchy o 1 pole."""
        moves = []
        piece = self.board[r][c]
        # Białe idą w górę (-1), czarne w dół (+1). Damki w obie.
        dirs = []
        if piece == WHITE: dirs = [(-1, -1), (-1, 1)]
        elif piece == BLACK: dirs = [(1, -1), (1, 1)]
        elif abs(piece) == 2: dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self.is_on_board(nr, nc) and self.board[nr][nc] == EMPTY:
                moves.append({'dest': (nr, nc), 'captured': [], 'origin': (r, c)})
        return moves
    def check_winner(self):
        """Zwraca WHITE, BLACK lub None jeśli gra trwa."""
        # Brak pionków
        white_pieces = any((1 in row or 2 in row) for row in self.board)
        black_pieces = any((-1 in row or -2 in row) for row in self.board)
        
        if not white_pieces: return BLACK
        if not black_pieces: return WHITE
        
        # Brak możliwości ruchu (blokada)
        if not self.get_valid_moves(WHITE): return BLACK
        if not self.get_valid_moves(BLACK): return WHITE
        
        return None
