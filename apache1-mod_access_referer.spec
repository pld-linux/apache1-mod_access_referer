%define		mod_name	access_referer
%define 	apxs		/usr/sbin/apxs
Summary:	Access control based on "Referer" HTTP header content
Summary(pl):	Kontrola dostêpu bazuj±ca na zawarto¶ci standardowego nag³ówka HTTP "REFERER"
Name:		apache-mod_%{mod_name}
Version:	1.0.2
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(cs):	Sí»ové/Démoni
Group(da):	Netværks/Dæmoner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	Réseau/Serveurs
Group(is):	Net/Púkar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	óÅÔØ/äÅÍÏÎÙ
Group(sl):	Omre¾ni/Stre¾niki
Group(sv):	Nätverk/Demoner
Group(uk):	íÅÒÅÖÁ/äÅÍÏÎÉ
Source0:	http://prdownloads.sourceforge.net/accessreferer/mod_%{mod_name}-%{version}.tar.gz
URL:		http://sourceforge.net/projects/accessreferer/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an module for the Apache HTTP Server that provides access
control based on "Referer" HTTP header content.

%description -l pl
Modu³ ten pozwala na kontrolowanie dostêpu do plików na serwerze w
zale¿no¶ci od zawarto¶ci standardowego nag³ówka HTTP - "REFERER"

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

gzip -9nf README ChangeLog

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
%{_sbindir}/apxsks -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_pkglibdir}/*
