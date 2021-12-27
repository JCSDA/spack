# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymol(PythonPackage):
    """PyMOL is a Python-enhanced molecular graphics tool. It excels at 3D
       visualization of proteins, small molecules, density, surfaces, and
       trajectories. It also includes molecular editing, ray tracing, and
       movies. Open Source PyMOL is free to everyone!"""

    homepage = "https://pymol.org"
    url      = "https://github.com/schrodinger/pymol-open-source/archive/v2.4.0.tar.gz"

    version('2.5.0', sha256='aa828bf5719bd9a14510118a93182a6e0cadc03a574ba1e327e1e9780a0e80b3')
    version('2.4.0', sha256='5ede4ce2e8f53713c5ee64f5905b2d29bf01e4391da7e536ce8909d6b9116581')
    version('2.3.0', sha256='62aa21fafd1db805c876f89466e47513809f8198395e1f00a5f5cc40d6f40ed0')

    depends_on('python+tkinter@2.7:', type=('build', 'run'), when='@2.3.0:2.4.0')
    depends_on('python+tkinter@3.6:', type=('build', 'run'), when='@2.5.0:')
    depends_on('gl')
    depends_on('glew')
    depends_on('libpng')
    depends_on('freetype')
    depends_on('glm')
    depends_on('libmmtf-cpp')
    depends_on('msgpack-c@2.1.5:')
    depends_on('netcdf-cxx4')
    depends_on('libxml2')
    depends_on('py-pmw-patched', type=('build', 'run'))
    depends_on('py-pyqt5', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    def install_args(self, spec, prefix):
        args = super(PyPymol, self).install_args(spec, prefix)
        args.append('--no-launcher')
        return args

    @run_after('install')
    def install_launcher(self):
        binpath = self.prefix.bin
        mkdirp(self.prefix.bin)
        fname = join_path(binpath, 'pymol')
        script = join_path(self.prefix,
                           self.spec['python'].package.site_packages_dir,
                           'pymol',
                           '__init__.py')

        shebang = '#!/bin/sh\n'
        fdata = 'exec {0} {1} \"$@\"'.format(self.spec['python'].command,
                                             script)
        with open(fname, 'w') as new:
            new.write(shebang + fdata)
        set_executable(fname)
