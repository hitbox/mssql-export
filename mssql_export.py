import argparse
import configparser
import os
import pyodbc

def generate_schema_scripts(config):
    output_directory = config['Output']['Directory']

    # Query to get all user-defined objects (tables, views, stored procedures, functions, etc.)
    query = """
    SELECT 
        o.type_desc,
        s.name AS schema_name,
        o.name AS object_name,
        m.definition AS object_definition
    FROM 
        sys.objects o
    INNER JOIN 
        sys.sql_modules m ON o.object_id = m.object_id
    LEFT JOIN 
        sys.schemas s ON o.schema_id = s.schema_id
    WHERE 
        o.type IN ('U', 'V', 'P', 'FN', 'IF', 'TF')
    """

    cursor.execute(query)

    for row in cursor.fetchall():
        object_type = row.type_desc.lower().strip()
        schema_name = row.schema_name
        object_name = row.object_name
        object_definition = row.object_definition

        # Create directory for the schema if it doesn't exist
        schema_directory = os.path.join(output_directory, schema_name)
        if not os.path.exists(schema_directory):
            os.makedirs(schema_directory)

        # Write object definition to file
        object_file = os.path.join(schema_directory, f"{object_name}.sql")
        with open(object_file, 'w') as f:
            f.write(f"-- {object_type.upper()}: {object_name}\n")
            f.write(object_definition + '\n\n')

    print("Schema scripts generated for all objects.")

def main():
    parser = argparse.ArgumentParser(
        description = '',
    )
    parser.add_argument(
        'config',
        help = 'INI config file.',
    )
    args = parser.parse_args()

    cp = configparser.ConfigParser()
    cp.read(args.config)

    pyodbc.connect(**cp['export'])

if __name__ == "__main__":
    main()
