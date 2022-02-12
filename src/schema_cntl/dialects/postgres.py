from enum import Enum
from psycopg2 import sql

class DataTypes(Enum):
  BOOL="bool"
  VARCHAR="varchar"
  DOUBLE="float8"
  INTEGER="int"
  DECIMAL="decimal"
  DATE="date"

class Column:
  
  @staticmethod
  def column_definition(name, data_type, limit=None, foreign_key_references=None, primary_key=False, not_null=False):
    if primary_key:
        return "{%s} SERIAL PRIMARY KEY"%(name)

    if foreign_key_references is not None:
        return "{%s} integer REFERENCES {%s}"%(name, foreign_key_references)

    col_def = "{%s} %s"%(name, data_type.value)

    if limit is not None:
        col_def += "(%s)"%(limit)

    if not_null:
        col_def += " NOT NULL"

    return col_def

