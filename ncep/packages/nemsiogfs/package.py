# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nemsiogfs
#
# You can edit this file again by typing:
#
#     spack edit nemsiogfs
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Nemsiogfs(CMakePackage):
    """
    Performs I/O for the NEMS-GFS model. This is part of the NCEPLIBS project.
    """

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs/archive/refs/tags/v2.5.3.tar.gz"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('2.5.3', sha256='bf84206b08c8779787bef33e4aba18404df05f8b2fdd20fc40b3af608ae4b9af')

    depends_on('nemsio')

