# This is a spec file for fedora rpm
# Big fat Warning:
# - has not tested yet if commit hash of HEAD changes (i.e. does rpmbuild really build 'latest')
# - does work only with rpmbuild command, mock refuses to install BuildRequires dependencies

%global         _hardened_build 1
%global         githubparent    keystone-engine
%global         commit          18569351000cf1b8bd1ea2cc8a02c2e17b76391f
%global         latest          %(/usr/bin/git ls-remote https://github.com/keystone-engine/keystone.git HEAD | cut -f1)
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         commitdate      20220606
%global         gitversion      .git%{shortcommit}
%if "%{commit}" != "%{latest}"
%global         commit          %(/usr/bin/git ls-remote https://github.com/keystone-engine/keystone.git HEAD | cut -f1)
%global         archive         %(c=%{commit}; curl -L https://api.github.com/repos/keystone-engine/keystone/tarball/$c > "SOUCES/keystone-${c:0:7}.tar.gz")
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         commitdate      %(date '+%Y%m%d')
%global         gitversion      .git%{shortcommit}
%endif

Name:           keystone
Version:        %{commitdate}
Release:        1%{gitversion}%{?dist}
Summary:        Multi architecture assembler framework
Group:          Development/Libraries
License:        GPLv2 and commercial royalty-free
URL:            https://github.com/%{githubparent}/%{name}
Source0:        https://api.github.com/repos/%{githubparent}/%{name}/tarball/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  git-core
BuildRequires:  cmake

%description
Keystone is a lightweight multi-platform, multi-architecture assembler framework.
It offers some unparalleled features:

- Multi-architecture, with support for Arm, Arm64 (AArch64/Armv8), Ethereum Virtual Machine, Hexagon, Mips, PowerPC, Sparc, SystemZ & X86 (include 16/32/64bit).
- Clean/simple/lightweight/intuitive architecture-neutral API.
- Implemented in C/C++ languages, with bindings for Java, Masm, C#, PowerShell, Perl, Python, NodeJS, Ruby, Go, Rust, Haskell, VB6 & OCaml available.
- Native support for Windows & \*nix (with Mac OSX, Linux, \*BSD & Solaris confirmed).
- Thread-safe by design.
- Open source - with a dual license.

Keystone is based on LLVM, but it goes much further with [a lot more to offer](/docs/beyond_llvm.md).

Further information is available at http://www.keystone-engine.org


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with the %{name} library.

%prep
%setup -q -n %{githubparent}-%{name}-%{shortcommit}

%build
%cmake ..
%cmake_build

%install
%cmake_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/kstool
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Jun 06 2022 Juha Nikkanen <nikkej@gmail.com> - 0.9.2-1.20220606git1856935
- Initial Release

