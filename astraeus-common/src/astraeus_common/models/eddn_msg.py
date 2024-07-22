import json
from datetime import datetime
from typing import Optional, Dict
from uuid import UUID


class EDDNMsg:
    _id: Optional[UUID]
    _schema: Optional[str]
    _header: Optional[Dict]
    _message: Optional[Dict]
    _recv_date: Optional[datetime]
    _sync_date: Optional[datetime]

    EDDN_MESSAGE_SELECT_BY_ID = '''
    select id, "schema", header, message, recv_date, sync_date
    from eddn_message
    where id = %(id)s
    '''

    EDDN_MESSAGE_SELECT_UNREAD = '''
    select id, "schema", header, message, recv_date, sync_date
    from eddn_message
    where sync_date is null
    '''

    EDDN_MESSAGE_INSERT = '''
    insert into eddn_message
    ("schema", header, message, recv_date, sync_date)
    values (%(schema)s,
            %(header)s,
            %(message)s,
            %(recv_date)s,
            %(sync_date)s);
    '''

    EDDN_MESSAGE_UPDATE_BY_ID = '''
    update eddn_message
    set "schema" = %(schema)s,
        header = %(header)s,
        message = %(message)s,
        recv_date = %(recv_date)s,
        sync_date = %(sync_date)s
    where id = %(id)s
    '''

    EDDN_MESSAGE_DELETE_BY_ID = '''
    delete from eddn_message
    where id = %(id)s
    '''

    @property
    def id(self) -> Optional[UUID]:
        return self._id

    @id.setter
    def id(self, value: UUID):
        self._id = value

    @property
    def schema(self) -> Optional[str]:
        return self._schema

    @schema.setter
    def schema(self, value: str):
        self._schema = value

    @property
    def header(self) -> Optional[Dict]:
        return self._header

    @header.setter
    def header(self, value: dict):
        self._header = value

    @property
    def message(self) -> Optional[Dict]:
        return self._message

    @message.setter
    def message(self, value: dict):
        self._message = value

    @property
    def recv_date(self) -> Optional[datetime]:
        return self._recv_date

    @recv_date.setter
    def recv_date(self, value: datetime):
        self._recv_date = value

    @property
    def sync_date(self) -> Optional[datetime]:
        return self._sync_date

    @sync_date.setter
    def sync_date(self, value: datetime):
        self._sync_date = value

    def __init__(self, dict_from_db: Optional[Dict] = None,
                 uuid: Optional[UUID] = None,
                 schema: Optional[str] = None,
                 header: Optional[Dict] = None,
                 message: Optional[Dict] = None,
                 recv_date: Optional[datetime] = None,
                 sync_date: Optional[datetime] = None):
        if dict_from_db is not None:
            uuid = dict_from_db.get('id', None)
            schema = dict_from_db.get('schema', None)
            header = dict_from_db.get('header', None)
            message = dict_from_db.get('message', None)
            recv_date = dict_from_db.get('recv_date', None)
            sync_date = dict_from_db.get('sync_date', None)
        self._id = uuid
        self._schema = schema
        self._header = header
        self._message = message
        self._recv_date = recv_date
        self._sync_date = sync_date

    def to_dict(self):
        return {
            'id': self._id,
            'schema': self._schema,
            'header': self._header,
            'message': self._message,
            'recv_date': self._recv_date,
            'sync_date': self._sync_date,
        }

    def to_dict_for_db(self):
        return {
            'id': self._id,
            'schema': self._schema,
            'header': json.dumps(self._header),
            'message': json.dumps(self._message),
            'recv_date': self._recv_date,
            'sync_date': self._sync_date,
        }


def msg_from_eddn(eddn_recv: dict) -> EDDNMsg:
    schema = eddn_recv.get('name', None)
    header = eddn_recv.get('type', None)
    message = eddn_recv.get('subType', None)
    return EDDNMsg(schema=schema,
                   header=header,
                   message=message,
                   )
