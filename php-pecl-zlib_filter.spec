%define		_modname	zlib_filter
%define		_status		stable

Summary:	%{_modname} - zlib filter implementation backport for PHP 5.0
Summary(pl):	%{_modname} - backport implementacji filtra zlib dla PHP 5.0
Name:		php-pecl-%{_modname}
Version:	1.1
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1ebb48e3fd1be4593a4eb217fbc1ab53
URL:		http://pecl.php.net/package/zlib_filter/
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
RFC 1951 inflate/deflate stream filter implementation. Performs inline
compression/decompression using the deflate method on any PHP I/O
stream. The data produced by this filter, while compatable with the
payload portion of an RFC 1952 gzip file, does not include headers or
tailers for full RFC 1952 gzip compatability. To achieve this format,
use the compress.zlib:// fopen wrapper built directly into PHP.

In PECL status of this extension is: %{_status}.

#%description -l pl
#
#To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-zlib-filter=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
