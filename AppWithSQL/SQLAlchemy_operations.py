from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import select, func

Base = declarative_base()


class Usuario(Base):
    """
    Esta classe representa a tabela user_account dentro
    do SQlite.
    """
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    nome_completo = Column(String)

    endereco = relationship(
        "Endereco", back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, nome_completo={self.nome_completo})"


class Endereco(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    endereco_email = Column(String(30), nullable=False)
    usuario_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="endereco")

    def __repr__(self):
        return f"Endereco(id={self.id}, endereco_email={self.endereco_email})"


def create_engine_and_tables():
    engine = create_engine("sqlite://")

    Base.metadata.create_all(engine)

    return engine


def insert_users_data(session):
    fernanda = Usuario(
        nome='fernanda',
        nome_completo='Fernanda Silva',
        endereco=[Endereco(endereco_email='fernanda@example.com')]
    )

    carine = Usuario(
        nome='carine',
        nome_completo='Carine Souza',
        endereco=[Endereco(endereco_email='carine@example.com'),
                 Endereco(endereco_email='carine2@example.com')]
    )

    jose = Usuario(nome='jose', nome_completo='José da Silva')

    session.add_all([fernanda, carine, jose])
    session.commit()


def retrieve_users_by_name(session):
    stmt = session.query(Usuario).filter(Usuario.nome.in_(["fernanda", 'carine']))
    print('Recuperando usuários a partir de condição de filtragem')
    for user in stmt:
        print(user)


def retrieve_addresses_by_user_id(session, user_id):
    stmt_address = session.query(Endereco).filter(Endereco.usuario_id == user_id)
    print('\nRecuperando os endereços de email')
    for address in stmt_address:
        print(address)


def retrieve_users_ordered_by_fullname(session):
    stmt_order = session.query(Usuario).order_by(Usuario.nome_completo.desc())
    print("\nRecuperando info de maneira ordenada")
    for result in stmt_order:
        print(result)


def retrieve_users_and_addresses(session):
    stmt_join = session.query(Usuario.nome_completo, Endereco.endereco_email).join(Usuario)
    print("\nRecuperando usuários e seus endereços")
    for result in stmt_join:
        print(result)


def retrieve_users_and_addresses_with_connection(engine):
    with engine.connect() as connection:
        stmt_join = select(Usuario.nome_completo, Endereco.endereco_email).join(Usuario)
        results = connection.execute(stmt_join).fetchall()
        print("\nExecutando statement a partir da connection")
        for result in results:
            print(result)


def retrieve_user_count(session):
    stmt_count = session.query(func.count('*')).select_from(Usuario)
    print('\nTotal de instâncias em Usuario')
    for result in stmt_count:
        print(result[0])


def main():
    engine = create_engine_and_tables()

    Session = Session(bind=engine)
    session = Session()

    insert_users_data(session)

    retrieve_users_by_name(session)
    retrieve_addresses_by_user_id(session, user_id=2)
    retrieve_users_ordered_by_fullname(session)
    retrieve_users_and_addresses(session)
    retrieve_users_and_addresses_with_connection(engine)
    retrieve_user_count(session)

    session.close()


if __name__ == "__main__":
    main()
