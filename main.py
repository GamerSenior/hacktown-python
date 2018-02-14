#!/usr/bin/env python
# -*- coding: utf-8 -*-
import curses
import time
import pudb
from datetime import datetime

MENU_INICIAL = [
    "Iniciar jogo",
    "Carregar",
    "Opcoes",
    "Creditos",
    "Sair"
    ]

def init(stdscr):
    """Inicializa o curses e atribui parametros essenciais para o programa"""

    #Inicia o sistema de cores
    curses.start_color()
    #Deixa de imprimir as teclas no console
    curses.noecho()
    #Permite o input sem ser necessario o ENTER
    curses.cbreak()
    #Permite o uso de teclas especiais
    stdscr.keypad(True)

def close(stdscr):
    """Libera memoria e finaliza os processos antes de fechar o programa"""
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def start_screen(stdscr):
    """Menu inicial do programa"""
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    running = True
    cursor_y = 0
    key_pressed = 0

    while running:
        for item in MENU_INICIAL:
            if MENU_INICIAL.index(item) == (cursor_y):
                stdscr.addstr(MENU_INICIAL.index(item), 0, item, curses.color_pair(1) | curses.A_BOLD)
            else:
                stdscr.addstr(MENU_INICIAL.index(item), 0, item, curses.color_pair(1))

        stdscr.addstr(curses.LINES - 2, 0, 'Key Pressed: {} Cursor_Y: {}'.format(key_pressed, cursor_y))
        stdscr.addstr(curses.LINES - 1, 0, 'HackTown ALHPA 0.1 by Giovani Garcia',
                      curses.color_pair(1))

        key_pressed = stdscr.getkey()
        #pudb.set_trace()

        if key_pressed == 'q':
            running = False
        elif key_pressed == 'KEY_DOWN':
            if cursor_y == len(MENU_INICIAL) - 1:
                cursor_y = 0
            else:
                cursor_y += 1
        elif key_pressed == 'KEY_UP':
            if cursor_y == 0:
                cursor_y = len(MENU_INICIAL) - 1
            else:
                cursor_y -= 1
        elif key_pressed == '\n':
            running = False
            return MENU_INICIAL[cursor_y]

        stdscr.move(cursor_y, 0)

        stdscr.clear()
        stdscr.refresh()

def credit_screen(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.clear();
    stdscr.addstr(0, 0, 'Prototype made by Giovani Garcia')
    stdscr.addstr(1, 0, 'Student and Programmer, born and raised in Brazil')
    stdscr.addstr(curses.LINES - 2, 0, 'Contact: abelgiovani@gmail.com')
    stdscr.addstr(curses.LINES - 1, 0, 'Press Q to go back')
    stdscr.refresh()

    while True:
        c = stdscr.getch()
        pudb.set_trace()
        if c == ord('q'):
            break

def scene_manager(stdscr):
    running = True
    tela_inicial = True

    while running:
        if(tela_inicial):
            scene = start_screen(stdscr)
            tela_inicial = False
        #NOVO JOGO
        if scene == MENU_INICIAL[0]:
            pass
        #CARREGAR
        if scene == MENU_INICIAL[1]:
            pass
        #OPCOES
        if scene == MENU_INICIAL[2]:
            pass
        #CREDITOS
        if scene == MENU_INICIAL[3]:
            credit_screen(stdscr)
            tela_inicial = True
        #SAIR
        if scene == MENU_INICIAL[4]:
            running = False

def main(stdscr):
    """Função principal... durr"""
    stdscr = curses.initscr()

    init(stdscr)

    stdscr.clear()

    scene_manager(stdscr)
#    start_screen(stdscr)

    close(stdscr)

curses.wrapper(main)
