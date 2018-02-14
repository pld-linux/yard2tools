#
# Conditional build:
%bcond_without	lirc	# LIRC driver
#
Summary:	Infra-red remote control support for Y.A.R.D.2 hardware
Summary(pl.UTF-8):	Obsługa pilotów na podczerwień Y.A.R.D.2
Name:		yard2tools
Version:	1.2.5
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://launchpad.net/~yard2team/+archive/ubuntu/test/+files/%{name}_%{version}.orig.tar.gz
# Source0-md5:	91427839a1aad9bab65a163b1cbec951
# from git://git.assembla.com/yard2srvd.git (master on 20171026)
Patch0:		%{name}-lircd_094.patch
Patch1:		%{name}-lirc.patch
URL:		https://app.assembla.com/spaces/yard2srvd/git/source
BuildRequires:	libbsd-devel
BuildRequires:	libusb-compat-devel
%{?with_lirc:BuildRequires:	lirc-devel >= 0.9.4}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the daemon and some utilities to support
infra-red remote controls with the Y.A.R.D.2 type of hardware under
Linux.

%description -l pl.UTF-8
Ten pakiet zawiera demona i narzędzia do obsługi pilotów na
podczerwień typu Y.A.R.D.2 pod Linuksem.

%package vdr
Summary:	Infra-red remote control support for Y.A.R.D.2 hardware in VDR
Summary(pl.UTF-8):	Obsługa pilotów na podczerwień Y.A.R.D.2 w programie VDR
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	vdr

%description vdr
Infra-red remote control support for Y.A.R.D.2 hardware in VDR.

%description vdr -l pl.UTF-8
Obsługa pilotów na podczerwień Y.A.R.D.2 w programie VDR.

%package -n lirc-plugin-yard2
Summary:	Y.A.R.D.2 driver for LIRC
Summary(pl.UTF-8):	Sterownik do sprzętu Y.A.R.D.2 dla LIRC-a
Group:		Libraries
Requires:	lirc >= 0.9.4

%description -n lirc-plugin-yard2
Y.A.R.D.2 driver for LIRC.

%description -n lirc-plugin-yard2 -l pl.UTF-8
Sterownik do sprzętu Y.A.R.D.2 dla LIRC-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__rm} inih/extra/*.a

%build
%configure
%{__make}

%if %{with lirc}
%{__make} -C lirc/lircd_094 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with lirc}
%{__make} -C lirc/lircd_094 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Readme.txt ChangeLog 
%attr(755,root,root) %{_bindir}/lirctest
%attr(755,root,root) %{_bindir}/yard2config
%attr(755,root,root) %{_bindir}/yard2flash
%attr(755,root,root) %{_bindir}/yard2lcdtest
%attr(755,root,root) %{_bindir}/yard2record
%attr(755,root,root) %{_bindir}/yard2srvd
%attr(755,root,root) %{_bindir}/yard2wakeup
%dir %{_sysconfdir}/yard2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yard2/yard2tools.cfg
%{systemdunitdir}/yard2.service
/lib/udev/rules.d/60-usb-yard2.rules

%files vdr
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vdr/vdr-addon-yard2wakeup.conf
%dir %{_datadir}/vdr
%dir %{_datadir}/vdr/shutdown-hooks
%{_datadir}/vdr/shutdown-hooks/S90.yard2-wakeup

%if %{with lirc}
%files -n lirc-plugin-yard2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lirc/plugins/yard2.so
%{_datadir}/lirc/configs/yard2.conf
%endif
