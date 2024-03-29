%define tarname xorg-docs

Summary: X.Org X11 documentation
Name: xorg-x11-docs
Version: 1.3
Release: 6.1%{?dist}
License: MIT
Group: Documentation
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

Source0: ftp://ftp.x.org/pub/individual/doc/%{tarname}-%{version}.tar.bz2
Patch0: docs-1.3-registry.patch

BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: xorg-sgml-doctools >= 1.1.1
BuildRequires: xorg-x11-util-macros
BuildRequires: ghostscript

Obsoletes: XFree86-doc, xorg-x11-doc

Provides: XFree86-doc, xorg-x11-doc

%define x11docdir %{_datadir}/doc/xorg-x11-docs-%{version}-%{release}

%description
Protocol and other technical documentation for the X.Org X11 X Window System
implementation.

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p1 -b .registry

%build
autoreconf -v --install || exit 1
%configure --with-x11docdir=%{x11docdir}
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/Xprint.7*

pushd $RPM_BUILD_ROOT%{x11docdir}

rm -rf hardcopy/XPRINT
rm -f hardcopy/Xserver/Xprt.PS.gz
find . -name '*.gz' | xargs gunzip
find . -name '*.PS' | while read f ; do
    mv $f $(dirname $f)/$(basename $f .PS).ps
    echo $(dirname $f) $(basename $f .PS).ps
done | while read d f ; do
    pushd $d
    ps2pdf14 $f
    rm $f
    popd
done

popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{x11docdir}
%{_mandir}/man7/Consortium.7*
%{_mandir}/man7/Standards.7*
%{_mandir}/man7/X.7*
%{_mandir}/man7/XOrgFoundation.7*
%{_mandir}/man7/XProjectTeam.7*
%{_mandir}/man7/security.7*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3-6.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Adam Jackson <ajax@redhat.com> 1.3-4
- Fix %%x11docdir to match %%name. (#484734)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.3-3
- Fix license tag.

* Tue Dec 25 2007 Adam Jackson <ajax@redhat.com> 1.3-2
- Install PDF instead of gzipped PostScript.
- Move everything to /usr/share/doc to be more like other doc packages.
- Add 'registry' to the doc set.

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 1.3-1
- Update to 1.3

* Tue Jul 25 2006 Mike A. Harris <mharris@redhat.com> 1.2-4.fc6
- Fix the package summary/description.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.2-3.fc6
- Added "Provides: XFree86-doc, xorg-x11-doc" as per request in (#199927)

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.2-2.fc6
- Change rpm Group to "Documentation", which is what other docs packages use.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.2-1.fc6
- Initial build.
