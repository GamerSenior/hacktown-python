import sqlite3
import time
from pudb import set_trace
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from const import *

from entities import Item, Character, Droplist, Base


def move(x, y):
    print('\033[{};{}H'.format(x, y))

def cls():
    print(chr(27) + "[2J")
    move(0, 0)

def getValor(texto):
    retorno = None
    while True:
        try:
            retorno = int(input('{}: '.format(texto)))
            break
        except ValueError:
            print('Valor invalido.')
            print('\33[3A')
            print('\33[2K')
            print('\33[2A')
    print('\33[2K')
    print('\33[2A')
    return retorno

def getSimNao(texto):
    retorno = None
    while True:
        retorno = input('{} (s/n): '.format(texto)).lower()
        if retorno in ['s', 'n']:
            if retorno == 's':
                retorno = True
            else:
                retorno = False
            break
        else:
            print('Valor invalido.')
            print('\33[3A')
            print('\33[2K')
            print('\33[2A')
    print('\33[2K')
    print('\33[2A')
    return retorno

def editCharacter(char):
    print(VERMELHO + 'Caso não deseje alterar os valores, deixar em branco' + RESET)
    val = input((RESET + 'Nome: {} -> ' + AZUL).format(char.nome))
    if val.strip():
        char.nome = val

    val = input((RESET + 'Amigavel: {} -> ' + AZUL).format(char.amigavel))
    if val.strip():
        char.amigavel = val

    val = input((RESET + 'Vida: {} -> ' + AZUL).format(char.vida))
    if val.strip():
        char.vida = val

    val = input((RESET + 'Ataque: {} -> ' + AZUL).format(char.ataque))
    if val.strip():
        char.ataque = val

    val = input((RESET + 'Defesa: {} -> ' + AZUL).format(char.defesa))
    if val.strip():
        char.defesa = val

    val = input((RESET + 'Droplist: {} -> ' + AZUL).format(char.droplist))
    if val.strip():
        char.droplist = val

    val = input((RESET + 'Equipamento: {} -> ' + AZUL).format(char.equipamento))
    if val.strip():
        char.droplist= val
    print(RESET)
    return char

def editItem(item):
    print(VERMELHO + 'Caso não deseje alterar os valores, deixar em branco' + RESET)
    val = input((RESET + 'Nome: {} -> ' + AZUL).format(item.nome))
    if val.strip():
        item.nome = val

    val = input((RESET + 'Equipavel: {} -> '+ AZUL).format(item.descricao))
    if val.strip():
        item.descricao = val

    val = getSimNao((RESET + 'Equipavel: {} -> ' + AZUL).format(item.equipavel))

    val = input((RESET + 'Ataque: {} -> ' + AZUL).format(item.ataque))
    if val.strip():
        item.ataque = int(val)

    val = input((RESET + 'Defesa: {} -> ' + AZUL).format(item.defesa))
    if val.strip():
        item.defesa = int(val)

    val = input((RESET + 'Valor : {} -> ' + AZUL).format(item.valor))
    if val.strip():
        item.valor = int(val)

    print(RESET)
    return item

def createDroplist(char):
    while True:
        droplist = Droplist()
        item_id = getValor('ID Item: ')
        try:
            item = session.query(Item).filter_by(id = item_id).first()
            droplist.item = item
            droplist.character = char
            while True:
                val = getValor('Chance de drop (1~100)')
                if val > 1 and val < 100:
                    break
            droplist.dropchance = val
            char.droplist.append(droplist)
        except Exception as e:
            print('Erro inesperado:\n'+ VERMELHO + e + RESET)
        if getSimNao('Deseja adicionar outro item?') == False:
            break

print(VERMELHO)
cls()
print('Conectando ao banco de dados...')

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

