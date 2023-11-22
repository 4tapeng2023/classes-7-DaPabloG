from xml_file_processor import FileProcessor

def display_menu():
    print("XML File Processor Menu:")
    print("1. Read File")
    print("2. Add Record")
    print("3. Delete Record")
    print("4. Update Record")
    print("5. Display Records")
    print("0. Exit")

def get_user_choice():
    try:
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def main():
    processor = FileProcessor()
    filename = "data.xml"  # Replace with the actual filename

    while True:
        display_menu()
        choice = get_user_choice()

        if choice is None:
            continue

        if choice == 0:
            print("Exiting...")
            break
        elif choice == 1:
            processor.display_records(filename)
        elif choice == 2:
            record_id = int(input("Enter record ID: "))
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            city = input("Enter city: ")
            record = {"id": record_id, "name": name, "age": age, "city": city}
            processor.add_record(filename, record)
        elif choice == 3:
            record_id = int(input("Enter record ID to delete: "))
            processor.delete_record(filename, record_id)
        elif choice == 4:
            record_id = int(input("Enter record ID to update: "))
            new_age = int(input("Enter new age: "))
            new_city = input("Enter new city: ")
            new_record = {"age": new_age, "city": new_city}
            processor.update_record(filename, record_id, new_record)
        elif choice == 5:
            processor.display_records(filename)
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
