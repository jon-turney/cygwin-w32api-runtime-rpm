%{?cygwin_package_header}

#%%global snapshot_rev 5747
#%%global branch trunk

Name:           cygwin-w32api-runtime
Version:        13.0.0
Release:        1%{?dist}
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


# Note about standard dlls
# ------------------------------------------------------------
#
# We want to be able to build & install cygwin libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the cygwin toolchain to develop software (i.e. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
# (rpm -ql cygwin32-w32api-runtime | grep '\.a$' | while read f ; do i686-pc-cygwin-dlltool   -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-cygwin32
Source1:       standard-dlls-cygwin32
# (rpm -ql cygwin64-w32api-runtime | grep '\.a$' | while read f ; do x86_64-pc-cygwin-dlltool -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-cygwin64
Source2:       standard-dlls-cygwin64


BuildRequires:  cygwin32-filesystem
BuildRequires:  cygwin32-binutils
BuildRequires:  cygwin32-w32api-headers >= %{version}
BuildRequires:  cygwin32-gcc

BuildRequires:  cygwin64-filesystem
BuildRequires:  cygwin64-binutils
BuildRequires:  cygwin64-w32api-headers >= %{version}
BuildRequires:  cygwin64-gcc

BuildRequires:  make

%description
Windows cross-compiler runtime base libraries for Cygwin toolchain.

%package -n cygwin32-w32api-runtime
Summary:        Windows API libraries for Cygwin32 toolchain
Requires:       cygwin32-filesystem
Requires:       cygwin32-w32api-headers >= %{version}
Provides:       %(sed "s/\(.*\)/cygwin32(\1) /g" %{SOURCE1} | tr "\n" " ")
Provides:       cygwin32(mscoree.dll)

%description -n cygwin32-w32api-runtime
Windows cross-compiler runtime base libraries for Cygwin32 toolchain.

%package -n cygwin64-w32api-runtime
Summary:        Windows API libraries for Cygwin64 toolchain
Requires:       cygwin64-filesystem
Requires:       cygwin64-w32api-headers >= %{version}
Provides:       %(sed "s/\(.*\)/cygwin64(\1) /g" %{SOURCE2} | tr "\n" " ")
Provides:       cygwin64(mscoree.dll)

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
    # Filter out -fstack-protector and -lssp from LDFLAGS as libssp is not yet potentially built with the bootstrap gcc
    CYGWIN32_LDFLAGS="`echo %{cygwin32_ldflags} | sed 's|-fstack-protector||' | sed 's|-lssp||'`"
    CYGWIN64_LDFLAGS="`echo %{cygwin64_ldflags} | sed 's|-fstack-protector||' | sed 's|-lssp||'`"

    CYGWIN32_CONFIGURE_ARGS="--disable-lib64"
    CYGWIN64_CONFIGURE_ARGS="--disable-lib32"
    %cygwin_configure --enable-w32api
    %cygwin_make_build
popd


%install
pushd mingw-w64-crt
    %cygwin_make_install
popd

# Dunno what to do with these files
rm -fr %{buildroot}%{cygwin32_includedir}/w32api/*.c
rm -fr %{buildroot}%{cygwin64_includedir}/w32api/*.c


%files -n cygwin32-w32api-runtime
%doc COPYING DISCLAIMER DISCLAIMER.PD
%{cygwin32_libdir}/w32api/

%files -n cygwin64-w32api-runtime
%doc COPYING DISCLAIMER DISCLAIMER.PD
%{cygwin64_libdir}/w32api/


%changelog
* Thu Aug 26 2021 Yaakov Selkowitz <yselkowi@redhat.com> - 9.0.0-1
- new version

* Thu Sep 24 2020 Yaakov Selkowitz <yselkowi@redhat.com> - 8.0.0-1
- new version

* Wed Apr 01 2020 Yaakov Selkowitz <yselkowi@redhat.com> - 7.0.0-1
- new version

* Thu Dec 20 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 5.0.4-1
- new version

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
