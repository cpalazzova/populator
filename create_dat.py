import csv
from datetime import datetime


TEMPLATE_ROW = ' ' * 120 + '3537 KESHAUN MEWS                                                               LAKE ALESSIABOROUGH 0000000   201002012025031620261221YESAUTOKarras          Enda           F                                            00000000000000000000SPOUSE   00000000000000000000666135295  0993000000NJ60758     AUTOPALLIS          COLUMBUS       7774176430000000   0000000       WV000000000000000000000                                                                                  00000000001985060832301 MUELLER SUMMIT                                        SOUTH BRYCEFURT     NV1602425540          F                               SEAMUS                                  0000000   EA            00000000           ABNO NO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             20090906        ELIGIBLE            200909061018706361V5506121018706360V82575720251114'

BENE_DOB_INDEXES = (230, 237)
BENE_FIRST_NAME_INDEXES = (277, 291)
BENE_LAST_NAME_INDEXES = (257, 276)
BENE_SSN_INDEXES = (386, 394)
BENE_ICN_INDEXES = (1739, 1755)

SPONSOR_DOB_INDEXES = (602, 609)
SPONSOR_FIRST_NAME_INDEXES = (439, 453)
SPONSOR_LAST_NAME_INDEXES = (419, 438)
SPONSOR_SSN_INDEXES = (454, 462)
SPONSOR_ICN_INDEXES = (1756, 1772)

INPUT_VALUES_FILENAME = 'input_values.csv'
OUTPUT_DAT_FILENAME = 'EligibilityPlus.PED.XXXX.PopulateXXXfor270_XXXXXXXX.DAT'


def convert_dob(dob_str):
    """Convert DOB from MM/DD/YYYY to YYYYMMDD"""
    date_obj = datetime.strptime(dob_str.strip(), '%m/%d/%Y')
    return date_obj.strftime('%Y%m%d')


def populate_row(template_row, values_dict):
    """Populate a template row with values from the CSV"""
    # Convert to list for mutability
    row = list(template_row)
    
    # Map CSV columns to index constants
    field_mapping = {
        'sponsor_first_name': (SPONSOR_FIRST_NAME_INDEXES, False),
        'sponsor_last_name': (SPONSOR_LAST_NAME_INDEXES, False),
        'sponsor_dob': (SPONSOR_DOB_INDEXES, True),  # True = needs DOB conversion
        'sponsor_ssn': (SPONSOR_SSN_INDEXES, False),
        'sponsor_icn': (SPONSOR_ICN_INDEXES, False),
        'bene_first_name': (BENE_FIRST_NAME_INDEXES, False),
        'bene_last_name': (BENE_LAST_NAME_INDEXES, False),
        'bene_dob': (BENE_DOB_INDEXES, True),  # True = needs DOB conversion
        'bene_ssn': (BENE_SSN_INDEXES, False),
        'bene_icn': (BENE_ICN_INDEXES, False),
    }
    
    for field, (indexes, is_dob) in field_mapping.items():
        value = values_dict.get(field, '').strip()
        
        # Convert DOB if needed
        if is_dob and '/' in value:
            value = convert_dob(value)
        
        # Capitalize
        value = value.upper()
        start, end = indexes
        field_length = end - start + 1
        
        # Pad or truncate value to fit the field length
        value = value.ljust(field_length)[:field_length]
        
        # Place characters at correct positions
        for i, char in enumerate(value):
            row[start + i] = char
    
    return ''.join(row)


def main():
    """Read values.csv and generate the fixed-width dat file"""
    try:
        with open(INPUT_VALUES_FILENAME, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            with open(OUTPUT_DAT_FILENAME, 'w') as outfile:
                for row_dict in reader:
                    populated_row = populate_row(TEMPLATE_ROW, row_dict)
                    # Capitalize the entire row
                    populated_row = populated_row.upper()
                    outfile.write(populated_row + '\n\n')
        
        print(f"Successfully created {OUTPUT_DAT_FILENAME}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
