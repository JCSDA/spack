# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import sys

from spack import *


class EmcVerifGlobal(BundlePackage):
    """Development environment for emc-verif-global"""

    homepage = "https://github.com/NOAA-EMC/EMC_verif-global"
    git      = "https://github.com/NOAA-EMC/EMC_verif-global.git"

    maintainers = ['kgerheiser']

    version('develop', branch='develop')

    depends_on('netcdf-fortran')
    depends_on('nco')
    depends_on('prod-util')
    depends_on('grib-util')
    # depends_on('grads')
    depends_on('met')
    depends_on('metplus')
