# google-datacatalog-spanner-connector

Library for ingesting Spanner metadata into Google Cloud Data Catalog.

[![Python package][2]][2] [![License][5]][5] [![Issues][6]][7]

**Disclaimer: This is not an officially supported Google product.**

<!--
  DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Installation](#1-installation)
  * [1.1. Mac/Linux](#11-maclinux)
  * [1.2. Windows](#12-windows)
  * [1.3. Install from source](#13-install-from-source)
    + [1.3.1. Get the code](#131-get-the-code)
    + [1.3.2. Create and activate a *virtualenv*](#132-create-and-activate-a-virtualenv)
    + [1.3.3. Install the library](#133-install-the-library)
- [2. Environment setup](#2-environment-setup)
  * [2.1. Auth credentials](#21-auth-credentials)
    + [2.1.1. Create a service account and grant it below roles](#211-create-a-service-account-and-grant-it-below-roles)
    + [2.1.2. Download a JSON key and save it as](#212-download-a-json-key-and-save-it-as)
  * [2.2. Set environment variables](#22-set-environment-variables)
- [3. Adapt user configurations](#3-adapt-user-configurations)
- [4. Run entry point](#4-run-entry-point)
  * [4.1. Run Python entry point](#41-run-python-entry-point)
  * [4.2. Run the Python entry point with a user-defined entry resource URL prefix](#42-run-the-python-entry-point-with-a-user-defined-entry-resource-url-prefix)
  * [4.3. Run Docker entry point](#43-run-docker-entry-point)
- [5. Scripts inside tools](#5-scripts-inside-tools)
  * [5.1. Run clean up](#51-run-clean-up)
  * [5.2. Extract CSV](#52-extract-csv)
- [6. Developer environment](#6-developer-environment)
  * [6.1. Install and run Yapf formatter](#61-install-and-run-yapf-formatter)
  * [6.2. Install and run Flake8 linter](#62-install-and-run-flake8-linter)
  * [6.3. Run Tests](#63-run-tests)
- [7. Metrics](#7-metrics)
- [8. Troubleshooting](#8-troubleshooting)

<!-- tocstop -->

-----

## 1. Installation

Install this library in a [virtualenv][1] using pip. [virtualenv][1] is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With [virtualenv][1], it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies. Make sure you use Python 3.8+.

**WARNING: Spanner connector currently not published in PyPi, so skip steps 1.1 and 1.2, and go to step 1.3.**

### 1.1. Mac/Linux

```bash
pip3 install virtualenv
virtualenv --python python3.8 <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip3 install google-datacatalog-spanner-connector
```

### 1.2. Windows

```bash
pip3 install virtualenv
virtualenv --python python3.8 <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip3.exe install google-datacatalog-spanner-connector
```

### 1.3. Install from source

#### 1.3.1. Get the code

````bash
git clone https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/
cd datacatalog-connectors-rdbms/google-datacatalog-spanner-connector
````

#### 1.3.2. Create and activate a *virtualenv*

```bash
pip3 install virtualenv
virtualenv --python python3.8 <your-env>
source <your-env>/bin/activate
```

#### 1.3.3. Install the library

```bash
pip3 install .
```

## 2. Environment setup

### 2.1. Auth credentials

#### 2.1.1. Create a service account and grant it below roles

- Data Catalog Admin

#### 2.1.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/spanner2dc-credentials.json`

> Please notice this folder and file will be required in next steps.

### 2.2. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export SPANNER2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export SPANNER2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export SPANNER2DC_INSTANCE=spanner_instance
export SPANNER2DC_DATABASE=spanner_database
export SPANNER2DC_RAW_METADATA_CSV=spanner_raw_csv (If supplied ignores the SPANNER server credentials)
```

## 3. Adapt user configurations

Along with default metadata, the connector can ingest optional metadata as well, such as number of
rows in each table. The table below shows what metadata is scraped by default, and what is configurable.

SPANNER DIALECT  
| Metadata                     | Description                                 | Scraped by default | Config option                |                    
| ---                          | ---                                         | ---                | ---                          |                       
| schema_name                  | Name of a schema                            | Y                  | ---                          | 
| table_name                   | Name of a table                             | Y                  | ---                          | 
| table_type                   | Type of a table (BASE, VIEW, etc)           | Y                  | ---                          | 
| column_name                  | Name of a column                            | Y                  | ---                          | 
| column_type                  | Type of a column (ARRAY, USER-DEFINED, etc) | Y                  | ---                          | 
| column_default_value         | Default value of a column                   | Y                  | ---                          | 
| column_nullable              | Whether a column is nullable                | Y                  | ---                          | 

SPANNER POSTGRESQL DIALECT  
| Metadata                     | Description                                 | Scraped by default | Config option                |                    
| ---                          | ---                                         | ---                | ---                          |                       
| schema_name                  | Name of a schema                            | Y                  | ---                          |
| table_name                   | Name of a table                             | Y                  | ---                          |
| table_type                   | Type of a table (BASE, VIEW, etc)           | Y                  | ---                          |
| column_name                  | Name of a column                            | Y                  | ---                          |
| column_type                  | Type of a column (ARRAY, USER-DEFINED, etc) | Y                  | ---                          |
| column_default_value         | Default value of a column                   | Y                  | ---                          |
| column_nullable              | Whether a column is nullable                | Y                  | ---                          |
| column_char_length           | Char length of values in a column           | Y                  | ---                          |
| column_numeric_precision     | Numeric precision of values in a column     | Y                  | ---                          |

## 4. Run entry point

### 4.1. Run Python entry point

- Virtualenv

```bash
google-datacatalog-spanner-connector \
--datacatalog-project-id=$SPANNER2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$SPANNER2DC_DATACATALOG_LOCATION_ID \
--spanner-instance=$SPANNER2DC_INSTANCE \
--spanner-database=$SPANNER2DC_DATABASE \
--datacatalog-entry-group-id="spanner_${SPANNER2DC_INSTANCE}_${SPANNER2DC_DATABASE}" \
--raw-metadata-csv=$SPANNER2DC_RAW_METADATA_CSV
```

### 4.2. Run the Python entry point with a user-defined entry resource URL prefix

This option is useful when the connector cannot accurately determine the database hostname.
For example when running under proxies, load balancers or database read replicas,
you can specify the prefix of your master instance so the resource URL will point
to the exact database where the data is stored.

- Virtualenv

```bash
google-datacatalog-spanner-connector \
--datacatalog-project-id=$SPANNER2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$SPANNER2DC_DATACATALOG_LOCATION_ID \
--datacatalog-entry-resource-url-prefix project/database-instance \
--spanner-instance=$SPANNER2DC_INSTANCE \
--spanner-database=$SPANNER2DC_DATABASE \
--datacatalog-entry-group-id="spanner_${SPANNER2DC_INSTANCE}_${SPANNER2DC_DATABASE}" \
--raw-metadata-csv=$SPANNER2DC_RAW_METADATA_CSV
```

### 4.3. Run Docker entry point

```bash
docker build -t spanner2datacatalog .
docker run --rm --tty -v YOUR-CREDENTIALS_FILES_FOLDER:/data spanner2datacatalog \
--datacatalog-project-id=$SPANNER2DC_DATACATALOG_PROJECT_ID \
--datacatalog-location-id=$SPANNER2DC_DATACATALOG_LOCATION_ID \
--spanner-instance=$SPANNER2DC_INSTANCE \
--spanner-database=$SPANNER2DC_DATABASE \
--datacatalog-entry-group-id="spanner_${SPANNER2DC_INSTANCE}_${SPANNER2DC_DATABASE}" \
--raw-metadata-csv=$SPANNER2DC_RAW_METADATA_CSV
```

## 5. Scripts inside tools

### 5.1. Run clean up

```bash
# List of projects split by comma. Can be a single value without comma
export SPANNER2DC_DATACATALOG_PROJECT_IDS=my-project-1,my-project-2
```

```bash
# Run the clean up
python tools/cleanup_datacatalog.py --datacatalog-project-ids=$SPANNER2DC_DATACATALOG_PROJECT_IDS 
# If using "--datacatalog-entry-group-id=..." change the cleanup_datacatalog.py file to match  
# By default, it cleans up only "spanner"  
```

### 5.2. Extract CSV

```bash
# Spanner SQL dialect
gcloud spanner databases execute-sql $SPANNER2DC_DATABASE --instance=$SPANNER2DC_INSTANCE --flatten "rows" --format="csv(rows[0]:label=schema_name,rows[1]:label=table_name,rows[2]:label=table_type,rows[3]:label=column_name,rows[4]:label=column_default_value,rows[5]:label=column_nullable,rows[6]:label=column_type)" --sql="SELECT 'default' as schema_name,
       t.table_name, t.table_type,
       c.column_name,
       c.column_default as column_default_value,
       c.is_nullable as column_nullable,
       c.spanner_type as column_type
FROM information_schema.tables t
         JOIN  information_schema.columns c
               on c.table_name = t.table_name and c.table_schema = t.table_schema
WHERE t.table_catalog = '' AND t.table_schema = ''
ORDER BY t.table_name, c.column_name;" > resource/spanner_full_dump.csv 
```

## 6. Developer environment

### 6.1. Install and run Yapf formatter

```bash
pip3 install --upgrade yapf

# Auto update files
yapf --in-place --recursive src tests

# Show diff
yapf --diff --recursive src tests

# Set up pre-commit hook
# From the root of your git project.
curl -o pre-commit.sh https://raw.githubusercontent.com/google/yapf/master/plugins/pre-commit.sh
chmod a+x pre-commit.sh
mv pre-commit.sh .git/hooks/pre-commit
```

### 6.2. Install and run Flake8 linter

```bash
pip3 install --upgrade flake8
flake8 src tests
```

### 6.3. Run Tests

```bash
python3 setup.py test
```

## 7. Metrics

[Metrics README.md](docs/README.md)

## 8. Troubleshooting

In the case a connector execution hits Data Catalog quota limit, an error will be raised and logged with the following detailement, depending on the performed operation READ/WRITE/SEARCH: 
```
status = StatusCode.RESOURCE_EXHAUSTED
details = "Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'."
debug_error_string = 
"{"created":"@1587396969.506556000", "description":"Error received from peer ipv4:172.217.29.42:443","file":"src/core/lib/surface/call.cc","file_line":1056,"grpc_message":"Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute' of service 'datacatalog.googleapis.com' for consumer 'project_number:1111111111111'.","grpc_status":8}"
```
For more info about Data Catalog quota, go to: [Data Catalog quota docs](https://cloud.google.com/data-catalog/docs/resources/quotas).

[1]: https://virtualenv.pypa.io/en/latest/
[2]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/workflows/Python%20package/badge.svg?branch=master
[5]: https://img.shields.io/github/license/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[6]: https://img.shields.io/github/issues/GoogleCloudPlatform/datacatalog-connectors-rdbms.svg
[7]: https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/issues