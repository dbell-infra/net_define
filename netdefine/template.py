from jinja2 import Template
from .utilities import Files



class ConfigTemplate:
    def __init__(self, root, template, environment):
        self.root = root
        self.environment = environment
        self.files = Files(root=self.root, environment=self.environment)
        self.template = self.files.read_file(f'templates/{template}', from_yaml=True)
        self.features = self.resolve_features()

    @staticmethod
    def render_template(data, template):
        rendered = Template(template).render(**data)
        return rendered

    def resolve_features(self):
        features = []
        for feature in self.template['features']:
            data = self.files.read_file(f'features/{feature}', from_yaml=True)
            features.append({'name': feature, 'data': data})
        return features

    def produce_template(self):
        output = []
        for feature in self.features:
            try:
                feature_output = self.render_template(
                    data=feature['data']['config'],
                    template=self.files.read_file(f"components/{feature['data']['meta']['component']}")
                    )
                output.append(feature_output)
            except KeyError:
                raise Exception(f"Unable to parse Feature: {feature['name']} ")
        return "\n".join(output)


