import os
import spack
import spack.util.spack_yaml as syaml
from spack.extensions.stack.stack_paths import stack_path, template_path, container_path
import copy


class StackContainer():
    """Represents an abstract container. It takes in a
    container template (spack.yaml), the specs from an app, and
    its packages.yaml versions then writes out a merged file.
    """

    def __init__(self, container, template, name, dir, base_packages) -> None:
        self.template = template
        self.container = container

        test_path = os.path.join(container_path, container + '.yaml')
        if os.path.exists(test_path):
            self.container_path = test_path
        elif os.path.isabs(container):
            self.container_path = container
        else:
            raise Exception("Invalid container {}".format(self.container))

        if os.path.isabs(template):
            self.template_path = template
        elif os.path.exists(os.path.join(template_path, template)):
            self.template_path = os.path.join(template_path, template)
        else:
            raise Exception("Invalid template")

        self.name = name if name else '{}.{}'.format(template, container)

        self.dir = dir
        self.env_dir = os.path.join(self.dir, self.name)
        self.base_packages = base_packages

    def write(self):
        """Merge base packages and app's spack.yaml into
        output container file.
        """
        app_env = os.path.join(self.template_path, 'spack.yaml')
        with open(app_env, 'r') as f:
            # Spack uses :: to override settings.
            # but it's not understood when used in a spack.yaml
            filedata = f.read()
            filedata.replace('::', ':')
            filedata = filedata.replace('::', ':')
            template_yaml = syaml.load_config(filedata)

        with open(self.container_path, 'r') as f:
            container_yaml = syaml.load_config(f)

        # Create copy so we can modify it
        original_yaml = copy.deepcopy(container_yaml)

        with open(self.base_packages, 'r') as f:
            filedata = f.read()
            filedata = filedata.replace('::', ':')
            packages_yaml = syaml.load_config(filedata)

        if 'packages' not in container_yaml['spack']:
            container_yaml['spack']['packages'] = {}

        container_yaml['spack']['packages'] = spack.config.merge_yaml(
            container_yaml['spack']['packages'], packages_yaml['packages'])

        container_yaml = spack.config.merge_yaml(container_yaml, template_yaml)
        # Merge the original back in so it takes precedence
        container_yaml = spack.config.merge_yaml(container_yaml, original_yaml)

        container_yaml['spack']['container']['labels']['app'] = self.template

        os.makedirs(self.env_dir, exist_ok=True)

        with open(os.path.join(self.env_dir, 'spack.yaml'), 'w') as f:
            syaml.dump_config(container_yaml, stream=f)
