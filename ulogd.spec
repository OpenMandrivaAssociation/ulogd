Summary:	The userspace logging daemon for netfilter
Name:		ulogd
Version:	2.0.2
Release:	1
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.netfilter.org/projects/ulogd/
Source0:	ftp://ftp.netfilter.org/pub/ulogd/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.netfilter.org/pub/ulogd/%{name}-%{version}.tar.bz2.sig
Source2:	ulogd.service
# (fc) 1.24-3mdv fix killall path (Mdv bug #35286)
Patch0:		ulogd-1.24-fixkillall.patch
Patch1:		ulogd-build_fix.diff
Patch2:		omv-ulogd-2.0.2-conf.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	autoconf automake libtool
BuildRequires:	dbi-devel
BuildRequires:	pcap-devel
BuildRequires:	linuxdoc-tools texlive
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(libnetfilter_acct)
BuildRequires:	pkgconfig(libnetfilter_conntrack)
BuildRequires:	pkgconfig(libnetfilter_log)
BuildRequires:	pkgconfig(libnfnetlink)
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	linuxdoc-tools
Requires:	userspace-ipfilter

%description
Ulogd is an universal logging daemon for the ULOG target of netfilter, the
Linux 2.4/2.6 firewalling subsystem. Ulogd is able to log packets in various
formats to different targets (text files, databases, etc.). It has an
easy-to-use plugin interface to add new protocols and new output targets.

%package	mysql
Summary:	MySQL output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	mysql
Ulogd-mysql is a MySQL output plugin for ulogd. It enables logging of
firewall information into a MySQL database.

%package	pgsql
Summary:	PostgreSQL output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	pgsql
Ulogd-pgsql is a PostgreSQL output plugin for ulogd. It enables logging of
firewall information into a PostgreSQL database.

%package	sqlite
Summary:	SQLite output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	sqlite
Ulogd-sqlite is a SQLite output plugin for ulogd. It enables logging of
firewall information into a SQLite database.

%package	pcap
Summary:	PCAP output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	pcap
Ulogd-pcap is a output plugin for ulogd that saves packet logs as PCAP file.
PCAP is a standard format that can be later analyzed by a lot of tools such as
tcpdump and wireshark.

%package	dbi
Summary:	Libdbi framework output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	dbi
Ulogd-dbi is a libdbi output plugin for ulogd. It enables logging of
firewall information through a libdbi interface.

%prep

%setup -q
%patch0 -p1 -b .fixkillall
%patch1 -p1
%patch2 -p1

# lib64 fix
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*

cp %{SOURCE2} ulogd.service

%build
autoreconf -fi
%serverbuild

%configure2_5x \
    --disable-static \
    --enable-shared \
    --with-pgsql=%{_prefix} \
    --with-pgsql-inc=%{_includedir}/postgresql \
    --with-mysql=%{_prefix} \
    --with-mysql-inc=%{_includedir}/mysql \
    --with-dbi=%{_prefix} \
    --with-dbi-lib=%{_libdir} \
    --with-dbi-inc=%{_includedir} \

# bork...
cat >> config.h << EOF
#define HAVE_LIBDBI 1
#define HAVE_LIBMYSQLCLIENT 1
#define HAVE_LIBPQ 1
EOF

%make
make -C doc

%install

%makeinstall_std

# install initscript
install -d %{buildroot}%{_unitdir}
install -m0755 ulogd.service %{buildroot}%{_unitdir}/ulogd.service

# install logrotate file
install -d %{buildroot}/%{_sysconfdir}/logrotate.d
install ulogd.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/ulogd

install -d %{buildroot}/var/lib/ulogd
install -d %{buildroot}/var/log/ulogd

# install man page
install -d %{buildroot}%{_mandir}/man8
install -m0644 ulogd.8 %{buildroot}%{_mandir}/man8/

install -m0644 ulogd.conf %{buildroot}%{_sysconfdir}/

rm -f %{buildroot}%{_libdir}/ulogd/*.*a

%post
%_post_service ulogd

%preun
%_preun_service ulogd

%files
%doc COPYING AUTHORS README
%doc doc/ulogd.txt
%doc doc/ulogd.html
%doc doc/mysql-ulogd2-flat.sql
%doc doc/mysql-ulogd2.sql
%doc doc/pgsql-ulogd2-flat.sql
%doc doc/pgsql-ulogd2.sql
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ulogd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/ulogd
%attr(0755,root,root) %{_sbindir}/ulogd
%{_unitdir}/ulogd.service
%dir %{_libdir}/ulogd
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_HWHDR.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_IFINDEX.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_IP2BIN.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_IP2HBIN.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_IP2STR.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_MARK.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_PRINTFLOW.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_PRINTPKT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_filter_PWSNIFF.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_inpflow_NFACCT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_inpflow_NFCT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_inppkt_NFLOG.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_inppkt_ULOG.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_inppkt_UNIXSOCK.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_GPRINT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_LOGEMU.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_NACCT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_OPRINT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_SYSLOG.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_GRAPHITE.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_XML.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_raw2packet_BASE.so
%dir /var/lib/ulogd
%dir /var/log/ulogd
%attr(0644,root,root) %{_mandir}/man8/*

%files mysql
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_MYSQL.so

%files pgsql
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_PGSQL.so

%files sqlite
%doc doc/sqlite3.table
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_SQLITE3.so

%files pcap
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_PCAP.so

%files dbi
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_output_DBI.so
