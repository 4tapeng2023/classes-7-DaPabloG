import xml.etree.ElementTree as ET

class FileProcessor:
    def read_file(self, filename):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return None

    def add_record(self, filename, record):
        root = self.read_file(filename)
        if root is not None:
            record_element = ET.Element("record")
            for key, value in record.items():
                field = ET.Element(key)
                field.text = str(value)
                record_element.append(field)
            root.append(record_element)
            self._write_to_file(filename, root)
            print("Record added successfully.")

    def delete_record(self, filename, record_id):
        root = self.read_file(filename)
        if root is not None:
            record_to_delete = next((record for record in root.findall("record") if record.find("id").text == str(record_id)), None)
            if record_to_delete is not None:
                root.remove(record_to_delete)
                self._write_to_file(filename, root)
                print("Record deleted successfully.")
            else:
                print(f"Record with ID {record_id} not found.")

    def update_record(self, filename, record_id, new_record):
        root = self.read_file(filename)
        if root is not None:
            record_to_update = next((record for record in root.findall("record") if record.find("id").text == str(record_id)), None)
            if record_to_update is not None:
                for key, value in new_record.items():
                    field = record_to_update.find(key)
                    if field is not None:
                        field.text = str(value)
                    else:
                        new_field = ET.Element(key)
                        new_field.text = str(value)
                        record_to_update.append(new_field)
                self._write_to_file(filename, root)
                print("Record updated successfully.")
            else:
                print(f"Record with ID {record_id} not found.")

    def display_records(self, filename):
        root = self.read_file(filename)
        if root is not None:
            for record in root.findall("record"):
                print("Record:")
                for field in record:
                    print(f"  {field.tag}: {field.text}")
                print("------------------------")

    def _write_to_file(self, filename, root):
        try:
            tree = ET.ElementTree(root)
            tree.write(filename)
        except ET.ParseError as e:
            print(f"Error writing to XML file: {e}")
            print(f"Invalid XML content: {ET.tostring(root)}")
