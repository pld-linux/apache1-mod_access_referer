%define		mod_name	access_referer
%define 	apxs		%{_sbindir}/apxs1
Summary:	Access control based on "Referer" HTTP header content
Summary(pl):	Kontrola dostêpu bazuj±ca na zawarto¶ci standardowego nag³ówka HTTP "REFERER"
Name:		apache1-mod_%{mod_name}
Version:	1.0.2
Release:	2.8
License:	Apache Group
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/accessreferer/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	f1726cfe5965eda1bdca90b8db475377
Patch0:		http://dl.sourceforge.net/sourceforge/accessreferer/mod_access_referer_1.0.2_third_part_patch.txt
URL:		http://sourceforge.net/projects/accessreferer/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
Requires(triggerpostun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an module for the Apache HTTP Server that provides access
control based on "Referer" HTTP header content.

%description -l pl
Modu³ ten pozwala na kontrolowanie dostêpu do plików na serwerze w
zale¿no¶ci od zawarto¶ci standardowego nag³ówka HTTP - "REFERER"

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

CFG=$RPM_BUILD_ROOT%{_sysconfdir}/conf.d
echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > $CFG/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%triggerpostun -- %{name} < 1.0.2-2.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog HACKING *.html
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
