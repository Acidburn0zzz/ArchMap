#!/usr/bin/env python3
import io
import logging
import os
import pickle
import sys
import unittest
import urllib

import archmap


archmap.log.setLevel(logging.CRITICAL)


class WikiParserTestCase(unittest.TestCase):
    """These tests test the wiki parser in the get_users() function
    """

    # 'ArchMap_List-stripped.html' is a stripped down page of HTML
    # including the tags needed for parsing and some test data
    wiki_html = 'tests/ArchMap_List-stripped.html'

    # 'raw_users.txt' contains the extracted list from 'ArchMap_List-stripped.html'
    # The trailing newline needs to be stripped to match the output from 'get_users'
    with open('tests/raw_users.txt', 'r') as raw_users:
        raw_users = raw_users.read().rstrip('\n')

    def setUp(self):
        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def test_wiki_parser(self):
        output_get_users = archmap.get_users(local=self.wiki_html)
        self.assertEqual(self.raw_users, output_get_users)

    def test_internet(self):
        # Mock out the internet connection using an offline copy
        def mock_urlopen(url):
            with open('tests/ArchMap_List-stripped.html', 'rb') as test_page:
                test_string = io.BytesIO(test_page.read())
            return test_string

        # Reassign the 'urlopen' function to use the mock one
        archmap.urlopen = mock_urlopen

        # Check that the returned string equals the raw text
        self.assertEqual(self.raw_users, archmap.get_users())

        # Restore the original call
        archmap.urlopen = urllib.request.urlopen

    def test_error(self):
        # Fake an error when the function is called
        def mock_error(url):
            raise urllib.error.URLError('Simulated test error')

        # Reassign the 'urlopen' function to use the mock one
        archmap.urlopen = mock_error

        # Check that the function returns 'None' when there is a connection error
        self.assertIsNone(archmap.get_users())

        # Restore the original call
        archmap.urlopen = urllib.request.urlopen


class ListParserTestCase(unittest.TestCase):
    """These tests test that the list parser is working correctly
    """

    # 'raw_users.txt' contains an unformatted 'raw' sample list
    with open('tests/raw_users.txt', 'r') as raw_users_file:
        raw_users = raw_users_file.read()

    # 'sample_users.txt' contains a formatted sample list equivilent to the raw version above
    with open('tests/sample-archmap_users.txt', 'r') as sample_users_file:
        sample_users = sample_users_file.read()

    # 'sample_parsed_users.pickle' is a pickled list that was generated with a known good list
    # ('get_users' was run on 'sample_users.txt' and the output was pickled)
    with open('tests/sample_parsed_users.pickle', 'rb') as pickled_input:
        sample_parsed_users = pickle.load(pickled_input)

    def setUp(self):
        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def test_list_parser_raw(self):
        parsed_raw_users = archmap.parse_users(self.raw_users)
        self.assertEqual(self.sample_parsed_users, parsed_raw_users)

    def test_list_parser_cleaned(self):
        parsed_cleaned_users = archmap.parse_users(self.sample_users)
        self.assertEqual(self.sample_parsed_users, parsed_cleaned_users)


class OutputTestCase(unittest.TestCase):
    """These tests compare the output of ``make_geojson()``, ``make_kml()``  and ``make csv()``
    with pre-generated versions that have been checked manually, these *sample* files were
    generated by running ``archmap.py`` on the stripped-down/handmade ``ArchMap_List-stripped.html'``.
    """

    # 'sample_parsed_users.pickle' is a pickled list that was generated with a known good list
    # ('get_users' was run on 'sample_users.txt' and the output was pickled)
    with open('tests/sample_parsed_users.pickle', 'rb') as pickled_input:
        parsed_users = pickle.load(pickled_input)

    def setUp(self):
        self.sample_users = 'tests/sample-archmap_users.txt'
        self.output_users = 'tests/output-archmap_users.txt'
        self.sample_pretty_users = 'tests/sample-archmap_pretty_users.txt'
        self.output_pretty_users = 'tests/output-archmap_pretty_users.txt'
        self.sample_geojson = 'tests/sample-archmap.geojson'
        self.output_geojson = 'tests/output-archmap.geojson'
        self.sample_kml = 'tests/sample-archmap.kml'
        self.output_kml = 'tests/output-archmap.kml'
        self.sample_csv = 'tests/sample-archmap.csv'
        self.output_csv = 'tests/output-archmap.csv'

        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def tearDown(self):
        try:
            os.remove(self.output_users)
            os.remove(self.output_pretty_users)
            os.remove(self.output_geojson)
            os.remove(self.output_kml)
            os.remove(self.output_csv)
        except FileNotFoundError:
            pass

    def test_users(self):
        archmap.make_users(self.parsed_users, self.output_users)

        with open(self.sample_users, 'r') as file:
            sample_users = file.read()
        with open(self.output_users, 'r') as file:
            output_users = file.read()

        self.assertEqual(sample_users, output_users)

    def test_pretty_users(self):
        archmap.make_users(self.parsed_users, self.output_pretty_users, pretty=True)

        with open(self.sample_pretty_users, 'r') as file:
            sample_pretty_users = file.read()
        with open(self.output_pretty_users, 'r') as file:
            output_pretty_users = file.read()

        self.assertEqual(sample_pretty_users, output_pretty_users)

    def test_geojson(self):
        archmap.make_geojson(self.parsed_users, self.output_geojson)

        with open(self.sample_geojson, 'r') as file:
            sample_geojson = file.read()
        with open(self.output_geojson, 'r') as file:
            output_geojson = file.read()

        self.assertEqual(sample_geojson, output_geojson)

    def test_kml(self):
        archmap.make_kml(self.parsed_users, self.output_kml)

        with open(self.sample_kml, 'r') as file:
            sample_kml = file.read()
        with open(self.output_kml, 'r') as file:
            output_kml = file.read()

        self.assertEqual(sample_kml, output_kml)

    def test_csv(self):
        archmap.make_csv(self.parsed_users, self.output_csv)

        with open(self.sample_csv, 'r') as file:
            sample_csv = file.read()
        with open(self.output_csv, 'r') as file:
            output_csv = file.read()

        self.assertEqual(sample_csv, output_csv)


