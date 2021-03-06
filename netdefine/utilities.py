import os
import json
import hashlib
from deepdiff import DeepDiff
import yaml
import sys
from configparser import ConfigParser

class Files:
    def __init__(self, root, environment, output_directory='configs'):
        self.root = root
        self.output_directory = f'{root}/{output_directory}'
        self.environment = environment
        try:
            self.templates = os.listdir(f"{self.root}/templates")
            self.features = os.listdir(f"{self.root}/features")
            self.components = os.listdir(f"{self.root}/components")
        except FileNotFoundError:
            choice = input('Project structure not found, create project? y/n ')
            if choice == "y":
                project_name = input('project name:')
                self.create_directory_structure(project_name)
                self.create_cfg(project_name)
                sys.exit(0)
            else:
                sys.exit(1)

    def write_file(self, file_name, data):
        if self.environment == 'local':
            with open(f"{self.output_directory}/{file_name}", 'w') as file:
                file.write(data)

    def read_file(self, file_name, bytes=False, from_yaml=False):
        if self.environment == 'local':
            if bytes:
                with open(f"{self.root}/{file_name}", 'rb') as file:
                    return file.read()
            if from_yaml:
                with open(f"{self.root}/{file_name}") as file:
                    return yaml.safe_load(file.read())
            with open(f"{self.root}/{file_name}") as file:
                return file.read()


    def get_state(self):
        try:
            # print(f'attepting to load state file: {self.root}/state.json')
            state = json.loads(self.read_file('state.json'))
            return state
        except:
            return None



    def create_directory_structure(self, project_name):
        if not os.path.exists(project_name):
            print(f'creating directory: {project_name}/components')
            os.makedirs(f'{project_name}/components')
            print(f'creating directory: {project_name}/configs')
            os.makedirs(f'{project_name}/configs')
            print(f'creating directory: {project_name}/features')
            os.makedirs(f'{project_name}/features')
            print(f'creating directory: {project_name}/templates')
            os.makedirs(f'{project_name}/templates')
    def create_cfg(self, project_name):
        print('creating config file: netdefine.cfg')
        with open('netdefine.cfg', 'w') as file:
            config = ConfigParser()
            config['DEFAULT'] = {'root': project_name}
            config.write(file)





class State:
    def __init__(self, root, environment, output_directory='configs'):
        self.files = Files(root, environment, output_directory)

        if not self.files.get_state():
            print('State file not found, building state...')
            state = self.build_state()
            self.files.write_file('state.json', json.dumps(state))
            self.state_current = self.files.get_state()
            print('state built successfully')
        else:
            self.state_current = self.files.get_state()
        self.state_change = self.build_state()




        # self.files.write_file('state.json', json.dumps(self.state, indent=2))

    def calculate_md5(self, file):
        data = self.files.read_file(file_name=file, bytes=True)
        return hashlib.md5(data).hexdigest()

    def build_state(self):
        state = {'features': {}, 'components': {}, 'templates': {}}
        for feature in self.files.features:
            feature_state = {'hash': self.calculate_md5(f'features/{feature}')}
            state['features'][feature] = feature_state
        for component in self.files.components:
            component_state = {'hash': self.calculate_md5(f'components/{component}')}
            state['components'][component] = component_state
        for template in self.files.templates:
            template_state = {'hash': self.calculate_md5(f'templates/{template}')}
            state['templates'][template] = template_state
        return state

    def determine_state(self):
        diff = DeepDiff(self.state_current, self.state_change)

        return diff

    def update_state(self):
        self.files.write_file('state.json', json.dumps(self.state_change, indent=2))
        self.state_current = self.files.get_state()



