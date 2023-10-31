# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ip(CMakePackage):
    """The NCEP general interpolation library (iplib) contains Fortran 90
    subprograms to be used for interpolating between nearly all grids used at
    NCEP. This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-ip"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-ip/archive/refs/tags/v3.3.3.tar.gz"

    maintainers("t-brown", "AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA")

    version("4.4.0", sha256="858d9201ce0bc4d16b83581ef94a4a0262f498ed1ea1b0535de2e575da7a8b8c")
    version("4.3.0", sha256="799308a868dea889d2527d96a0405af7b376869581410fe4cff681205e9212b4")
    # Note that versions 4.0-4.2 contain constants_mod module, and should not be used when
    # also compiling with packages containing Fortran modules of the same name, namely, FMS.
    version("4.1.0", sha256="b83ca037d9a5ad3eb0fb1acfe665c38b51e01f6bd73ce9fb8bb2a14f5f63cdbe")
    version("4.0.0", sha256="a2ef0cc4e4012f9cb0389fab6097407f4c623eb49772d96eb80c44f804aa86b8")
    version(
        "3.3.3",
        sha256="d5a569ca7c8225a3ade64ef5cd68f3319bcd11f6f86eb3dba901d93842eb3633",
        preferred=True,
    )

    variant("openmp", description="Enable OpenMP threading", default=True)
    variant("pic", default=True, description="Build with position-independent-code")
    variant("shared", default=False, description="Build shared library", when="@4.1:")
    variant(
        "precision",
        default=["4", "d"],
        values=["4", "d"],
        multi=True,
        description="Set precision (_4/_d library versions)",
        when="@4.1:",
    )

    depends_on("sp")
    depends_on("sp@:2.3.3", when="@:4.0")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP", "openmp"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

        if self.spec.satisfies("@4:"):
            args.append(self.define("BUILD_TESTING", "NO"))
        else:
            args.append(self.define("ENABLE_TESTS", "NO"))

        if self.spec.satisfies("@4.1:"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
            for prec in ["4", "d"]:
                if not self.spec.satisfies("precision=" + prec):
                    args += ["-DBUILD_%s:BOOL=OFF" % prec.upper()]

        return args

    def setup_run_environment(self, env):
        suffixes = (
            self.spec.variants["precision"].value
            if self.spec.satisfies("@4.1:")
            else ["4", "8", "d"]
        )
        shared = False if self.spec.satisfies("@:4.0") else self.spec.satisfies("+shared")
        for suffix in suffixes:
            lib = find_libraries(
                "libip_" + suffix, root=self.prefix, shared=shared, recursive=True
            )
            env.set("IP_LIB" + suffix, lib[0])
            env.set("IP_INC" + suffix, join_path(self.prefix, "include_" + suffix))