class ReturnedTestCase(unittest.TestCase):
    """These tests compare the return values of ``make_geojson()``, ``make_kml()``  and ``make csv()``
    with pre-generated versions that have been checked manually, these *sample* files were
    generated by running ``archmap.py`` on the stripped-down/handmade ``ArchMap_List-stripped.html'``.
    """

    # 'sample_parsed_users.pickle' is a pickled list that was generated with a known good list
    # ('get_users' was run on 'sample_users.txt' and the output was pickled)
    with open('tests/sample_parsed_users.pickle', 'rb') as pickled_input:
        parsed_users = pickle.load(pickled_input)

    def setUp(self):
        self.sample_users = 'tests/sample-archmap_users.txt'
        self.sample_pretty_users = 'tests/sample-archmap_pretty_users.txt'
        self.sample_geojson = 'tests/sample-archmap.geojson'
        self.sample_kml = 'tests/sample-archmap.kml'
        self.sample_csv = 'tests/sample-archmap.csv'

        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def test_users(self):
        returned_users = archmap.make_users(self.parsed_users)

        with open(self.sample_users, 'r') as file:
            sample_users = file.read()
        self.assertEqual(sample_users, returned_users)

    def test_pretty_users(self):
        returned_pretty_users = archmap.make_users(self.parsed_users, pretty=True)

        with open(self.sample_pretty_users, 'r') as file:
            sample_pretty_users = file.read()
        self.assertEqual(sample_pretty_users, returned_pretty_users)

    def test_geojson(self):
        returned_geojson = archmap.make_geojson(self.parsed_users)

        with open(self.sample_geojson, 'r') as file:
            sample_geojson = file.read()
        self.assertEqual(sample_geojson, returned_geojson)

    def test_kml(self):
        returned_kml = archmap.make_kml(self.parsed_users)

        with open(self.sample_kml, 'r') as file:
            sample_kml = file.read()
        self.assertEqual(sample_kml, returned_kml)

    def test_csv(self):
        returned_csv = archmap.make_csv(self.parsed_users)

        with open(self.sample_csv, 'r') as file:
            sample_csv = file.read()
        self.assertEqual(sample_csv, returned_csv)


class InteractiveTestCase(unittest.TestCase):
    """These tests test the interactive part of the script - the "main()" function
    """

    def setUp(self):
        self.sample_users = 'tests/sample-archmap_users.txt'
        self.output_users = 'tests/interactive_output-archmap_users.txt'
        self.sample_pretty_users = 'tests/sample-archmap_pretty_users.txt'
        self.output_pretty_users = 'tests/interactive_output-archmap_pretty_users.txt'
        self.sample_geojson = 'tests/sample-archmap.geojson'
        self.output_geojson = 'tests/interactive_output-archmap.geojson'
        self.sample_kml = 'tests/sample-archmap.kml'
        self.output_kml = 'tests/interactive_output-archmap.kml'
        self.sample_csv = 'tests/sample-archmap.csv'
        self.output_csv = 'tests/interactive_output-archmap.csv'

        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

        sys.argv = ['test',
                    '--quiet',
                    '--file', 'tests/ArchMap_List-stripped.html',
                    '--users', self.output_users,
                    '--geojson', self.output_geojson,
                    '--kml', self.output_kml,
                    '--csv', self.output_csv]

        archmap.main()

        # Make a prettyfied user file
        sys.argv = ['test',
                    '--quiet',
                    '--file', 'tests/ArchMap_List-stripped.html',
                    '--pretty',
                    '--users', self.output_pretty_users,
                    '--geojson', 'no',
                    '--kml', 'no',
                    '--csv', 'no']

        archmap.main()

        archmap.log.setLevel(logging.CRITICAL)

    def tearDown(self):
        try:
            os.remove(self.output_users)
            os.remove(self.output_pretty_users)
            os.remove(self.output_geojson)
            os.remove(self.output_kml)
            os.remove(self.output_csv)
        except FileNotFoundError:
            pass

    def test_users(self):
        with open(self.sample_users, 'r') as file:
            sample_users = file.read()
        with open(self.output_users, 'r') as file:
            output_users = file.read()

        self.assertEqual(sample_users, output_users)

    def test_pretty_users(self):
        with open(self.sample_pretty_users, 'r') as file:
            sample_pretty_users = file.read()
        with open(self.output_pretty_users, 'r') as file:
            output_pretty_users = file.read()

        self.assertEqual(sample_pretty_users, output_pretty_users)

    def test_geojson(self):
        with open(self.sample_geojson, 'r') as file:
            sample_geojson = file.read()
        with open(self.output_geojson, 'r') as file:
            output_geojson = file.read()

        self.assertEqual(sample_geojson, output_geojson)

    def test_kml(self):
        with open(self.sample_kml, 'r') as file:
            sample_kml = file.read()
        with open(self.output_kml, 'r') as file:
            output_kml = file.read()

        self.assertEqual(sample_kml, output_kml)

    def test_csv(self):
        with open(self.sample_csv, 'r') as file:
            sample_csv = file.read()
        with open(self.output_csv, 'r') as file:
            output_csv = file.read()

        self.assertEqual(sample_csv, output_csv)


if __name__ == '__main__':
    unittest.main()
