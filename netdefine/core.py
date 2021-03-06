from .template import ConfigTemplate
from .utilities import Files, State


class NetDefine:
    def __init__(self, root, environment='local'):
        self.environment = environment
        self.files = Files(root=root, environment=self.environment)
        self.templates = self.files.templates
        self.features = self.files.features
        self.root = root
        self.state = State(root=self.root, environment=self.environment, output_directory="/")

    def render_templates(self, change=None, subset=None, dry_run=False):
        template_output = []
        try:
            if subset:
                templates = [template for template in self.templates if template in subset]
                for template in templates:
                    config = ConfigTemplate(root=self.root, template=template, environment=self.environment)
                    template_output.append({'template': template, 'config': config.produce_template()})
                    if not dry_run:
                        self.files.write_file(file_name=f"{change}-config-{template}.txt", data=config.produce_template())
            else:
                for template in self.templates:
                    config = ConfigTemplate(root=self.root, template=template, environment=self.environment)
                    template_output.append({'template': template, 'config': config.produce_template()})
                    if not dry_run:
                        self.files.write_file(file_name=f"{change}-config-{template}.txt", data=config.produce_template())
        except Exception as e:
            print(e)
            return Exception('An issue occured during template load')
        return template_output

    def init(self, project):
        self.files.create_directory_structure(project=project)

    @staticmethod
    def parse_value(value):
        # garbage hack to make the diff response able to be consumed easier down the road
        name = value[4:].split("[")[2][1:-2]
        type = (value[4:].split("[")[1][1:-2])

        return {'type': type, "name": name}

    def plan(self):
        diff = self.state.determine_state()
        if diff == {}:
            return None
        else:
            features_changed = None
            templates = None
            components_changed = None
            templates_added = None
            templates_removed = None

            # handle added templates
            if 'dictionary_item_added' in diff:
                added = []
                for item in diff['dictionary_item_added']:
                    value_data = self.parse_value(item)
                    added.append(value_data)

                templates_added = [item['name'] for item in added if item['type'] == 'templates']

            # handle removed templates
            if 'dictionary_item_removed' in diff:
                removed = []
                for item in diff['dictionary_item_removed']:
                    value_data = self.parse_value(item)
                    removed.append(value_data)

                templates_removed = [item['name'] for item in removed if item['type'] == 'templates']

            # handle changed values in existing templates
            if "values_changed" in diff:
                changed = []
                for value in diff['values_changed']:
                    value_data = self.parse_value(value)
                    changed.append(value_data)

                # Collect components and features that have changed
                components_changed = [item['name'] for item in changed if item['type'] == 'components']
                features_changed = [item['name'] for item in changed if item['type'] == 'features']

                # Determine if any changes affect a device template
                templates = []

                if components_changed:
                    features = []
                    # If a component has been changed, look for features that reference the component
                    for entry in components_changed:
                        for feature in self.features:
                            feature_data = self.files.read_file(f'features/{feature}', from_yaml=True)
                            if feature_data['meta']['component'] == entry and entry not in features:
                                features.append(feature)
                    # In our collection of features referenced by a changed component,
                    # find templates that reference the feature.
                    for feature in features:
                        for template in self.templates:
                            template_data = self.files.read_file(f'templates/{template}', from_yaml=True)
                            if feature in template_data['features'] and template not in templates:
                                templates.append(template)

                if features_changed:
                    for feature in features_changed:
                        for template in self.templates:
                            template_data = self.files.read_file(f'templates/{template}', from_yaml=True)
                            if feature in template_data['features'] and template not in templates:
                                templates.append(template)

            return {'templates_changed': templates,
                    'features_changed': features_changed,
                    'components_changed': components_changed,
                    'templates_added': templates_added,
                    'templates_removed': templates_removed}

    def apply(self, change, difference=False, dry_run=False, target=None):
        if dry_run:
            if difference:
                templates = self.render_templates(change, subset=self.plan()['templates_changed'], dry_run=dry_run)
                return templates
            if target:
                templates = self.render_templates(change, subset=[target], dry_run=dry_run)
            else:
                templates = self.render_templates(change, dry_run=dry_run)
        else:
            if difference:
                subset = self.plan()
                if subset:
                    templates = self.render_templates(change, subset=subset['templates_changed'])
                    self.state.update_state()
                    return templates
                else:
                    return None
            else:
                templates = self.render_templates(change)
                self.state.update_state()
        return templates


