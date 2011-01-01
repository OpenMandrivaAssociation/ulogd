Summary:	Ulogd - The userspace logging daemon for netfilter
Name:		ulogd
Version:	1.24
Release:	%mkrel 17
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.netfilter.org/projects/ulogd/
Source0:	ftp://ftp.netfilter.org/pub/ulogd/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.netfilter.org/pub/ulogd/%{name}-%{version}.tar.bz2.sig
Patch0:		ulogd-1.24-CVE-2007-0460.diff
Patch1:		ulogd-1.24-suse_db_cleanup.diff
# (fc) 1.24-3mdv fix killall path (Mdv bug #35286)
Patch2:		ulogd-1.24-fixkillall.patch
Patch3:		ulogd-build_fix.diff
Patch4:		ulogd-1.24-format_not_a_string_literal_and_no_format_arguments.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	postgresql-devel 
BuildRequires:	libpcap-devel
BuildRequires:	mysql-devel
BuildRequires:	sqlite3-devel
Requires:	userspace-ipfilter
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Ulogd-mysql is a PostgreSQL output plugin for ulogd. It enables logging of
firewall information into a PostgreSQL database.

%package	sqlite
Summary:	SQLite output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	sqlite
Ulogd-mysql is a SQLite output plugin for ulogd. It enables logging of
firewall information into a SQLite database.

%package	pcap
Summary:	PCAP output plugin for ulogd
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}

%description	pcap
Ulogd-pcap is a output plugin for ulogd that saves packet logs as PCAP file.
PCAP is a standard format that can be later analyzed by a lot of tools such as
tcpdump and ethereal.

%prep

%setup -q
%patch0 -p1 -b .cve20077460
# I've disabled this for now as I'm not 100% confident about the edits
# I made from the version on http://qa.mandriva.com/show_bug.cgi?id=28420
# This mostly relates to return values and mysql database connection 
# reconnection.
#patch1 -p1 -b .dbclean
%patch2 -p1 -b .fixkillall
%patch3 -p1
%patch4 -p0

# lib64 fix
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*

%build

%configure \
    --with-mysql=%{_libdir}/mysql \
    --with-pgsql=%{_libdir}/pgsql \
    --with-sqlite3=%{_libdir}

# lib64 fix
perl -pi -e "s|\-L/usr/lib\ |\-L%{_libdir}\ |g" Rules.make

make

%install
rm -rf %{buildroot}

%makeinstall_std

# install initscript
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
install ulogd.init %{buildroot}/%{_sysconfdir}/rc.d/init.d/ulogd

# install logrotate file
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install ulogd.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/ulogd

mkdir -p %{buildroot}/var/log/ulogd

# install man page
install -d %{buildroot}%{_mandir}/man8
install -m0644 ulogd.8 %{buildroot}%{_mandir}/man8/

gunzip contrib/ulog_query.php.gz


%post
%_post_service ulogd

%preun
%_preun_service ulogd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING AUTHORS README
%doc doc/ulogd.txt doc/ulogd.a4.ps doc/ulogd.html
%doc contrib/ulog_query.php
%attr(0755,root,root) %{_initrddir}/ulogd
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ulogd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/ulogd
%attr(0755,root,root) %{_sbindir}/ulogd
%dir %{_libdir}/ulogd
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_BASE.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_LOCAL.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_LOGEMU.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_OPRINT.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_PWSNIFF.so
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_SYSLOG.so
%dir /var/log/ulogd
%attr(0644,root,root) %{_mandir}/man8/*

%files mysql
%defattr(-,root,root)
%doc doc/mysql.table doc/mysql.table.ipaddr-as-string
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_MYSQL.so

%files pgsql
%defattr(-,root,root)
%doc doc/pgsql.table
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_PGSQL.so

%files sqlite
%defattr(-,root,root)
%doc doc/sqlite3.table
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_SQLITE3.so

%files pcap
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/ulogd/ulogd_PCAP.so
