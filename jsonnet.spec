# Copyright 2023 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: jsonnet
Epoch: 100
Version: 0.19.1
Release: 1%{?dist}
Summary: A data templating language for app and tool developers
License: Apache-2.0
URL: https://github.com/google/jsonnet/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?centos_version} == 700
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
%endif
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: gcc-c++
BuildRequires: python-rpm-macros
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
A data templating language for app and tool developers based on JSON.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?centos_version} == 700
. /opt/rh/devtoolset-11/enable
%endif
export CFLAGS="%{optflags} -Ithird_party/md5 -Ithird_party/json -Ithird_party/rapidyaml/rapidyaml -Iinclude -fPIC"
export CXXFLAGS="%{optflags} -Ithird_party/md5 -Ithird_party/json -Ithird_party/rapidyaml/rapidyaml -Iinclude -fPIC"
%cmake \
    -DCMAKE_LD_FLAGS="-static" \
    -DCMAKE_FIND_LIBRARY_SUFFIXES=".a" \
    -DBUILD_SHARED_BINARIES=OFF \
    -DBUILD_STATIC_LIBS=ON \
    -DBUILD_TESTS=OFF
%cmake_build
%py3_build

%install
%cmake_install
%py3_install
find %{buildroot} -type f -name '*.a' -exec rm -rf {} \;
find %{buildroot}%{python3_sitearch} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitearch}

%check

%if 0%{?suse_version} > 1500
%package -n libjsonnet0
Summary: Shared Libraries for jsonnet

%description -n libjsonnet0
This package ships the shared object.

%package -n jsonnet-devel
Summary: Development Headers for jsonnet
Requires: libjsonnet0 = %{epoch}:%{version}-%{release}

%description -n jsonnet-devel
This package ships the development files.

%package -n python%{python3_version_nodots}-jsonnet
Summary: jsonnet Bindings for Python
Requires: python3
Provides: python3-jsonnet = %{epoch}:%{version}-%{release}
Provides: python3dist(jsonnet) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-jsonnet = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(jsonnet) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-jsonnet = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(jsonnet) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-jsonnet
This package ships the Python binding.

%post -n libjsonnet0 -p /sbin/ldconfig
%postun -n libjsonnet0 -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/*

%files -n libjsonnet0
%{_libdir}/libjsonnet*.so.*

%files -n jsonnet-devel
%dir %{_prefix}/lib/cmake
%dir %{_prefix}/lib/cmake/c4core
%{_includedir}/*
%{_libdir}/*.so
%{_prefix}/lib/cmake/c4core/*
%{_prefix}/lib/libc4core.so

%files -n python%{python3_version_nodots}-jsonnet
%{python3_sitearch}/*
%endif

%if 0%{?sle_version} > 150000
%package -n libjsonnet0
Summary: Shared Libraries for jsonnet

%description -n libjsonnet0
This package ships the shared object.

%package -n jsonnet-devel
Summary: Development Headers for jsonnet
Requires: libjsonnet0 = %{epoch}:%{version}-%{release}

%description -n jsonnet-devel
This package ships the development files.

%package -n python3-jsonnet
Summary: jsonnet Bindings for Python
Requires: python3
Provides: python3-jsonnet = %{epoch}:%{version}-%{release}
Provides: python3dist(jsonnet) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-jsonnet = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(jsonnet) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-jsonnet = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(jsonnet) = %{epoch}:%{version}-%{release}

%description -n python3-jsonnet
This package ships the Python binding.

%post -n libjsonnet0 -p /sbin/ldconfig
%postun -n libjsonnet0 -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/*

%files -n libjsonnet0
%{_libdir}/libjsonnet*.so.*

%files -n jsonnet-devel
%dir %{_prefix}/lib/cmake
%dir %{_prefix}/lib/cmake/c4core
%{_includedir}/*
%{_libdir}/*.so
%{_prefix}/lib/cmake/c4core/*
%{_prefix}/lib/libc4core.so

%files -n python3-jsonnet
%{python3_sitearch}/*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n jsonnet-libs
Summary: Shared Libraries for jsonnet

%description -n jsonnet-libs
This package ships the shared object.

%package -n jsonnet-devel
Summary: Development Headers for jsonnet
Requires: jsonnet-libs = %{epoch}:%{version}-%{release}

%description -n jsonnet-devel
This package ships the development files.

%package -n python3-jsonnet
Summary: jsonnet Bindings for Python
Requires: python3
Requires: jsonnet-libs = %{epoch}:%{version}-%{release}
Provides: python3-jsonnet = %{epoch}:%{version}-%{release}
Provides: python3dist(jsonnet) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-jsonnet = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(jsonnet) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-jsonnet = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(jsonnet) = %{epoch}:%{version}-%{release}

%description -n python3-jsonnet
This package ships the Python binding.

%post -n jsonnet-libs -p /sbin/ldconfig
%postun -n jsonnet-libs -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/*

%files -n jsonnet-libs
%{_libdir}/libjsonnet*.so.*

%files -n jsonnet-devel
%dir %{_prefix}/lib/cmake
%dir %{_prefix}/lib/cmake/c4core
%{_includedir}/*
%{_libdir}/*.so
%{_prefix}/lib/cmake/c4core/*
%{_prefix}/lib/libc4core.so

%files -n python3-jsonnet
%{python3_sitearch}/*
%endif

%changelog
