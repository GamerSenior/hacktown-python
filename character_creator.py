import sqlite3
from pudb import set_trace

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

def create_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS characters (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        amigavel INTEGER NOT NULL,
        vida INTEGER NOT NULL,
        ataque INTEGER NOT NULL,
        defesa INTEGER NOT NULL,
        droplist TEXT,
        equipamento TEXT);""")

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
    print('Caso não deseje alterar os valores, deixar em branco')
    val = input('Nome: {} -> '.format(char.nome))
    if val.strip():
        char.nome = val

    val = input('Amigavel: {} -> '.format(char.amigavel))
    if val.strip():
        char.amigavel = val

    val = input('Vida: {} -> '.format(char.vida))
    if val.strip():
        char.vida = val

    val = input('Ataque: {} -> '.format(char.ataque))
    if val.strip():
        char.ataque = val

    val = input('Defesa: {} -> '.format(char.defesa))
    if val.strip():
        char.defesa = val

    val = input('Droplist: {} -> '.format(char.droplist))
    if val.strip():
        char.droplist = val

    val = input('Equipamento: {} -> '.format(char.equipamento))
    if val.strip():
        char.droplist= val

    return char

print('Conectando ao banco de dados...')
conn = sqlite3.connect('data.db')

if conn != None:
    print('Acesso ao banco de dados: OK\nDefinindo cursor...')
    cursor = conn.cursor()

    print('Iniciando programa...')

    while True:
        cls()
        print('Criador de Personagens - versao alpha')
        print('1. Criar novo personagem')
        print('2. Visualizar personagem')
        print('3. Editar personagem')
        print('4. Deletar personagem')
        print('0. Sair')

        c = None
        try:
            c = int(input('\n\nOpcão: '))
        except ValueError:
            print('Opcao invalida')
        if c == 0:
            conn.close()
            break
        elif c == 1:
            while True:
                cls()
                create_table(cursor)
                print('NOVO PERSONAGEM\n')
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
        elif c == 2:
            cls()
            cursor.execute('SELECT * FROM characters')
            for row in cursor:
                print(('ID: {}\nNome: {}\nAmigavel: {}\nVida: {}\n' + \
                    'Ataque: {}\nDefesa: {}\nDroplist: {}\nEquipamentos: {}').format(
                    row[0], row[1], row[2], row[3], row[4],
                    row[5], row[6], row[7]))
                while True:
                    if getSimNao('Próximo? (s/n)') == 's':
                        break
        elif c == 3:
            cls()
            print('EDICAO DE PERSONAGEM\n')
            char_id = input('ID do Personagem: ')
            char = getCharacterById(char_id, cursor)
            char = editCharacter(char)
            cursor.execute("""UPDATE characters SET nome = ?, amigavel =  ?, vida = ?, ataque = ?,
            defesa = ?, droplist = ?, equipamento = ? WHERE ID = ?""",
                (char.nome, char.amigavel, char.vida, char.ataque,
                char.defesa, char.droplist, char.equipamento, char_id))
            cls()
            print(char)
            while True:
                if getSimNao('Commitar mudanças? (s/n)' ) == 's':
                    conn.commit()
                else:
                    conn.rollback()
            input('')
        elif c == 4:
            cls()
            print('DELETAR PERSONAGEM')
            char_id = getValor('ID')
            char = getCharacterById(char_id, cursor)
            print(char)
            while True:
                if getSimNao('Deseja realmente deletar esse personagem? (s/n) ') == 's':
                    cursor.execute('DELETE FROM characters WHERE ID = ?', (char_id,))
                    conn.commit()
                    print('Cadastro deletado')
                    input('')
                    break;
                else:
                    break;
        else:
            print('Opcao invalida')
else:
    print('Erro ao abrir arquivo do banco de dados.')

