%{?cygwin_package_header}

#%%global snapshot_rev 5747
#%%global branch trunk

Name:           cygwin-w32api-runtime
Version:        5.0.3
Release:        2%{?dist}
Summary:        Windows API libraries for Cygwin toolchain

License:        Public Domain and ZPLv2.1
Group:          Development/Libraries
URL:            http://mingw-w64.sourceforge.net/
BuildArch:      noarch

%if 0%{?snapshot_rev}
# To regenerate a snapshot:
# wget http://sourceforge.net/code-snapshots/svn/m/mi/mingw-w64/code/mingw-w64-code-%{snapshot_rev}-%{branch}.zip
Source0:        mingw-w64-code-%{snapshot_rev}-%{branch}.zip
%else
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-v%{version}.tar.bz2
%endif

BuildRequires:  cygwin32-filesystem
BuildRequires:  cygwin32-binutils
BuildRequires:  cygwin32-w32api-headers >= %{version}
BuildRequires:  cygwin32-gcc

BuildRequires:  cygwin64-filesystem
BuildRequires:  cygwin64-binutils
BuildRequires:  cygwin64-w32api-headers >= %{version}
BuildRequires:  cygwin64-gcc

%description
Windows cross-compiler runtime base libraries for Cygwin toolchain.

%package -n cygwin32-w32api-runtime
Summary:        Windows API libraries for Cygwin32 toolchain
Requires:       cygwin32-filesystem
Requires:       cygwin32-w32api-headers >= %{version}

%description -n cygwin32-w32api-runtime
Windows cross-compiler runtime base libraries for Cygwin32 toolchain.

%package -n cygwin64-w32api-runtime
Summary:        Windows API libraries for Cygwin64 toolchain
Requires:       cygwin64-filesystem
Requires:       cygwin64-w32api-headers >= %{version}

%description -n cygwin64-w32api-runtime
Windows cross-compiler runtime base libraries for Cygwin64 toolchain.


%prep
%if 0%{?snapshot_rev}
%setup -q -n mingw-w64-code-%{snapshot_rev}-%{branch}
%else
%setup -q -n mingw-w64-v%{version}
%endif


%build
pushd mingw-w64-crt
    CYGWIN32_CONFIGURE_ARGS="--disable-lib64"
    CYGWIN64_CONFIGURE_ARGS="--disable-lib32"
    %cygwin_configure --enable-w32api
    %cygwin_make %{?_smp_mflags}
popd


%install
pushd mingw-w64-crt
    %cygwin_make_install DESTDIR=$RPM_BUILD_ROOT
popd

# Dunno what to do with these files
rm -fr $RPM_BUILD_ROOT%{cygwin32_includedir}/w32api/*.c
rm -fr $RPM_BUILD_ROOT%{cygwin64_includedir}/w32api/*.c


%files -n cygwin32-w32api-runtime
%doc COPYING DISCLAIMER DISCLAIMER.PD
%{cygwin32_libdir}/w32api/

%files -n cygwin64-w32api-runtime
%doc COPYING DISCLAIMER DISCLAIMER.PD
%{cygwin64_libdir}/w32api/


%changelog
* Mon Dec 04 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 5.0.3-2
- Require only matching w32api-headers version, not release

* Wed Nov 15 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 5.0.3-1
- new version

* Wed Mar 30 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 4.0.5-1
- new version

* Sun Feb 21 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 4.0.4-1
- new version

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 3.3.0-1
- new version

* Mon Sep 01 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 3.2.0-1
- Version bump

* Thu Jan 16 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 3.1.0-1
- Update to latest stable release.

* Thu Jun 27 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.0.999-0.15.trunk.r5747
- Update to SVN trunk.
- Update to new Cygwin packaging scheme.

* Tue Oct 16 2012 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.0.999-0.13.trunk.20121215
- Change name and update to match current Cygwin package.

* Tue Oct 16 2012 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 2.0.999-0.13.trunk.20121016
- Replace mingw.org w32api with mingw-w64 to match Cygwin distribution.
