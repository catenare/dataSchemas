'''
Schemas
  center - create a new center
  session - new session for the school/year
  registration - register a child into the process
'''
import json
from yaml import load, dump, FullLoader
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_schema(schema_file):
    schema_object = None
    with open(schema_file, 'r') as current_schema_file:
        return load(current_schema_file, Loader=FullLoader)


definitions_path = 'definitions.yml'

base = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    '$id': 'http://localhost/center.json',
    'additionalProperties': False,
    'properties': {}
}

schemas = {
    'center': ['center/center.yml'],
    'session': ['center/session.yml'],
    'registration': ['child/child.yml', 'child/guardian.yml']
}


def save_json_file(file_name, schema_object):
    json_file_name = f'schemas/{file_name}.json'
    with open(json_file_name, 'w') as write_file:
        json.dump(schema_object, write_file)


def generate_schema_files(schemas, base):
    for k, v in schemas.items():
        schema_object = {}
        schema_object.update(base)
        schema_object['$id'] = f'http://localhost/{k}.json'
        properties = {}
        for yml_file in v:
            properties.update(load_schema(yml_file))
            # schema_object['properties'].update(properties)
        schema_object['properties'] = properties
        # print(f"File: {yml_file} Object: {k} Keys: ",
        # schema_object['properties'].keys(), "===========")
        save_json_file(k, schema_object)


def main():
    base.update(load_schema(definitions_path))
    generate_schema_files(schemas, base)
    print('Generator done')


main()
# with open('center.json', 'w') as write_file:
# json.dump(base_write_file)
# create the base schema
# create the center schema
# create the session schema
# create the registration schema
# transaction schema
