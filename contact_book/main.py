import os
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List

# Set a few global vars
column_headers = ['Name', 'Email', 'Phone']
contacts_database_location = 'contacts.csv'
separator = '\n--------------------------------\n'

def load_contacts_db() -> pd.DataFrame:
        """Load the csv into a DataFrame

        Returns:
            pd.DataFrame: _description_
        """
        return pd.read_csv(contacts_database_location)
        
def write_contacts_db(df: pd.DataFrame, mode_flag: str, header_flag: str):
        """Write the DataFrame to a csv

        Args:
            df (pd.DataFrame): _description_
            mode_flag (str): _description_
            header_flag (str): _description_
        """
        df.to_csv(contacts_database_location, mode=mode_flag, header=header_flag, index=False)
        
def check_db_exists() -> None:
        """Validate the existence of the csv db
        """
        # Does the db file exist? Carry on
        if os.path.exists(contacts_database_location):
                pass
        else:
                # Set an empty index value to avoid an empty column at the start of a brand new dataframe
                # Create the csv with the correct headers
                df = pd.DataFrame(columns=column_headers, index=[])
                df.to_csv(contacts_database_location, header=True, index=False)

def display_menu() -> None:
        """Print the main program menu
        """
        menu = '''
        1. Add a contact
        2. Search for a contacts
        3. Update a contact
        4. Delete a contact
        5. Display all contacts
        6. Exit
        '''
        print(menu)
        
def add_contact() -> None:
        """Add a brand new contact and save to the db
        """
        name: str = input('Enter contact name: ')
        email: str = input('Enter contact email: ')
        phone: str = input('Enter contact phone number: ')
        contact: dict = {'Name': name, 'Email': email, 'Phone': phone}
        df: pd.DataFrame = pd.DataFrame(contact, index=['0'])
        write_contacts_db(df, 'a', False)
        print('Contact added!')
        
def search_contacts(df: pd.DataFrame, search_string: str) -> List:
        """Search the DataFrame and return results

        Args:
            df (pd.DataFrame): _description_
            search_string (str): _description_

        Returns:
            List: _description_
        """
        filtered_rows: List = []
        # Search every column in the dataframe for the string and return all rows that contain it
        for column in df:
                filtered_rows.extend(df[df[column].astype(str).str.contains(search_string)].index)
        # Since the text could be in more than one row filter the list so there can't be more than 
        # a single occurrence of a row
        return list(set(filtered_rows))

def update_contact() -> None:
        """Update an existing contacts fields
        """
        df: pd.DataFrame = pd.read_csv(contacts_database_location)
        entry: int = int(input('Contact to update: '))
        fields: pd.DataFrame = df.iloc[entry].to_list()
        for i, item in enumerate(fields):
                print(f"{i}: {item}")
        field_index: int = int(input('Field to update: '))
        updated_value: str = input('New value: ')
        df.iloc[entry, field_index] = updated_value
        write_contacts_db(df, 'w', True)
        print('Contact updated!')

def delete_contact() -> None:
        """Delete a contact from the DataFrame
        """
        df: pd.DataFrame = pd.read_csv(contacts_database_location)
        entry: str = int(input('Contact index # to delete: '))
        df.drop(index=entry, inplace=True)
        write_contacts_db(df, 'w', True)
        print('Contact deleted!')

def display_all_contacts() -> None:
        """Display all contacts
        """
        df: pd.DataFrame = pd.read_csv(contacts_database_location)
        print(df)
        
if __name__ == "__main__":
        check_db_exists()
        
        while True:
                display_menu()
                choice: str = input('Enter choice: ')
                print(separator)
                match choice:
                        case '1':
                                add_contact()
                        case '2':
                                df: pd.DataFrame = load_contacts_db()
                                filtered_rows: List = search_contacts(df, input('Search for name: '))
                                # Using list comprehension to print the rows and format as a new dataframe
                                # so they look nice
                                [print(df.iloc[i].to_frame().T) for i in filtered_rows]
                                print(separator)
                        case '3':
                                update_contact()
                                print(separator)
                        case '4':
                                delete_contact()
                                print(separator)
                        case '5':
                                display_all_contacts()
                                print(separator)
                        case '6':
                                break