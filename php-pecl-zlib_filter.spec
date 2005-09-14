%define		_modname	zlib_filter
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - zlib filter implementation backport for PHP 5.0
Summary(pl):	%{_modname} - backport implementacji filtra zlib dla PHP 5.0
Name:		php-pecl-%{_modname}
Version:	1.1
Release:	1.1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1ebb48e3fd1be4593a4eb217fbc1ab53
URL:		http://pecl.php.net/package/zlib_filter/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RFC 1951 inflate/deflate stream filter implementation. Performs inline
compression/decompression using the deflate method on any PHP I/O
stream. The data produced by this filter, while compatable with the
payload portion of an RFC 1952 gzip file, does not include headers or
tailers for full RFC 1952 gzip compatability. To achieve this format,
use the compress.zlib:// fopen wrapper built directly into PHP.

In PECL status of this extension is: %{_status}.

%description -l pl
Implementacja filtra strumienia inflate/deflate zgodna z RFC 1951.
Wykonuje kompresjê/dekompresjê metod± deflate na dowolnym strumieniu
I/O PHP. Dane stworzone przez ten filtr, bêd±c kompatybilnymi z
czê¶ci± RFC 1952 dotycz±c± payloadu pliku gzip, nie zawieraj±
nag³ówków ani koñcówek dla pe³nej zgodno¶ci z gzipem wed³ug RFC 1952.
Aby uzyskaæ ten format, trzeba u¿yæ wrappera fopen compress.zlib://
wbudowanego bezpo¶rednio w PHP.

To rozszerzenie ma w PECL status: %{_status}.

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
