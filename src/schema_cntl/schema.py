
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

def generate_revision_history(id, start = 0, no = 1):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True)
    if start + no > len(schema_doc.strands):
        raise KeyError("Too many strands specified")
    return schema_doc.strands[start:start+no]

def no_of_revisions(id):
    return len(Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True).strands)

def generate_differences(id, strand_start_index, strand_end_index):
    schema_doc = Document(table=settings.TABLE, ledger=settings.LEDGER, id=id, stranded=True)

    if strand_start_index > len(schema_doc.strands) - 1 or \
      strand_end_index > len(schema_doc.strands):
        raise ValueError("Specified indices exceed number of strands")

    strand_start = schema_doc.strands[strand_start_index]
    strand_end = schema_doc.strands[strand_end_index]
    
    print(strand_start.schema.tables[0]['name'])
    print(strand_start.schema.tables[0]['columns'])
    print(strand_end.schema.tables[0]['name'])
    print(strand_end.schema.tables[0]['columns'])
