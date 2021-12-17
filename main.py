from typing import List
from random import randint
from pygame import draw
import pygame
from time import sleep

# Inlcusiones para resolver por el algoritmo de graham
from graham_algorithm import *

# tamaño de pantalla: 1024 x 768
"""
    Paleta de colores:
    #43bec6: Puntos Jugador y lineas
    #c66b43: Puntos graham
    #bc0101: Temporizador
"""

def generate_points(x1: int, x2: int, y1: int, y2 :int):
    points = []
    for _ in range(30):
        x = randint(x1, x2) # Coordenadas en X
        y = randint(y1, y2) # Coordenadas en Y
        points.append(Point((x, y)))

    return points

# Dibuja el tablero especificado por "board"
def draw_board(
        surface: pygame.surface.Surface,
        bg_color: pygame.Color,
        board_points: List[Point],
        char_lines: List[Point],
        opt: str = '',
        board: str = '',
        color_sol: str = '#c92828'
    ):
    if board == 'player':
        surface.fill(bg_color, (12, 49, 490, 657))
        draw_points_on_board(surface, board_points, '#437cc6')
        if opt == 'player solve':
            draw_line_player(surface, char_lines, '#fcba03')
        elif opt == 'graham solve':
            char_lines.append(char_lines[0])
            draw_line_player(surface, char_lines, color_sol)
            char_lines.pop()

    if board == 'graham':
        surface.fill(bg_color, (512, 49, 500, 657))
        draw_points_on_board(surface, board_points, '#c66b43')
        if opt == 'steps':
            draw_graham_steps(surface, char_lines)
        elif opt == 'solve':
            draw_graham_solve(surface, char_lines)



# Dibuja los pasos de la solución de graham
def draw_graham_steps(surface: pygame.Surface, graham_steps: List[Point]):
    if len(graham_steps) < 1:
        return
    for idx, point in enumerate(graham_steps[0]):
        if idx+1 >= len(graham_steps[0]):
            return
        draw.line(surface, '#fcba03', (point.X, point.Y), (graham_steps[0][idx+1].X, graham_steps[0][idx+1].Y), 4)

# Dibuja la solución de graham
def draw_graham_solve(surface: pygame.Surface, graham_solve: List[Point]):
    for idx, point in enumerate(graham_solve):
        if idx+1 >= len(graham_solve):
            draw.line(surface, '#fcba03', (graham_solve[-1].X, graham_solve[-1].Y),
                (graham_solve[0].X, graham_solve[0].Y), 4)
            return
        draw.line(surface, '#fcba03', (point.X, point.Y), (graham_solve[idx+1].X, graham_solve[idx+1].Y), 4)

# Revisa si el mouse está sobre un punto en el tablero del jugador
def point_colition(point_a: Point, point_b: Point, radius: int = 1):
    sqx = (point_a.X - point_b.X) ** 2
    sqy = (point_a.Y - point_b.Y) ** 2

    return (sqx + sqy) ** 0.5 < radius

# Dibuja los puntos
def draw_points_on_board(surface: pygame.Surface, points: List[Point], color: pygame.Color):
    for point in points:
        draw.circle(surface, color, (point.X, point.Y), 4)

# Dibuja las lineas que ha dibujado el jugador
def draw_line_player(surface: pygame.Surface, points: List[Point], color_line: pygame.Color):
    for idx, point in enumerate(points):
        if idx + 1 >= len(points):
            return
        draw.line(surface, color_line, (point.X, point.Y), (points[idx+1].X, points[idx+1].Y), 4)

def check_player_solve(player_drawn_lines: List[Point], player_solve: List[Point]):
    player_solve.append(player_solve[0])
    if player_drawn_lines == []:
        player_solve.pop()
        return False
    if (len(player_solve)-1)*2 != len(player_drawn_lines):
        player_solve.pop()
        return False
    for point in player_drawn_lines:
        if point not in player_solve:
            player_solve.pop()
            return False

    player_solve.pop()
    return True

