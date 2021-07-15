import click
import pprint
from core import NetDefine

netdefine = NetDefine(root='.')
printer = pprint.PrettyPrinter(indent=2)

@click.group()
def cli():
    pass


@cli.command()
def plan():
    result = netdefine.plan()
    if result:

        templates = result['templates_changed']
        features = result['features_changed']
        components = result['components_changed']

        print(f"\nNetdefine has detected changes.")

        if features:
            print('\nThe following features have been changed:')
            for feature in features:
                print(f"  - {feature}")
        if components:
            print('\nThe following components have been changed:')
            for component in components:
                print(f"  - {component}")
        if templates:
            print(f"\nThe following device configurations are affected by changes")
            for template in templates:
                print(f"  - Device Template: {template}")

        print("\n Run apply to update device configurations")
    else:
        print('The state has not changed since the last apply')

@cli.command()
@click.argument('change')
@click.option('--difference', is_flag=True)
@click.option('--dry_run', is_flag=True)
@click.option('--display', is_flag=True)
@click.option('--target')
def apply(change, difference, dry_run, display, target):
    if difference:
        templates = netdefine.apply(change=change, difference=True, dry_run=dry_run, target=target)
    else:
        templates = netdefine.apply(change=change, dry_run=dry_run, target=target)
    if templates:
        print(f'apply success for change {change}\n')
    if display:
        for template in templates:
            print(f'Template: \n {template["template"]} \n')
            print(f'Config: \n\n{template["config"]}\n')



if __name__=='__main__':
    cli()