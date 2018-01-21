%define	snap	20180121
%define	commit	793d1b8b093f382c46fb59fe6435da208802ce43

Summary:	Sample Executables for OpenZWave
Name:		openzwave
Version:	1.5.0
Release:	0.%{snap}.1
License:	LGPLv3+
Group:		Libraries
URL:		http://www.openzwave.net
Source0:	https://github.com/OpenZWave/open-zwave/archive/%{commit}.tar.gz
# Source0-md5:	fcd8fda2237693c8e93dacd954634818
# Use system tinyxml
Patch1:		%{name}-tinyxml.patch
# Use system hidapi
Patch2:		%{name}-hidapi.patch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	hidapi-devel >= 0.8.0
BuildRequires:	systemd-devel
BuildRequires:	tinyxml-devel

%description
OpenZWave is an open-source, cross-platform library designed to enable
anyone to add support for Z-Wave home-automation devices to their
applications, without requiring any in depth knowledge of the Z-Wave
protocol.

%package -n libopenzwave
Summary:	Library to access Z-Wave interfaces

%description -n libopenzwave
OpenZWave is an open-source, cross-platform library designed to enable
anyone to add support for Z-Wave home-automation devices to their
applications, without requiring any in depth knowledge of the Z-Wave
protocol.

%package -n libopenzwave-devel
Summary:	Open-ZWave header files
Requires:	libopenzwave = %{version}-%{release}

%description -n libopenzwave-devel
Header files needed when you want to compile your own applications
using openzwave

%prep
%setup -q -n open-zwave-%{commit}
%patch1 -p1 -b.tinyxml
%patch2 -p1 -b.hidapi

%build
major_ver=$(echo %{version} | awk -F \. {'print $1'})
minor_ver=$(echo %{version} | awk -F \. {'print $2'})
revision=$(echo %{version} | awk -F \. {'print $3'})

CPPFLAGS="%{rpmcppflags} -Wformat -DOPENZWAVE_ENABLE_EXCEPTIONS" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags} -pthread" \
	VERSION_MAJ=$major_ver \
	VERSION_MIN=$minor_ver \
	VERSION_REV=$revision \
	PREFIX=%{_prefix} \
	sysconfdir=%{_sysconfdir}/openzwave/ \
	includedir=%{_includedir} \
	docdir=%{_defaultdocdir}/openzwave-%{version} \
	instlibdir=%{_libdir} \
	%{__make}

%install
rm -rf $RPM_BUILD_ROOT
major_ver=$(echo %{version} | awk -F \. {'print $1'})
minor_ver=$(echo %{version} | awk -F \. {'print $2'})
revision=$(echo %{version} | awk -F \. {'print $3'})

install -d $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_libdir}
install -d $RPM_BUILD_ROOT/%{_docdir}/openzwave-%{version}/
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/
install -d $RPM_BUILD_ROOT/%{_includedir}/openzwave/

DESTDIR=$RPM_BUILD_ROOT \
	VERSION_MAJ=$major_ver \
	VERSION_MIN=$minor_ver \
	VERSION_REV=$revision \
	PREFIX=%{_prefix} \
	sysconfdir=%{_sysconfdir}/openzwave/ \
	includedir=%{_includedir}/openzwave/ \
	docdir=%{_docdir}/openzwave-%{version} \
	instlibdir=%{_libdir} \
	%{__make} install

rm $RPM_BUILD_ROOT%{_docdir}/openzwave-%{version}/Doxyfile.in
rm -rf $RPM_BUILD_ROOT%{_docdir}/openzwave-%{version}/html/
rm -rf $RPM_BUILD_ROOT%{_docdir}/openzwave-%{version}/default.htm
rm -rf $RPM_BUILD_ROOT%{_docdir}/openzwave-%{version}/general/
rm -rf $RPM_BUILD_ROOT%{_docdir}/openzwave-%{version}/images+css/
rm -rf $RPM_BUILD_ROOT%{_docdir}/openzwave-%{version}/api/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libopenzwave -p /sbin/ldconfig
%postun -n libopenzwave -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/MinOZW

%files -n libopenzwave
%defattr(644,root,root,755)
%doc license/*.txt
%doc docs/default.htm docs/general/ docs/images+css/
%{_libdir}/libopenzwave.so.*
%dir %{_sysconfdir}/openzwave/
%config(noreplace) %{_sysconfdir}/openzwave/*

%files -n libopenzwave-devel
%defattr(644,root,root,755)
%doc docs/api
%attr(755,root,root) %{_bindir}/ozw_config
%{_includedir}/openzwave/
%{_libdir}/libopenzwave.so
%{_pkgconfigdir}/libopenzwave.pc
