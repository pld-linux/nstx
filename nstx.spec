# TODO
# - nstxd system user
%define		subver	beta6
%define		rel		0.1
Summary:	Nameserver Transfer Protocol
Name:		nstx
Version:	1.1
Release:	0.%{subver}.%{rel}
License:	GPL
Group:		Networking
URL:		http://nstx.dereference.de/nstx/
Source0:	http://nstx.dereference.de/nstx/%{name}-%{version}-%{subver}.tar.bz2
# Source0-md5:	da6af7010de63590cc3000541ec5074f
Source1:	http://ftp.debian.org/debian/pool/main/n/nstx/%{name}_%{version}-%{subver}-5.diff.gz
# Source1-md5:	0b7b4d4d3added258ff61b1c5357a1b9
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Source4:	%{name}cd.init
Source5:	%{name}cd.sysconfig
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NSTX (the Nameserver Transfer Protocol) makes it possible to create IP
tunnels using DNS queries and replies for IP packet encapsulation
where IP traffic other than DNS isn't possible.

%package -n nstxcd
Summary:	Nstx (Tunnel IP over DNS)
Group:		Networking
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description -n nstxcd
The nstx client.

%prep
%setup -q -n %{name}-%{version}-%{subver}
%{__gzip} -dc %{SOURCE1} | %{__patch} %{S:0} -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/{rc.d/init.d,sysconfig}}
install -p nstxd nstxcd $RPM_BUILD_ROOT%{_sbindir}
cp -a *.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}d
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}cd
cp -a %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add nstxd
%service nstxd restart

%preun
if [ "$1" = "0" ]; then
	%service -q nstxd stop
	/sbin/chkconfig --del nstxd
fi

%post -n nstxcd
/sbin/chkconfig --add nstxcd
%service nstxcd restart

%preun -n nstxcd
if [ "$1" = "0" ]; then
	%service -q nstxcd stop
	/sbin/chkconfig --del nstxcd
fi

%files
%defattr(644,root,root,755)
%doc README Changelog
%attr(755,root,root) %{_sbindir}/nstxd
%{_mandir}/man8/nstxd.8*
%{_sysconfdir}/%{name}/nstxd.*
%attr(754,root,root) /etc/rc.d/init.d/nstxd

%files -n nstxcd
%defattr(644,root,root,755)
%doc README Changelog
%attr(755,root,root) %{_sbindir}/nstxcd
%{_mandir}/man8/nstxcd.8*
%{_sysconfdir}/%{name}/nstxcd.*
%attr(754,root,root) /etc/rc.d/init.d/nstxcd
