%define		mod_name	access_referer
%define 	apxs		%{_sbindir}/apxs1
Summary:	Access control based on "Referer" HTTP header content
Summary(pl.UTF-8):	Kontrola dostępu bazująca na zawartości standardowego nagłówka HTTP "REFERER"
Name:		apache1-mod_%{mod_name}
Version:	1.0.2
Release:	4
License:	Apache Group
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/accessreferer/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	f1726cfe5965eda1bdca90b8db475377
Patch0:		http://dl.sourceforge.net/accessreferer/mod_access_referer_1.0.2_third_part_patch.txt
URL:		http://sourceforge.net/projects/accessreferer/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_access_referer <= 1.0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an module for the Apache HTTP Server that provides access
control based on "Referer" HTTP header content.

%description -l pl.UTF-8
Moduł ten pozwala na kontrolowanie dostępu do plików na serwerze w
zależności od zawartości standardowego nagłówka HTTP - "REFERER"

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}
install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- %{name} < 1.0.2-2.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog HACKING *.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
