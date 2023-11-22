# test_xml_file_processor.py
import unittest
from unittest import mock
from xml.etree.ElementTree import Element, ElementTree
import io
import sys
import os
from xml_file_processor import FileProcessor

class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = FileProcessor()
        self.test_filename = "test_data.xml"
        self.initial_records = [
            {"id": 1, "name": "Alice", "age": 25, "city": "Wonderland"},
            {"id": 2, "name": "Bob", "age": 30, "city": "Cityville"},
            {"id": 3, "name": "Charlie", "age": 35, "city": "Charlottetown"}
        ]
        self._create_test_file(self.test_filename, self.initial_records)

    def tearDown(self):
        self._delete_test_file(self.test_filename)

    def _create_test_file(self, filename, records):
        root = self._create_test_root(records)
        tree = ElementTree(root)
        tree.write(filename)

    def _create_test_root(self, records):
        root = Element("data")
        for record in records:
            record_element = Element("record")
            for key, value in record.items():
                field = Element(key)
                field.text = str(value)
                record_element.append(field)
            root.append(record_element)
        return root

    def _delete_test_file(self, filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_read_file(self, mock_open_file):
        mock_open_file.side_effect = [
            mock.mock_open(read_data='<data><record><id>1</id><name>Alice</name><age>25</age><city>Wonderland</city></record></data>').return_value,
            mock.mock_open(read_data='').return_value
        ]

        root = self.processor.read_file(self.test_filename)
        self.assertIsNotNone(root)
        self.assertEqual(len(root.findall("record")), 1)

        empty_filename = "empty.xml"
        root_empty = self.processor.read_file(empty_filename)
        self.assertIsNone(root_empty)

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("xml.etree.ElementTree.parse")
    def test_write_to_file(self, mock_parse, mock_open_file):
        mock_open_file.side_effect = [
            mock.mock_open().return_value,
            mock.mock_open().return_value
        ]

        mock_parse.return_value = ElementTree(Element("data"))

        root = self._create_test_root(self.initial_records)
        self.processor._write_to_file(self.test_filename, root)

        mock_open_file.assert_called_with(
            self.test_filename, "w", encoding='us-ascii', errors='xmlcharrefreplace')

        handle = mock_open_file.return_value.__enter__.return_value

        written_content = ''.join([call[1][0] for call in handle.write.mock_calls])

        expected_content = ''

        self.assertEqual(expected_content, written_content)

    def test_add_record(self):
        new_record_data = {"id": 4, "name": "David", "age": 40, "city": "Downtown"}
        self.processor.add_record(self.test_filename, new_record_data)

        root = self.processor.read_file(self.test_filename)
        self.assertIsNotNone(root)
        records = root.findall("record")
        self.assertEqual(len(records), len(self.initial_records) + 1)
        added_record = records[-1]
        self.assertEqual(added_record.find("id").text, str(new_record_data["id"]))
        self.assertEqual(added_record.find("name").text, new_record_data["name"])
        self.assertEqual(added_record.find("age").text, str(new_record_data["age"]))
        self.assertEqual(added_record.find("city").text, new_record_data["city"])

    def test_delete_record(self):
        record_id_to_delete = 2
        self.processor.delete_record(self.test_filename, record_id_to_delete)

        root = self.processor.read_file(self.test_filename)
        self.assertIsNotNone(root)
        records = root.findall("record")
        self.assertEqual(len(records), len(self.initial_records) - 1)
        self.assertNotIn(record_id_to_delete, [int(record.find("id").text) for record in records])

        non_existing_record_id = 99
        self.processor.delete_record(self.test_filename, non_existing_record_id)
        root_after_delete = self.processor.read_file(self.test_filename)
        self.assertEqual(len(root_after_delete.findall("record")), len(records))

    def test_update_record(self):
        record_id_to_update = 1
        updated_data = {"age": 26, "city": "New Wonderland"}
        self.processor.update_record(self.test_filename, record_id_to_update, updated_data)

        root = self.processor.read_file(self.test_filename)
        self.assertIsNotNone(root)
        updated_record = next(
            (record for record in root.findall("record") if record.find("id").text == str(record_id_to_update)),
            None
        )
        self.assertIsNotNone(updated_record)
        self.assertEqual(updated_record.find("age").text, str(updated_data["age"]))
        self.assertEqual(updated_record.find("city").text, updated_data["city"])

        non_existing_record_id = 99
        self.processor.update_record(self.test_filename, non_existing_record_id, updated_data)
        root_after_update = self.processor.read_file(self.test_filename)
        self.assertEqual(len(root_after_update.findall("record")), len(self.initial_records))

    def test_display_records(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.processor.display_records(self.test_filename)
        expected_output = (
            "Record:\n  id: 1\n  name: Alice\n  age: 25\n  city: Wonderland\n------------------------\n"
            "Record:\n  id: 2\n  name: Bob\n  age: 30\n  city: Cityville\n------------------------\n"
            "Record:\n  id: 3\n  name: Charlie\n  age: 35\n  city: Charlottetown\n------------------------\n"
        )
        self.assertEqual(captured_output.getvalue(), expected_output)

        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
