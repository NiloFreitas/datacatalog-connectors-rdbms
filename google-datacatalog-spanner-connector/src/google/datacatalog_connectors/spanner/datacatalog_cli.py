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

import argparse
import os
import sys

from .scrape import metadata_scraper

from google.datacatalog_connectors.rdbms import \
    datacatalog_cli


class Spanner2DatacatalogCli(datacatalog_cli.DatacatalogCli):

    metadata_query_file = "metadata_query.sql"

    def _get_metadata_scraper(self):
        return metadata_scraper.MetadataScraper

    def _get_host_arg(self, args):
        return args.spanner_instance

    def _get_connection_args(self, args):
        return {
            'spanner-database': args.spanner_database,
            'spanner-instance': args.spanner_instance
        }

    def _get_entry_group_id(self, args):
        return args.datacatalog_entry_group_id or 'spanner'

    def _get_metadata_definition_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'config/metadata_definition.json')

    def _get_query_path(self, args):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'config/' + self.metadata_query_file)

    def _parse_args(self, argv):
        parser = argparse.ArgumentParser(
            description='Command line to sync spanner '
            'metadata to Datacatalog')

        parser.add_argument('--datacatalog-project-id',
                            help='Your Google Cloud project ID',
                            required=True)
        parser.add_argument(
            '--datacatalog-location-id',
            help='Location ID to be used for your Google Cloud Datacatalog',
            required=True)
        parser.add_argument('--datacatalog-entry-group-id',
                            help='Entry group ID to be used for your Google '
                            'Cloud Datacatalog')
        parser.add_argument(
            '--raw-metadata-csv',
            help='Your raw metadata as a csv file, '
            'can be either a local os GCS '
            'path (If supplied ignores the spanner server credentials)')
        parser.add_argument('--datacatalog-entry-resource-url-prefix',
                            help='Entry resource URL prefix '
                            'used in the ingested Data Catalog Entries')
        parser.add_argument('--spanner-instance',
                            help='Your spanner server instance',
                            required=True)
        parser.add_argument('--spanner-database',
                            help='Your spanner database name',
                            required=True)
        parser.add_argument('--service-account-path',
                            help='Local Service Account path '
                            '(Can be suplied as '
                            'GOOGLE_APPLICATION_CREDENTIALS env '
                            'var)')
        parser.add_argument('--enable-monitoring',
                            help='Enables monitoring metrics on the connector')
        parser.add_argument('--is-postgresql-dialect-database',
                            type=bool,
                            default=False,
                            help='If true, the Spanner database is a'
                            'PostgreSQL dialect Spanner database')

        arguments = parser.parse_args(argv)

        if arguments.is_postgresql_dialect_database:
            self.metadata_query_file = "metadata_query_postgresql_dialect.sql"

        return arguments


def main():
    argv = sys.argv
    Spanner2DatacatalogCli().run(argv[1:] if len(argv) > 0 else argv)