if session != None:
    time.sleep(.3)
    print('Acesso ao banco de dados:'+AZUL+' OK'+RESET)
    time.sleep(.3)
    print('Inicializando tabelas...')
    Item.create_table()
    Character.create_table()
    time.sleep(.3)
    print(AZUL + 'Iniciando programa...' + RESET)
    time.sleep(.5)

    ### MENU PRINCIPAL ###
    while True:
        cls()
        print('\33[34mGERADOR DE ENTIDADES - versao alpha 0.1\33[0m')
        print('  1. Criar nova entidade')
        print('  2. Visualizar entidades')
        print('  3. Editar entidade')
        print('  4. Deletar entidade')
        print('  0. Sair')

        c = None
        try:
            c = int(input(VERMELHO +'\n\nOpcão: '))
        except ValueError:
            print('Opcao invalida')
        print(RESET)
        if c == 0:
            session.close()
            break
        elif c == 1:
            while True:
                cls()
                print(AZUL + 'ADICIONAR NOVA ENTIDADE' + RESET)
                print('1. Personagem\n2. Item\n0. Voltar')
                c = getValor(VERMELHO + 'Opção')
                print(RESET)
                if c == 1:
                    while True:
                        cls()
                        print(AZUL + 'NOVO PERSONAGEM\n' + RESET)

                        nome = input('Nome: ')
                        amigavel = getSimNao('Amigavel')
                        vida = getValor('Vida')
                        ataque = getValor('Ataque')
                        defesa = getValor('Defesa')
                        personagem = Character(nome, amigavel, vida, ataque, defesa)
                        if getSimNao('Deseja adcionar itens ao droplist?'):
                            createDroplist(personagem)
                        session.add(personagem)
                        set_trace()
                        cls()
                        print(personagem)
                        if getSimNao('Os dados estão corretos?'):
                            session.commit()
                            break
                        else:
                            session.rollback()
                if c == 2:
                    while True:
                        cls()
                        print(AZUL + 'NOVO ITEM\n' + RESET)
                        nome = input('Nome: ')
                        descricao = input('Descrição: ')
                        equipavel = getSimNao('Equipável')
                        ataque = getValor('Ataque')
                        defesa = getValor('Defesa')
                        valor = getValor('Valor')
                        item = Item(nome, descricao, equipavel,  ataque, defesa, valor)
                        session.add(item)
                        cls()
                        print(item)
                        if getSimNao('Os dados estão corretos?'):
                            session.commit()
                            break
                        else:
                            session.rollback()
                if c == 0:
                    break
        elif c == 2:
            while True:
                cls()
                print(AZUL + 'VISUALIZAR ENTIDADES' +RESET)
                print('1. Personagens')
                print('2. Items')
                print('0. Voltar')
                c = getValor(VERMELHO + '\n\nOpção' + RESET)

                if c == 1:
                    try:
                        cls()
                        lista = session.query(Character).all()
                        sair = False
                        for personagem in lista:
                            print('\n##############################')
                            print(personagem)
                            print('##############################')
                            while True:
                                if getSimNao(VERMELHO + 'Próximo?' + RESET):
                                    break
                                else:
                                    sair = True
                                    break
                            if sair:
                                break
                    except Exception as e:
                        print('Tabela de personagens não existe.\n' + VERMELHO + e)
                        input('\nAperte qualquer tecla para sair' + RESET)
                elif c == 2:
                    while True:
                        cls()
                        print('1. Listar todos')
                        print('2. Buscar por ID')
                        print('0. Voltar')
                        c = getValor(VERMELHO + '\n\nOpção: ' + RESET)

                        if c == 1:
                            cls()
                            print(AZUL + 'LISTA DE ITEMS' + RESET)
                            lista = session.query(Item).all()
                            for item in lista:
                                print(str(item.id) + '. ' + item.nome)
                            input('Pressione qualquer tecla para voltar')
                        elif c == 2:
                            cls()
                            print(AZUL + 'BUSCAR ITEM POR ID' + RESET)
                            item_id = getValor('ID do Item: ')
                            item = session.query(Item).filter_by(id = item_id).first()
                            print(AZUL+'\n##############################'+RESET)
                            print(item)
                            print(AZUL+'\n##############################'+RESET)
                            input(VERMELHO+'Pressione qualquer tecla para voltar'+RESET)
                        elif c == 0:
                            break
                elif c == 0:
                    break
        elif c == 3:
            while True:
                cls()
                print('EDIÇÃO DE ENTIDADES\n')
                print('1. Personagem')
                print('2. Item')
                print('0. Voltar')
                c = getValor(VERMELHO + '\n\nOpção'+ RESET)

                if c == 1:
                    cls()
                    print(AZUL+'EDICAO DE PERSONAGEM'+RESET)
                    char_id = getValor('ID do Personagem')
                    char = session.query(Character).filter_by(id = char_id).first()
                    if(char):
                        char = editCharacter(char)
                        session.add(char)
                        cls()
                        print(char)
                        while True:
                            if getSimNao(VERMELHO + 'Commitar mudanças?' + RESET ):
                                session.commit()
                                break
                            else:
                                session.rollback()
                                break
                        input('Aperta qualquer tecla para sair')
                    else:
                        print('Nenhum registro encontrado')
                        input('Aperta qualquer tecla para sair')
                elif c == 2:
                    cls()
                    print(AZUL+'EDICAO DE ITEM'+RESET)
                    item_id = getValor('ID do Item')
                    item = session.query(Item).filter_by(id = item_id).first()
                    if(item):
                        item = editItem(item)
                        session.add(item)
                        cls()
                        print(item)

                        while True:
                            if getSimNao(VERMELHO + 'Commitar mudanças?' + RESET ):
                                session.commit()
                                break
                            else:
                                session.rollback()
                                break
                    else:
                        print('Nenhum registro encontrado')
                    input(VERMELHO+'Aperta qualquer tecla para sair'+RESET)
                elif c == 0:
                    break
        elif c == 4:
            cls()
            print('DELETAR PERSONAGEM')
            char_id = getValor('ID')
            char = session.query(Character).filter_by(id = char_id).first()
            session.delete(char)
            print(char)
            while True:
                if getSimNao('\33[31mDeseja realmente deletar esse personagem?\33[0m'):
                    session.commit()
                    print('Cadastro deletado')
                    input('Aperta qualquer tecla para sair')
                    break;
                else:
                    session.rollback()
                    break;
        else:
            print('Opcao invalida')
else:
    print('Erro ao abrir arquivo do banco de dados.')
