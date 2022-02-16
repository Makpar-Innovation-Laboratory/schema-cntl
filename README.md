# schema_cntl

A **Python** library created by [Makpar Innovation Lab](https://innolab-coverage.makpar-innovation.net) for versioning database schemas. Currently compatible with **PostgreSQL**.  **schema_cntl** uses **AWS QLDB** to maintain a revision history of a *schema.json*. This file defines the schema at a single point in time. As *schema.json* changes are committed, the revision history expands. This library generates **SQL** statements that allow the user to transform the schema from one revision to another.

## Setup

### PyPi Package

This is a command line utility. To use it, you must install the latest distribution from **PyPi**,

`pip install schema_cntl`

### QLDB

This library uses [innoldb](https://github.com/Makpar-Innovation-Laboratory/innoldb), another package supported by the *Makpar Innovation Lab*, to persist the *schema.json* to an **AWS Quantum Ledger Database**. As such, in order to use this package, you will need to create a **QLDB** ledger and an **IAM** account with permissions to access that ledger. For more detailed instructions on setting the necesssary resources on **AWS**, [refer to the innoldb documentation](https://makpar-innovation-laboratory.github.io/innoldb/SETUP.html#cloudformation) 

### Environment Variables

You will need to point the **LEDGER** environment variable to the name of the **QLDB** ledger and the **TABLE** environment variable to the name of the table you intend to use. The ledger must exist, but if the table does not exist, **schema_cntl** will create a new one. 

```shell
export LEDGER="<ledger-name>"
export TABLE="<table>"
```

## Schema JSON

A database schema is specified through a JSON configuration file formatted as follows,

```json
{
  "schema": {
      "name": "<schema-name>",
      "engine": "<postgres | ... >",
      "tables": [
          {
              "name": "<table-name>",
              "columns": [
                  {
                    "name": "<name>",
                    "type": "<bool | varchar | float8 | int | decimal | date> : ignored if primary key == true",
                    "limit": "<limit> : optional, defaults to None",
                    "primary_key": "<true | false> : optional, defaults to false",
                    "foreign_key_references" : "<fk> : optional, defaults to None",
                    "not_null": "<true | false> : optional, defaults to false"
                  }
              ]
          }
      ]
    }
}
```

For example, the following schema creates a table named `test_table` with three fields: a primary key field `unique_id`, an integer field `sample_int` and a text field `sample_text`.

```json
{
    "schema": {
        "engine": "postgres",
        "name": "test_schema",
        "tables": [
            {
                "name": "test_table",
                "columns": [
                    {
                        "name": "unique_id",
                        "primary_key": true
                    },
                    {
                        "name": "sample_int",
                        "type": "int"
                    },
                    {
                        "name": "sample_text",
                        "type": "text"
                    }
                ]
            }
        ]
    }
}
```

## Workflow

1. Commit Revision
2. List Revision History
3. Generate Schema
4. Generate Differences

### Commit

```shell
schema_cntl commit <path-to-schema.json>
```

### List Revision History

```shell
schema_cntl history <path-to-schema.json> --limit <revision_limit>
```

### Generate Schema

```shell
schema_cntl schema <path-to-schema.json> <revision>
```

### Generate Differences

```
schema_cntl diff <path-to-schema.json> <start_revision> <end_revision>
```

## Code Quality

[![DeepSource](https://deepsource.io/gh/Makpar-Innovation-Laboratory/schema-cntl.svg/?label=active+issues&show_trend=true&token=UtG51CSVJLsKa8DoELNp2K8W)](https://deepsource.io/gh/Makpar-Innovation-Laboratory/schema-cntl/?ref=repository-badge)
[![DeepSource](https://deepsource.io/gh/Makpar-Innovation-Laboratory/schema-cntl.svg/?label=resolved+issues&show_trend=true&token=UtG51CSVJLsKa8DoELNp2K8W)](https://deepsource.io/gh/Makpar-Innovation-Laboratory/schema-cntl/?ref=repository-badge)