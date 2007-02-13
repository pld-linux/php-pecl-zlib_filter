%define		_modname	zlib_filter
%define		_status		stable
Summary:	%{_modname} - zlib filter implementation backport for PHP 5.0
Summary(pl.UTF-8):	%{_modname} - backport implementacji filtra zlib dla PHP 5.0
Name:		php-pecl-%{_modname}
Version:	1.1
Release:	6
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1ebb48e3fd1be4593a4eb217fbc1ab53
URL:		http://pecl.php.net/package/zlib_filter/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
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

%description -l pl.UTF-8
Implementacja filtra strumienia inflate/deflate zgodna z RFC 1951.
Wykonuje kompresję/dekompresję metodą deflate na dowolnym strumieniu
I/O PHP. Dane stworzone przez ten filtr, będąc kompatybilnymi z
częścią RFC 1952 dotyczącą payloadu pliku gzip, nie zawierają
nagłówków ani końcówek dla pełnej zgodności z gzipem według RFC 1952.
Aby uzyskać ten format, trzeba użyć wrappera fopen compress.zlib://
wbudowanego bezpośrednio w PHP.

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
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
