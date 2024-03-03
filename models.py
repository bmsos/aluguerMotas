from sqlalchemy import Column, ForeignKey, Table
# from sqlalchemy.ext.declarative import declarative_base   # DEPRECATED (desde v2.0 em sqlalchemy.orm)
from sqlalchemy.types import Integer, Text, String, DateTime, Float, Date, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from database import engine, session
from sqlalchemy.dialects.mysql import TINYINT

Base = declarative_base()


# ----- opcional ------
# se não for usada,, apagar o campo promocao_id da tabela Aluguer
'''
class Promocao(Base):
    __tablename__ = 'promocao'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    nome = Column(String(100), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    desconto = Column(Float, nullable=False)

    alugueres = relationship('Aluguer', backref='promocao', lazy='dynamic')

    def __repr__(self):
        return f'<Promocao {self.nome}>'
''' 
# -----------    

class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    nome = Column(String(30), nullable=False, unique=True)
    badge_style = Column(String(300), nullable=False)

    motas = relationship('Mota', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria {self.nome}>'
    

class Mota(Base):
    __tablename__= 'mota'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    marca = Column(String(50), nullable=False)
    modelo = Column(String(100), nullable=False)
    cilindrada = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)

    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=False)

    is_rented = Column(TINYINT, nullable=False, default=0)
    
    imagem1 = Column(String(300), nullable=False, default='public/assets/img/projects/1.jpg')
    imagem2 = Column(String(300), nullable=False, default='public/assets/img/shop/single1.jpg')
    imagem3 = Column(String(300), nullable=False, default='public/assets/img/shop/single2.jpg')
    imagem4 = Column(String(300), nullable=False, default='public/assets/img/shop/single3.jpg')

    alugueres = relationship('Aluguer', backref='mota', lazy='dynamic')

    def __repr__(self):
        return f'<Mota {self.marca} {self.modelo}>'


class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    nome = Column(String(30), nullable=False)
    apelido = Column(String(40), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    profile_img = Column(String(500), default='private/assets/img/user_profile/user_profile_default.jpg')
    admin = Column(TINYINT, nullable=False, default=0)

    alugueres = relationship('Aluguer', backref='cliente', lazy='dynamic')

    def __repr__(self):
        return f'<Cliente {self.nome} {self.apelido} {self.email}>'


class Aluguer(Base):
    __tablename__ = 'aluguer'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    levantamento = Column(DateTime, nullable=False)
    entrega = Column(DateTime, nullable=False)
    
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    # promocao_id = Column(Integer, ForeignKey('promocao.id'), nullable=False)
    mota_id = Column(Integer, ForeignKey('mota.id'), nullable=False, unique=True)

    def __repr__(self):
        return f'<Aluguer {self.cliente.nome} {self.cliente.apelido} {self.levantamento} {self.entrega}>'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    urbana = Categoria(nome='Urbana', badge_style='style="background-color:#69349e"')
    trail = Categoria(nome='Trail', badge_style='style="background-color:#206a8c"')
    cruiser = Categoria(nome='Cruiser', badge_style='style="background-color:#27a34c"')
    scrambler = Categoria(nome='Scrambler', badge_style='style="background-color:#bfa119"')
    desportiva = Categoria(nome='Desportiva', badge_style='style="background-color:#a82323"')
    touring = Categoria(nome='Touring', badge_style='style="background-color:#1a3eab"')    

    session.add_all([urbana, trail, cruiser, scrambler, desportiva, touring])
    session.commit()

    # OPCIONAL (PARA TESTES INICIAIS) -----------------------------------------------
    hayabusa = Mota(marca='Suzuki', modelo='Hayabusa', cilindrada= 1340, ano=2019, preco=320.00, categoria_id=5, is_rented=1, imagem1='public/assets/img/motas/c1215720-2c37-11ee-99f6-d4939001689d_hayabusa.jpg')
    dn01 = Mota(marca='Honda', modelo='DN-01', cilindrada= 680, ano=2008, preco=200.00, categoria_id=6, imagem1='public/assets/img/motas/b4f80f09-2c37-11ee-8e30-d4939001689d_honda_dn01.jpg')
    sportster = Mota(marca='Harley-Davidson', modelo='Sportster S', cilindrada= 1252, ano=2020, preco=400.00, categoria_id=4, is_rented=1, imagem1='public/assets/img/motas/5fcc93b7-2c37-11ee-8d21-d4939001689d_hd_sportster.jpg')
    jetX = Mota(marca='SYM', modelo='Jet X', cilindrada= 125, ano=2022, preco=41.60, categoria_id=1, is_rented=1, imagem1='public/assets/img/motas/bb9c4551-2c37-11ee-9fae-d4939001689d_sym_jet_x.jpg')
    trk502X = Mota(marca='Benelli', modelo='TRK 502X', cilindrada= 499, ano=2018, preco=74.99, categoria_id=2, imagem1='public/assets/img/motas/88f86d68-2c37-11ee-b892-d4939001689d_trk502.jpg')
    midnightstar = Mota(marca='Yamaha', modelo='Midnight Star', cilindrada= 1900, ano=2010, preco=145.59, categoria_id=3, is_rented=1, imagem1='public/assets/img/motas/ae22ff5f-2c37-11ee-8002-d4939001689d_yamaha_minight_star.jpg')

    carlos = Cliente(nome='Carlos', apelido='Coimbra', email='carlos@gmail.com', password='carlos123', admin=1, profile_img='private/assets/img/user_profile/996260c4-29d8-11ee-b8cd-d4939001689d_carlos.jpg')
    ana = Cliente(nome='Ana', apelido='Almeida', email='ana@gmail.com', password='ana123', profile_img='private/assets/img/user_profile/d74b9a8b-29d8-11ee-8d71-d4939001689d_ana.jpg')

    aluguer1 = Aluguer(levantamento='2023-07-06 05:15:00', entrega='2023-07-07 06:15:00', cliente_id=1, mota_id=1)
    aluguer2 = Aluguer(levantamento='2023-08-05 05:15:00', entrega='2023-08-12 12:15:00', cliente_id=2, mota_id=3)
    aluguer3 = Aluguer(levantamento='2023-09-23 05:24:00', entrega='2023-10-29 05:12:00', cliente_id=2, mota_id=4)
    aluguer4 = Aluguer(levantamento='2023-07-08 05:15:00', entrega='2023-08-06 05:15:00', cliente_id=1, mota_id=6)

    session.add_all([hayabusa, dn01, sportster, jetX, trk502X, midnightstar])
    session.add_all([carlos, ana])
    session.add_all([aluguer1, aluguer2, aluguer3, aluguer4])
    session.commit()