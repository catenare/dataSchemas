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

import python_jsonschema_objects as pjs

BASE_PATH = 'definitions'


def load_schema(schema_file):
    schema_object = None
    schema_file = BASE_PATH + '/' + schema_file
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
    schema_list = {}
    for k, v in schemas.items():
        schema_object = {}
        schema_object.update(base)
        schema_object['$id'] = f'http://localhost/{k}.json'
        properties = {}
        for yml_file in v:
            properties.update(load_schema(yml_file))
        schema_object['properties'] = properties
        save_json_file(k, schema_object)
        schema_list[k] = schema_object
    return schema_list


def create_object(schema):
    builder = pjs.ObjectBuilder(schema)
    classes = builder.build_classes()
    for x in dir(classes):
        print(x)


def main():
    print("Generator started")
    base.update(load_schema(definitions_path))
    schema_list = generate_schema_files(schemas, base)
    schema = schema_list['session']
    create_object(schema)
    print('Generator done')


main()
