datatypes
=========

Currently this library uses `tableschema-sql-py` to convert table schema types to database types.

The following was written for v1.2.0 of `tableschema-sql-py`.

Follow this link to see the code that does that -- https://github.com/frictionlessdata/tableschema-sql-py/blob/0a4b600561c28b15661bea59254bd6c38f1b8787/tableschema_sql/mapper.py#L143-L168

(sa refers to sqlalchemy types)

- 'any': sa.Text
- 'array': JSONB
- 'boolean': sa.Boolean
- 'date': sa.Date
- 'datetime': sa.DateTime
- 'duration': sa.Text
- 'geojson': JSONB
- 'geopoint': sa.Text
- 'integer': sa.Integer
- 'number': sa.Numeric
- 'object': JSONB
- 'string': sa.Text
- 'time': sa.Time
- 'year': sa.Integer
- 'yearmonth': sa.Text

Known bug
---------

`date` and `datetimes` have a resolution bug. The application seems to assume you have a resolution of 1 millisecond so any times you send will have zeros appended to it.