def update_timer(surface: pygame.Surface, timer: int, color: pygame.Color):
    surface.fill(color, (456, 710, 100, 58))
    text = str(int(timer))
    font = pygame.font.SysFont('Consolas', 30)
    text = font.render(text, True, '#0878c9')
    text_rect = text.get_rect(center = (1014//2, 730))
    surface.blit(text, text_rect)

def game_over(surface: pygame.Surface, color: pygame.Color,  opt: bool = False):
    surface.fill(color)
    if opt:
        text = 'Ganaste :O'
    else:
        text = 'Perdiste :('
    font = pygame.font.SysFont('Consolas', 30)
    text = font.render(text, True, '#0878c9')
    text_rect = text.get_rect(center = (1024//2, 384))
    surface.blit(text, text_rect)

def main():
    player_board = generate_points(30, 476, 67, 687)
    graham_board = generate_points(536, 993, 67, 687)
    player_solve, _, _ = graham_scan(player_board)
    graham_solve, graham_steps, timer = graham_scan(graham_board) # Obtiene la envolente convexa por el algoritmo "graham scan"

    window = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Graham\'s Game')
    bg_black = pygame.Color('#000000')
    next_step, t = pygame.USEREVENT+1, 450

    pygame.time.set_timer(next_step, t)
    
    font = pygame.font.Font(None, 40)
    player_text = font.render('Player', True, '#43bec6')
    graham_text = font.render('Graham', True, '#43bec6')
    window.blit(player_text, (207, 10))
    window.blit(graham_text, (715, 10))

    draw.lines(window, '#43c68e', True, [(10, 47), (1013, 47), (1013, 707), (10, 707)], 3)
    draw.line(window, '#43c68e', (506, 47), (506, 707), 10)

    drawn_lines = []
    startpoint = Point((0, 0))
    endpoint = Point((0, 0))
    is_clicked = False
    run = True
    draw_board(window, bg_black, player_board, _, '', 'player')
    draw_board(window, bg_black, graham_board, _, '', 'graham')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Obtiene el estado del botón izquierdo del mouse
            button_left = pygame.mouse.get_pressed()[0]
            # Si el botón izquierdo del mouse está siendo presionado
            if button_left:
                # Obtiene la posición actual del mouse
                current_pos = pygame.mouse.get_pos()
                # Si la posición actual del mouse es diferente del punto
                # inicial y el mouse no estaba siendo presionado
                if current_pos != startpoint and not is_clicked:
                    # Itera los puntos dentro del tablero del jugador
                    for point in player_board:
                        # Revisa si hay alguna colisión entre el cursor del mouse y el punto "point"
                        if point_colition(Point(current_pos), point, 6):
                            # Establece el nuevo punto inicial
                            startpoint = point
                            is_clicked = True

                # Si "startpoint" no es el punto por defecto "(0, 0)"
                if startpoint != Point((0, 0)):
                    # Itera los puntos dentro del tablero del jugador
                    for point in player_board:
                        # Revisa si hay alguna colisión entre el cursor del mouse y el punto "point"
                        if point_colition(Point(current_pos), point, 6) and point != startpoint:
                            endpoint = point
                            drawn_lines.append(startpoint)
                            drawn_lines.append(point)

                            draw_board(window, bg_black, player_board, drawn_lines, 'player solve', 'player')
                            pygame.draw.line(window, '#fcba03', (startpoint.X, startpoint.Y), (endpoint.X, endpoint.Y), 3)
                            startpoint = endpoint
                        else:
                            draw_board(window, bg_black, player_board, drawn_lines, 'player solve', 'player')
                            pygame.draw.line(window, '#fcba03', (startpoint.X, startpoint.Y), current_pos, 3)
            else:
                if startpoint != Point((0, 0)):
                    draw_board(window, bg_black, player_board, drawn_lines, 'player solve', 'player')
                startpoint = Point((0, 0))
                is_clicked = False

            if event.type == next_step:
                timer -= (t/450)
                if len(graham_steps) > 0:
                    draw_board(window, bg_black, graham_board, graham_steps, 'steps', 'graham')
                    graham_steps.pop(0)
                else:
                    draw_board(window, bg_black, graham_board, graham_solve, 'solve', 'graham')

            if timer <= 0:
                update_timer(window, 0, bg_black)
                if check_player_solve(drawn_lines, player_solve):
                    if timer <= -10:
                        game_over(window, bg_black, True)
                    else:
                        draw_board(window, bg_black, player_board, player_solve, 'graham solve', 'player', '#0878c9')
                else:
                    if timer <= -10:
                        game_over(window, bg_black)
                    else:
                        draw_board(window, bg_black, player_board, player_solve, 'graham solve', 'player')
            else:
                update_timer(window, timer, bg_black)

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    sleep(3)
    main()
    pygame.quit()