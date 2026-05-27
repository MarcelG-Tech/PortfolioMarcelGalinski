# consts.py

# --- Wymiary planszy ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# --- Kolory planszy (HEX) ---
LIGHT_SQUARE = "#DDBB99"  # Jasny brąz/beż
DARK_SQUARE = "#664422"   # Ciemny brąz
HIGHLIGHT_COLOR = "#44FF44"  # Kolor podświetlenia dostępnych ruchów (jasny zielony)
SELECTED_COLOR = "#FFFF00"   # Kolor obramowania wybranego pionka (żółty)

# --- Kolory Pionków ---
WHITE_PIECE = "#FFFFFF"   # Białe
BLACK_PIECE = "#000000"   # Czarne
CROWN_COLOR = "#FFD700"   # Złoty kolor dla damki (oznaczenie tekstowe "K")

# --- Mechanika Gry ---
# Wartości liczbowe reprezentujące stan pola w logice
EMPTY = 0
WHITE = 1
BLACK = -1
WHITE_KING = 2
BLACK_KING = -2

# --- Sztuczna Inteligencja ---
AI_DEPTH = 4  # Głębokość przeszukiwania (4 to złoty środek między szybkością a trudnością)

# Wagi dla funkcji oceny (Heuristic weights)
PIONEK_VAL = 100
DAMKA_VAL = 300
EDGE_BONUS = 10  # Bonus za trzymanie się krawędzi (trudniej zbić)