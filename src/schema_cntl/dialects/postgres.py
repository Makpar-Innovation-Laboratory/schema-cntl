from enum import Enum
from psycopg2 import sql

class DataTypes(Enum):
  BOOL="bool"
  TEXT="text"
  CHAR="char"
  VARCHAR="varchar"
  DOUBLE="float8"
  INTEGER="int"
  DECIMAL="decimal"
  DATE="date"

  @staticmethod
  def convert(string = None):
      if string is None:
          return None
      for member in DataTypes.__members__.values():
          if string == member.value:
              return member
      return None

  @staticmethod
  def belongs_to_types(string, *enums):
      types = [ member.value for member in DataTypes.__members__.values() if member in enums ]
      try:
          for data_type in types:
              if string == data_type:
                  return True
          return False
      except ValueError:
          return False

class Column:
  
  @staticmethod
  def define(name, data_type, limit=None, foreign_key_references=None, primary_key=False, not_null=False):
      """Create a column definition clause in **PostgreSQL**. Column names will be parameterized to prevent injection, i.e. the `name` passed into this method is not the name of the column, but the name of the column parameter in the clause that is passed into the query cursor.

      :param name: [description]
      :type name: [type]
      :param data_type: [description]
      :type data_type: [type]
      :param limit: [description], defaults to None
      :type limit: [type], optional
      :param foreign_key_references: [description], defaults to None
      :type foreign_key_references: [type], optional
      :param primary_key: [description], defaults to False
      :type primary_key: bool, optional
      :param not_null: [description], defaults to False
      :type not_null: bool, optional
      :return: [description]
      :rtype: [type]
      """
      if primary_key:
          return "{%s} SERIAL PRIMARY KEY"%(name)

      if foreign_key_references is not None:
          return "{%s} integer REFERENCES {%s}"%(name, foreign_key_references)

      col_def = "{%s} %s"%(name, data_type.value)

      if limit is not None and data_type in [DataTypes.CHAR, DataTypes.VARCHAR]:
          col_def += "(%s)"%(limit)

      if not_null:
          col_def += " NOT NULL"

      return col_def

class Table:

  @staticmethod
  def create(table_name, *col_defs):
      """Generate a `CREATE TABLE` PostgreSQL  statement. Table and column names will be parameterized in query to prevent injection, i.e. `table_name` and `col_def[]['name']` are not the names of the table and columns, but the names of the column and column parameters in the statement.

      :param table_name: name of table
      :type table_name: string
      :param kwargs: array of column objects from `schema.tables[]` structure, with `name` replaced by a parameterized key.
      :return: `CREATE TABLE` statement
      :rtype: string
      """
      create_table = "CREATE TABLE {%s} ("%(table_name)
      for col_def in col_defs:
          col_statement = Column.define(
              name = col_def['name'], 
              data_type = DataTypes.convert(col_def.get('type', None)), 
              limit = col_def.get('limit', None), 
              primary_key = col_def.get('primary_key', False),
              foreign_key_references = col_def.get('foreign_key_references', None),
              not_null = col_def.get('not_null', False)
          )

          create_table += col_statement

          if col_defs.index(col_def) != len(col_defs) - 1:
              create_table += ", "

      create_table += ");"
      return create_table


