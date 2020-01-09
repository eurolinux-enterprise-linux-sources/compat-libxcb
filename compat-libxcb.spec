Name:           compat-libxcb
Version:        1.9
Release:        0.1%{?dist}
Summary:        A C binding to the X11 protocol

Group:          System Environment/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/libxcb-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/libxcb-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:        0001-integer-overflow-in-read_packet-CVE-2013-2064.patch
Patch2:	0001-c_client.py-Handle-multiple-expr.-in-a-bitcase.patch
Patch3: xkb.patch

BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  libXau-devel
BuildRequires:  libxslt
BuildRequires:  xcb-proto >= 1.7-3
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-util-macros

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%prep
%setup -q -n libxcb-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .jx

%build
sed -i 's/pthread-stubs //' configure.ac
autoreconf -v --i -f
%configure --disable-static --disable-build-docs --enable-xkb --enable-sync \
    --disable-{composite,damage,dpms,dri2,glx,randr,record,render} \
    --disable-{resource,screensaver,shape,shm,xevie,xfixes,xfree86-dri} \
    --disable-{xprint,xinerama,selinux,xtest,xv,xvmc,xkb}
ln -s %{_datadir}/xcb/xproto.xml .
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -delete
rm -rf $RPM_BUILD_ROOT{%{_datadir},%{_includedir},%{_libdir}/pkgconfig}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libxcb.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libxcb-sync.so.0*

%changelog
* Thu Nov 05 2015 Adam Jackson <ajax@redhat.com> 1.9-0.1
- Compatibility build for libxcb-sync.so.0
