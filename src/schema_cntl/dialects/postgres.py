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
    def define(**col_def):
        """Create a column definition clause in **PostgreSQL**. Column names will be parameterized to prevent injection, i.e. the `name` passed into this method is not the name of the column, but the name of the column parameter in the clause that is passed into the query cursor.

        :param kwargs: Keyword arguments. The input format should make the `schema.json` input format.
        :return: Column definition clause for `CREATE TABLE` **PostgreSQL** statement.
        :rtype: str
        """
        # data type is not parameterized in string, so it is converted into an enum before formatting
        # so user input can never directly touched the query string
        enumerated_type = DataTypes.convert(col_def['type'])
        if enumerated_type is None:
            raise ValueError("No data type specified for column %s".format(col_def['name']))

        if col_def.get('primary_key', None) is not None:
            return "{%s} SERIAL PRIMARY KEY".format(col_def['name'])

        if col_def.get('foreign_key_references', None) is not None:
            return "{%s} integer REFERENCES {%s}".format(col_def['name'], col_def['foreign_key_references'])

        col_def = "{%s} %s".format(col_def['name'], enumerated_type.value)


        if col_def.get('not_null', None) is not None:
            col_def += " NOT NULL"

        return col_def
      
    @staticmethod
    def add(**col_def):
        """`ADD COLUMN` subclause in **PostgreSQL**, for use in `ALTER TABLE` clauses. Column names will be parameterized to prevent injection, i.e. the `name` passed into this method is not the name of the column, but the name of the column parameter in the clause that is passed into the query cursor.

        :param kwargs: Keyword arguments. The input format should make the `schema.json` input format.
        :return: Column definition clause for `ADD COLUMN` **PostgreSQL** statement.
        :rtype: str
        """
        # data type is not parameterized in string, so it is converted into an enum before formatting
        # so user input can never directly touched the query string
        enumerated_type = DataTypes.convert(col_def['type'])
        if enumerated_type is None:
            raise ValueError("No data type specified for column %s".format(col_def['name']))

        add_column = "ADD COLUMN {%s} %s".format(col_def['name'], enumerated_type.value)

        if col_def.get('not_null', None):
            add_column += " NOT NULL"

        if col_def.get('foreign_key_references', None) is not None:
            fkr = col_def['foreign_key_references']
            add_column += "CONSTRAINT fk_%s_%s REFERENCES {%s}".format(col_def['name'], fkr, fkr)

        return add_column

    @staticmethod
    def drop(name):
        return "DROP COLUMN {%s}"%name
  

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
          col_statement = Column.define(**col_def)

          create_table += col_statement

          if col_defs.index(col_def) != len(col_defs) - 1:
              create_table += ", "

      create_table += ");"
      return create_table


