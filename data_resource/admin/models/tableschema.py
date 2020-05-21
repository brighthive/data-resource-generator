from sqlalchemy import MetaData, Column, Integer, String
from data_resource.db import admin_base
from sqlalchemy.dialects.postgresql import JSONB
import json
import logging


logging.basicConfig(level=logging.INFO)


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
