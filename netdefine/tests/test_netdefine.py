from netdefine.core import NetDefine
from .data import template_text, feature_text, component_text, \
    changed_component_text, changed_feature_text, bad_template_text
import pytest


# Set up directory structure and test files for test session
@pytest.fixture()
def file_structure(tmp_path):

    root = tmp_path / 'globomantics'
    root.mkdir()

    features = tmp_path / 'globomantics/features'
    features.mkdir()
    test_feature = features / 'test_feature.yml'
    test_feature.write_text(feature_text)

    templates = tmp_path / 'globomantics/templates'
    templates.mkdir()
    test_template = templates / "test_template.yml"
    test_template.write_text(template_text)

    components = tmp_path / 'globomantics/components'
    components.mkdir()
    test_component = components / "test_component.j2"
    test_component.write_text(component_text)

    configs = tmp_path / 'globomantics/configs'
    configs.mkdir()

    return root


def test_netdefine_load(file_structure):
    netdefine = NetDefine(root=file_structure)
    assert netdefine


def test_netdefine_plan_no_changes(file_structure):
    netdefine = NetDefine(root=file_structure)
    plan = netdefine.plan()
    assert not plan


def test_netdefine_plan_component_changes(file_structure):
    NetDefine(root=file_structure)
    changed_component = file_structure / 'components/test_component.j2'
    changed_component.write_text(changed_component_text)
    netdefine_changed = NetDefine(root=file_structure)
    plan = netdefine_changed.plan()
    assert plan


def test_netdefine_plan_feature_changes(file_structure):
    NetDefine(root=file_structure)
    changed_feature = file_structure / 'features/test_feature.yml'
    changed_feature.write_text(changed_feature_text)
    netdefine_changed = NetDefine(root=file_structure)
    plan = netdefine_changed.plan()
    assert plan


def test_netdefine_apply(file_structure):
    netdefine = NetDefine(root=file_structure)
    apply = netdefine.apply(change='test_change')
    assert apply
    assert type(apply) is list


def test_netdefine_apply_dry_run(file_structure):
    netdefine = NetDefine(root=file_structure)
    apply = netdefine.apply(change='test_change', dry_run=True)
    assert apply
    assert type(apply) is list



def test_netdefine_apply_difference_changes(file_structure):
    NetDefine(root=file_structure)
    changed_component = file_structure / 'components/test_component.j2'
    changed_component.write_text(changed_component_text)
    netdefine_changed = NetDefine(root=file_structure)
    apply = netdefine_changed.apply(change='test_change', difference=True)
    assert apply
    assert type(apply) is list


def test_netdefine_apply_difference_changes_dry_run(file_structure):
    NetDefine(root=file_structure)
    changed_component = file_structure / 'components/test_component.j2'
    changed_component.write_text(changed_component_text)
    netdefine_changed = NetDefine(root=file_structure)
    apply = netdefine_changed.apply(change='test_change', difference=True, dry_run=True)
    assert apply
    assert type(apply) is list


def test_netdefine_apply_difference_no_changes(file_structure):
    netdefine = NetDefine(root=file_structure)
    apply = netdefine.apply(change='test_change', difference=True)
    assert not apply


def test_netdefine_render_templates(file_structure):
    netdefine = NetDefine(root=file_structure)
    templates = netdefine.render_templates()
    assert templates


def test_netdefine_render_bad_templates(file_structure):
    bad_template = file_structure / 'templates/test_template.j2'
    bad_template.write_text(bad_template_text)
    netdefine = NetDefine(root=file_structure)
    templates = netdefine.render_templates()
    assert type(templates) is Exception

