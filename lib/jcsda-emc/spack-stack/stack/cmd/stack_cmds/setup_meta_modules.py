from spack.extensions.stack.meta_modules import setup_meta_modules

description = "Create meta-modules"
section = "spack-stack"
level = "long"


# Add potential arguments to setup-meta-modules
def setup_meta_modules_parser(subparser):
    pass


def stack_setup_meta_modules(parser, args):
    setup_meta_modules()
