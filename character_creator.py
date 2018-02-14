import sqlite3
import time
from pudb import set_trace

RESET = '\33[0m'
VERMELHO = '\33[31m'
VERDE = '\33[33m'
AZUL = '\33[34m'

class Character(object):
    nome = 'Nome genérico'
    amigavel = True
    vida = 2
    ataque = 2
    defesa = 2
    droplist = '' 
    equipamento = '' 

    def atacar(self, inimigo):
        pass

    def __str__(self):
        return ('Nome: {}\nAmigavel: {}\nVida: {}\n' + \
        'Ataque: {}\nDefesa: {}\nDroplist: {}\nEquipamentos: {}').format(
            self.nome, self.amigavel, self.vida, self.ataque, self.defesa,
            self.droplist, self.equipamento)

class Item(object):
    nome = 'Item genérico'
    descricao = 'Lorem ipsum? Descricao Genérica!'
    equipavel = False
    ataque = 0
    defesa = 0
    valor = 1

    def __str__(self):
        return ('Nome: {}\nDescrição: {}\nEquipável: {}\nAtaque: {}\nDefesa: {}\nValor: {}').format(
            self.nome, self.descricao, self.equipavel, self.ataque, self.defesa, self.valor)

def create_table(cur):
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS characters (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            amigavel INTEGER NOT NULL,
            vida INTEGER NOT NULL,
            ataque INTEGER NOT NULL,
            defesa INTEGER NOT NULL,
            droplist TEXT,
            equipamento TEXT);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS items (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            ataque INTEGER NOT NULL,
            defesa INTEGER NOT NULL,
            valor REAL NOT NULL);""")
    except Exception as e:
        print(VERMELHO + 'Erro inesperado:' + RESET + e )

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
        retorno = input('{}: '.format(texto))
        if retorno in ['s', 'n']:
            break
        else:
            print('Valor invalido.')
            print('\33[3A')
            print('\33[2K')
            print('\33[2A')
    print('\33[2K')
    print('\33[2A')
    return retorno

def getCharacterById(char_id, cursor):
    try:
        cursor.execute('SELECT * FROM characters WHERE id = ?', (char_id,))
        char = Character()
        row = cursor.fetchone()

        if row:
            char.nome = row[1]
            char.amigavel = row[2]
            char.vida = row[3]
            char.ataque = row[4]
            char.defesa = row[5]
            char.droplist = row[6]
            char.equipamento = row[7]
            return char
    except sqlite3.DatabaseError as e:
        print(e)

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

print(VERMELHO)
print('Conectando ao banco de dados...')
conn = sqlite3.connect('data.db')

if conn != None:
    print('Acesso ao banco de dados: OK\nDefinindo cursor...')
    cursor = conn.cursor()
    print('Inicializando tabelas...')
    create_table(cursor)
    print(AZUL + 'Iniciando programa...' + RESET)
    time.sleep(1)

    while True:
        cls()
        print('\33[34mGERADOR DE ENTIDADES - versao alpha 0.1\33[0m')
        print('  1. Criar nova entidade')
        print('  2. Visualizar personagem')
        print('  3. Editar personagem')
        print('  4. Deletar personagem')
        print('  0. Sair')

        c = None
        try:
            c = int(input(VERMELHO +'\n\nOpcão: '))
        except ValueError:
            print('Opcao invalida')
        print(RESET)
        if c == 0:
            conn.close()
            break
        elif c == 1:
            while True:
                cls()
                print('1. Personagem\n2. Item\n0. Voltar')
                c = getValor(VERMELHO + 'Opção')
                print(RESET)
                if c == 1:
                    while True:
                        cls()
                        print(AZUL + 'NOVO PERSONAGEM\n' + RESET)
                        personagem = Character()
                        personagem.nome = input('Nome: ')
                        personagem.amigavel = getSimNao('Amigavel (s/n)')
                        personagem.vida = getValor('Vida')
                        personagem.ataque = getValor('Ataque')
                        personagem.defesa = getValor('Defesa')

                        cls()
                        print(personagem)
                        if getSimNao('Os dados estão corretos? (s/n): ') == 's':
                            cursor.execute("""INSERT INTO characters 
                            (nome, amigavel, vida, ataque, defesa, droplist, equipamento)
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            (personagem.nome, personagem.amigavel, personagem.vida, personagem.ataque, 
                            personagem.defesa, personagem.droplist, personagem.equipamento))

                            conn.commit()
                            break
                if c == 2: 
                    while True:
                        cls()
        elif c == 2:
            cls()
            try:
                cursor.execute('SELECT * FROM characters')
                for row in cursor:
                    print(('ID: {}\nNome: {}\nAmigavel: {}\nVida: {}\n' + \
                    'Ataque: {}\nDefesa: {}\nDroplist: {}\nEquipamentos: {}').format(
                    row[0], row[1], row[2], row[3], row[4],
                    row[5], row[6], row[7]))
                    while True:
                        if getSimNao('Próximo? (s/n)') == 's':
                            break
            except sqlite3.OperationalError as e:
                print('Tabela de personagens não existe.\nFavor adicionar um personagem')
                input('Aperte qualquer tecla para sair')
        elif c == 3:
            cls()
            print('EDICAO DE PERSONAGEM\n')
            char_id = input('ID do Personagem: ')
            char = getCharacterById(char_id, cursor)
            if(char):
                char = editCharacter(char)
                cursor.execute("""UPDATE characters SET nome = ?, amigavel =  ?, vida = ?, ataque = ?,
                defesa = ?, droplist = ?, equipamento = ? WHERE ID = ?""",
                    (char.nome, char.amigavel, char.vida, char.ataque,
                    char.defesa, char.droplist, char.equipamento, char_id))
                cls()
                print(char)
                while True:
                    if getSimNao(VERMELHO + 'Commitar mudanças? (s/n)' + RESET ) == 's':
                        conn.commit()
                        break
                    else:
                        conn.rollback()
                        break
                input('Aperta qualquer tecla para sair')
            else:
                print('Nenhum registro encontrado')
                input('Aperta qualquer tecla para sair')
        elif c == 4:
            cls()
            print('DELETAR PERSONAGEM')
            char_id = getValor('ID')
            char = getCharacterById(char_id, cursor)
            print(char)
            while True:
                if getSimNao('\33[31mDeseja realmente deletar esse personagem? (s/n) \33[0m') == 's':
                    cursor.execute('DELETE FROM characters WHERE ID = ?', (char_id,))
                    conn.commit()
                    print('Cadastro deletado')
                    input('Aperta qualquer tecla para sair')
                    break;
                else:
                    break;
        else:
            print('Opcao invalida')
else:
    print('Erro ao abrir arquivo do banco de dados.')

