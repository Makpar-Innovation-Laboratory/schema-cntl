
# 1. get first_revision
#     a. create table statement
#
# 1. get revisions
#     previous_revision = first_revision
#
#     for revision in revisions:
#       
#       a. find keys in revision not in previous_revision
#           i. alter table statement for keys
#
#       b. find keys with values different from prevision
#           i. alter column statements for key, values
#
#       c. previous_revision = revision

from innoldb.qldb import Document

from schema_cntl import settings

def commit_schema(schema):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, snapshot=schema)
    schema_doc.save()
    return schema_doc

def generate_revision_history(id, start = 0, end = 1):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True)
    
    if start is not None and end is not None:
        return schema_doc.strands[start:end]
    elif start is not None and end is None:
        return schema_doc.strands[start:]
    elif start is None and end is not None:
        return schema_doc.strands[:end]
    return schema_doc.strands