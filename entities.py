from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from const import *

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)
    nome = Column(String(60), nullable = False)
    descricao = Column(String(250), nullable = False)
    equipavel = Column(Boolean, nullable = False)
    ataque = Column(Integer, nullable = False)
    defesa = Column(Integer, nullable = False)
    valor = Column(Float, nullable = False)
    quantidade = Column(Integer, nullable = False)

    def __str__(self):
        return ('Nome: ' + AZUL + '{}'+ RESET +'\nDescrição: ' + AZUL +'{}'+ RESET +'\
                \nEquipável: ' + AZUL +'{}'+ RESET +'\nAtaque: ' + AZUL +'{}'+ RESET +'\
                \nDefesa: ' + AZUL +'{}'+ RESET +'\nValor: ' + AZUL +'{}'+ RESET +'').format(
            self.nome, self.descricao, self.equipavel, self.ataque, self.defesa, self.valor)

    def __init__(self, nome, descricao, equipavel, ataque, defesa, valor, quantidade = 1):
        self.nome = nome
        self.descricao = descricao
        self.equipavel = equipavel
        self.ataque = ataque
        self.defesa = defesa
        self.valor = valor
        self.quantidade = quantidade

    def create_table():
        engine = create_engine('sqlite:///data.db')
        Base.metadata.create_all(engine)

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key = True)
    nome = Column(String(60), nullable = False)
    amigavel = Column(Boolean, nullable = False)
    vida = Column(Integer)
    ataque = Column(Integer)
    defesa = Column(Integer)
    droplist = relationship('Droplist')
    mochila = relationship('Mochila') 

    def atacar(self, inimigo):
        pass

    def __init__(self, nome, amigavel, vida, ataque, defesa, droplist = [], mochila = []):
        self.nome = nome
        self.amigavel = amigavel
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.droplist = droplist
        self.mochila = mochila

    def create_table():
        engine = create_engine('sqlite:///data.db')
        Base.metadata.create_all(engine)

    def getDroplist(self):
        nomeItems = []
        for droplist in self.droplist:
            nomeItems.append(droplist.item.nome)
        return nomeItems

    def getMochila(self):
        nomeItems = []
        for mochila in self.mochila:
            nomeItems.append(mochila.item.nome)
        return nomeItems

    def __str__(self):
        return ('Nome:'+ AZUL +' {}'+ RESET +'\nAmigavel: '+ AZUL +'{}'+ RESET +'\
                \nVida: '+ AZUL +'{}'+ RESET +'\n' + 'Ataque: '+ AZUL +'{}'+ RESET +'\
                \nDefesa: '+ AZUL +'{}'+ RESET +'\nDroplist: '+ AZUL +'{}'+ RESET +'\
                \nEquipamentos: '+ AZUL +'{}'+ RESET +'').format(
            self.nome, self.amigavel, self.vida, self.ataque, self.defesa,
            self.getDroplist(), self.getMochila())

class Mochila(Base):
    __tablename__ = 'backpack'
    item_id = Column(Integer, ForeignKey('item.id'), primary_key = True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key = True)
    item = relationship('Item')

class Droplist(Base):
    __tablename__ = 'droplist'
    item_id = Column(Integer, ForeignKey('item.id'), primary_key = True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key = True)
    dropchance = Column(Float, nullable = False)
    item = relationship('Item')
