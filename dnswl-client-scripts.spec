Name:		dnswl-client-scripts
Version:	0.1.1
Release:	%mkrel 3
Summary:	DNSWL client scripts
License:	GPL
Group:		Networking/Mail
URL:		https://www.dnswl.org
Source:		http://downloads.sourceforge.net/dnswl/%{name}-%{version}.tar.gz
Source1:	http://www.dnswl.org/pubkey.asc
Source2:	dnswl.cron
Patch:		dnswl-client-scripts.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
Requires(pre):	rpm-helper
Requires(post):	gnupg
Requires:	gnupg

%description
This set of files can be used to retrieve dnswl.org data via rsync
for rbldnsd and/or postfix.  To make it work you should ensure
user dnswl has write access to:
/etc/postfix/postfix-dnswl-header
/etc/postfix/postfix-dnswl-permit
and/or
/var/lib/rbldnsd/dnswl/rbldnsd-dnswl

%prep
%setup -q -n %{name}-%{version}
%patch -p1 -b .orig
cp %{SOURCE1} .

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/cron.daily
mkdir -p %{buildroot}/usr/share/dnswl
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/var/cache/dnswl
cp dnswl.conf %{buildroot}/etc/
install dnswl.sh %{buildroot}/usr/bin
install *.pl %{buildroot}/usr/share/dnswl/
install %{SOURCE1} %{buildroot}/usr/share/dnswl/
install %{SOURCE2} %{buildroot}/etc/cron.daily/dnswl

%pre
%_pre_useradd dnswl /var/cache/dnswl /bin/sh

%post
su - dnswl -c "gpg --import /usr/share/dnswl/pubkey.asc"

%postun
%_postun_userdel dnswl /var/cache/dnswl /bin/sh

%clean 
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc pubkey.asc CHANGELOG INSTALL README.postfix
/etc/cron.daily/dnswl
%config(noreplace) /etc/dnswl.conf
%{_bindir}/dnswl.sh
/usr/share/dnswl
%attr(-,dnswl,dnswl) /var/cache/dnswl

