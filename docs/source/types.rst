datatypes
=========

Currently this library uses `tableschema-sql-py` to convert tableschema types to database types.

The following was written for v1.2.0 of `tableschema-sql-py`.

Follow this link to see the code that does that -- https://github.com/frictionlessdata/tableschema-sql-py/blob/0a4b600561c28b15661bea59254bd6c38f1b8787/tableschema_sql/mapper.py#L143-L168

```
'any': sa.Text,
'array': JSONB,
'boolean': sa.Boolean,
'date': sa.Date,
'datetime': sa.DateTime,
'duration': None,
'geojson': JSONB,
'geopoint': None,
'integer': sa.Integer,
'number': sa.Numeric,
'object': JSONB,
'string': sa.Text,
'time': sa.Time,
'year': sa.Integer,
'yearmonth': None,
```

Any of the items notated as None should be stored as String.

Known bug
---------
date and datetimes have a resolution bug. The application seems to assume you have a resolution of 1 milisecond so any times you send will have zeros appended to it.
