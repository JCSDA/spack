# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class UfsWeatherModelEnv(BundlePackage):
    """Development environment for ufs-weathermodel-bundle"""

    homepage = "https://github.com/ufs-community/ufs-weather-model"
    git      = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers = ['kgerheiser', 'climbfuji']

    version('1.0.0', branch='develop')
    variant('python', default=True, description='Build Python dependencies')

    depends_on('base-env', type='run')

    depends_on('esmf~debug', type='run')
    depends_on('esmf@8.3.0b09~debug', when='@1.0.0', type='run')

    depends_on('mapl~debug', type='run')
    depends_on('fms', type='run')

    depends_on('bacio', type='run')
    depends_on('crtm', type='run')
    depends_on('g2', type='run')
    depends_on('g2tmpl', type='run')
    depends_on('ip', type='run')
    depends_on('sp', type='run')
    depends_on('w3nco', type='run')
    depends_on('w3emc', type='run')

    depends_on('ufswm-pyenv', when='+python')
