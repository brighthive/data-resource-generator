from sqlalchemy import MetaData, Column, Integer, String
from data_resource.db import admin_base
from sqlalchemy.dialects.postgresql import JSONB


class TableSchema(admin_base):
    __tablename__ = "table_schema"
    id = Column(Integer, primary_key=True)
    data = Column(JSONB)

    def update(self, id=None, data=None):
        if data is not None:
            self.data = data

    def dump(self):
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}
