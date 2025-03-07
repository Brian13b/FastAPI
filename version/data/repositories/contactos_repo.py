import logging
from sqlalchemy import select, Sequence, Row
from sqlalchemy.orm import Session, aliased

from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto
from domain.model.direccion import Direccion
from domain.model.localidad import Localidad


class ContactosRepo:
    """
    Repositorio de contactos, en base de datos
    """

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    # region Métodos CRUD
    def get_all(self, db: Session) -> Sequence[Row]:
        """
        Devuelve la lista completa de contactos
        :return: list[Contacto]. Lista de contactos
        """
        c = aliased(Contacto, name='c')
        result = db.execute(select(c.id, c.nombre, c.telefonos, c.fecha_nac, c.direccion.label('dir'), Localidad.nombre.label('localidad'))
                            .outerjoin(Localidad)).all()
        return result

    def get_by_id(self, db: Session, id: int) -> Contacto:
        """
        Busca un contacto por id
        :param id: int. El id a buscar
        :return: Contacto. El contacto encontrado.
                 Si no se encuentra, el método buscar_contacto lanzará una excepción NotFoundError
        """
        result = db.get(Contacto, id)
        if result is None:
            raise NotFoundError(f'Contacto [{id}] no encontrado')
        return result

    def agregar(self, db: Session, datos: Contacto) -> Contacto:
        """
        Agrega un nuevo contacto a la lista
        :param data: Contacto. Datos del contacto a agregar. El id se asignará automáticamente
        :return: Contacto. El contacto agregado, con el id asignado
        """
        db.add(datos)
        db.commit()
        return datos

    def editar(self, db: Session, id: int, datos: dict) -> Contacto:
        """
        Reemplaza los valores de un contacto existente por los nuevos valores
        :param id: int. Id del contacto a editar
        :param data: ContactoSinId. Datos nuevos del contacto. El id no se modifica
        :return: Contacto. El contacto actualizado
        """
        cto = self.get_by_id(db, id)
        # actualiza todos los campos del contacto
        datos_dir = datos.pop('direccion', {}) or {}
        dir = Direccion(**datos_dir)
        datos['direccion'] = dir
        for k, v in datos.items():
            setattr(cto, k, v)          # setattr es una función de Python que asigna un valor a un atributo de un objeto, recibe el objeto, el nombre del atributo y el valor a asignar
        db.commit()
        return cto

    def borrar(self, db: Session, id: int) -> None:
        """
        Borra un contacto de la lista
        :param id: int. Id del contacto a borrar
        :return: None. Si el contacto se encuentra en la lista, se elmimina.
          Si no se encuentra, el método buscar_contacto lanzará una excepción HTTP con código 404
        """
        cto = self.get_by_id(db, id)
        db.delete(cto)
        db.commit()

    # endregion

    # region otros metodos
    def get_all_count(self, db: Session) -> int:
        """
        Devuelve la cantidad de contactos en la tabla
        :return: int, cantidad de contactos
        """
        return db.query(Contacto).count()
    # endregion

        