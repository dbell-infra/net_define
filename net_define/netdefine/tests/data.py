template_text = """
---
name: test_template
features:
  - test_feature.yml
"""

feature_text = """
---
meta:
  component: test_component.j2
config:
  hello: world
"""

bad_feature_text = """
---
meta:
  component: test_component.j2
conf:
  hello: world
"""

component_text = """
hello {{ hello }} from netdefine
"""

changed_component_text = """
hello again {{ hello }} from netdefine
"""

changed_feature_text = """
---
meta:
  component: test_component.j2
config:
  hello: universe
"""

bad_template_text = """
---
meta:
  component: bad_reference.j2
config:
  hello: universe
"""