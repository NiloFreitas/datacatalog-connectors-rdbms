#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.datacatalog_connectors.rdbms.scrape import \
    metadata_scraper
import logging
from pandas import DataFrame


class MetadataScraper(metadata_scraper.MetadataScraper):

    def _create_dataframe(self, query_result):

        rows = list()
        for row in query_result:
            rows.append(row)

        cols = [x.name for x in query_result.fields]

        return DataFrame(rows, columns=cols)

    def _create_rdbms_connection(self, connection_args):
        # import at the method level, because this flow is conditional
        # if the connector reads from a CSV file, this is not used.

        # https://github.com/googleapis/python-spanner
        from google.cloud import spanner

        instance_id = connection_args.get('spanner-instance')
        database_id = connection_args.get('spanner-database')

        # Instantiate a client.
        spanner_client = spanner.Client()
        # Get a Cloud Spanner instance by ID.
        instance = spanner_client.instance(instance_id)
        # Get a Cloud Spanner database by ID.
        database = instance.database(database_id)

        return database

    def _get_base_metadata_from_rdbms_connection(self, connection_args, query):

        try:
            database = self._create_rdbms_connection(connection_args)

            with database.snapshot() as snapshot:
                query_result = snapshot.execute_sql(query)

            dataframe = self._create_dataframe(query_result)

            if dataframe.empty:
                raise Exception('RDBMS is empty, no metadata to extract.')

            return dataframe
        except:  # noqa:E722
            logging.error(
                'Error connecting to the database to extract metadata.')
            raise
