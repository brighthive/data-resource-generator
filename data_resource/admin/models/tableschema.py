from sqlalchemy import Column, Integer
from data_resource.db import admin_base
from sqlalchemy.dialects.postgresql import JSONB
from data_resource.shared_utils.log_factory import LogFactory


logger = LogFactory.get_console_logger("admin:model-tableschema")


class TableSchema(admin_base):
    __tablename__ = "table_schema"
    id = Column(Integer, primary_key=True)
    tableschema = Column(JSONB)
    swagger = Column(JSONB)

    def update(self, id=None, tableschema=None, swagger=None):
        if tableschema is not None:
            self.tableschema = tableschema
        if swagger is not None:
            self.swagger = swagger

    def dump(self):
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}
