Summary:	Sample Executables for OpenZWave
Name:		openzwave
Version:	1.6.1133
Release:	1
License:	LGPLv3+
Group:		Libraries
URL:		http://www.openzwave.net
#Source0:	https://github.com/OpenZWave/open-zwave/archive/%{version}.tar.gz
Source0:	http://old.openzwave.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	c9fd07d9d5bb971d97537e25ca5e73ce
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
%setup -q

%build
major_ver=$(echo %{version} | awk -F \. {'print $1'})
minor_ver=$(echo %{version} | awk -F \. {'print $2'})
revision=$(echo %{version} | awk -F \. {'print $3'})

CPPFLAGS="%{rpmcppflags} -Wformat -DOPENZWAVE_ENABLE_EXCEPTIONS" \
	USE_HID=1 \
	USE_BI_TXML=0 \
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
	USE_HID=1 \
	USE_BI_TXML=0 \
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
%doc licenses/license.txt
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
