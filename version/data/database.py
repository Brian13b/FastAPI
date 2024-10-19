import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DB_URL = "postgresql+psycopg2://postgres:utn228@localhost:5432/utn"
DB_TEST_CONNECTION = "postgresql+psycopg2://postgres:utn228@localhost:5432/utn_test"
logger = logging.getLogger(__name__)

class OrmBase(DeclarativeBase):                                                              # Clase base para las tablas de la base de datos
    pass                                                                                     # No tiene métodos, solo se usa para heredar de ella


class Database():                                                                            # Clase para manejar la conexión a la base de datos
    def __init__(self, connection_string: str = SQLALCHEMY_DB_URL, echo: bool = True):       # Constructor de la clase Database con dos parámetros
        self.logger = logger
        self.logger.info('Clase Database usando logger %s', self.logger.name)                # Se muestra un mensaje de información con el nombre del logger
        self.echo = echo                                                                     # echo es un parámetro opcional que indica si se muestran los mensajes de SQL en la consola
        self.set_connection_string(connection_string)                                        # Llama al método set_connection_string con el parámetro connection_string
    
    def set_connection_string(self, connection_string: str):                                  # Método para establecer la cadena de conexión a la base de datos
        self.engine = create_engine(connection_string, echo=self.echo)                            # echo es un parámetro opcional que indica si se muestran los mensajes de SQL en la consola


    @property
    def SessionLocal(self):                                                                  # Propiedad de la clase Database para obtener la sesión de la base de datos
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)             # Retorna una sesión de la base de datos con autocommit y autoflush en False. Sessionmaker crea una sesión de la base de datos

    def create_all(self):
        self.logger.info('Creating all tables')
        OrmBase.metadata.create_all(bind=self.engine)

    def drop_all(self):    
        self.logger.info('Creating all tables')                                                                 # Método para eliminar todas las tablas de la base de datos
        OrmBase.metadata.drop_all(bind=self.engine)                                         # Elimina todas las tablas de la base de datos

    def get_db(self):
        self.logger.debug('Getting DB session')
        db = self.SessionLocal()
        try:
            yield db
        finally:
            self.logger.debug('Closing DB session')
            db.close()

db_instance = Database()                                                            # Instancia de la clase Database para manejar la conexión a la base de datos

def connect_to_prod(with_echo: bool = False):                                # Función para crear una instancia de la base de datos con la conexión a la base de datos de producción
    global db_instance                                                              # con global indicamos que la variable db_instance es la global y no una variable local
    logger.debug(f'Connecting to prod DB (echo={with_echo})')                       # Se muestra un mensaje de depuración con el valor de with_echo
    db_instance.echo = with_echo                                                    # Se asigna el valor de with_echo al atributo echo de la instancia de la base de datos
    db_instance = Database(SQLALCHEMY_DB_URL)                       # Aca se crea la instancia de la base de datos con la conexión a la base de datos de producción

def connect_to_test(with_echo: bool = False):                                # Función para crear una instancia de la base de datos con la conexión a la base de datos de pruebas
    global db_instance
    logger.debug(f'Connecting to test DB (echo={with_echo})')
    db_instance.echo = with_echo
    db_instance = Database(DB_TEST_CONNECTION)
    