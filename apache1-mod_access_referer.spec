%define		mod_name	access_referer
%define 	apxs		%{_sbindir}/apxs
Summary:	Access control based on "Referer" HTTP header content
Summary(pl):	Kontrola dost�pu bazuj�ca na zawarto�ci standardowego nag��wka HTTP "REFERER"
Name:		apache-mod_%{mod_name}
Version:	1.0.2
Release:	6
License:	Apache Group
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/accessreferer/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	f1726cfe5965eda1bdca90b8db475377
Patch0:		http://dl.sourceforge.net/sourceforge/accessreferer/mod_access_referer_1.0.2_third_part_patch.txt
URL:		http://sourceforge.net/projects/accessreferer/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{apxs}
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an module for the Apache HTTP Server that provides access
control based on "Referer" HTTP header content.

%description -l pl
Modu� ten pozwala na kontrolowanie dost�pu do plik�w na serwerze w
zale�no�ci od zawarto�ci standardowego nag��wka HTTP - "REFERER"

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0

%build
PATH=$PATH:%{_sbindir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_pkglibdir}/*
