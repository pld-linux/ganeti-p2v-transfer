Summary:	Tool for converting a physical computer into a Ganeti instance
Name:		ganeti-p2v-transfer
Version:	0.1
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	https://ganeti.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	c0333098304fa1868ffcaa82a942eba0
Patch0:		DESTDIR.patch
URL:		https://code.google.com/p/ganeti/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docutils
BuildRequires:	rpmbuild(macros) >= 1.647
Requires:	ganeti
Requires:	mawk
Requires:	tar
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a tool for converting a physical computer into a ganeti
instance. It consists of two parts, a ganeti instance OS template that
allows the instance to be booted to receive the files, and a script
that is run on the source machine to make the transfer.

A design document is available in doc/design.rst that describes the
functioning of the system. This document will focus on getting the
system up and running, and the process for actually performing
physical-to-virtual transfers.

%package source
Summary:	Source system transfer script.
Group:		Applications/System

%description source
This script is run from the transfer OS to establish an SSH connection
with the bootstrap OS, mount the source filesystem(s), and copy
the data over to the target. It will prompt the user for credentials
as necessary to gain access to the bootstrap OS.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-source install-target \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT/%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README* doc/design.* doc/instance-p2v-target.*
%dir %{_sysconfdir}/ganeti/instance-p2v-target
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ganeti/instance-p2v-target/p2v-target.conf
%dir %{_sysconfdir}/ganeti/instance-p2v-target/fixes
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/fixes/10_fix_fstab
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/fixes/20_remove_persistent_rules
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/fixes/30_add_console_inittab
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/fixes/30_add_console_upstart
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/fixes/40_copy_hostname
%dir %{_sysconfdir}/ganeti/instance-p2v-target/fixes/fixlib
%{_sysconfdir}/ganeti/instance-p2v-target/fixes/fixlib/*.py*
%dir %{_sysconfdir}/ganeti/instance-p2v-target/hooks
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/hooks/clear-root-password
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/hooks/install-fixes
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/hooks/interfaces
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/hooks/ramboot
%attr(755,root,root) %{_sysconfdir}/ganeti/instance-p2v-target/hooks/xen-hvc0
%dir %{_sysconfdir}/ganeti/instance-p2v-target/variants
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ganeti/instance-p2v-target/variants/default.conf
%dir %{_datadir}/ganeti/os/p2v-target
%{_datadir}/ganeti/os/p2v-target/common.sh
%attr(755,root,root) %{_datadir}/ganeti/os/p2v-target/create
%attr(755,root,root) %{_datadir}/ganeti/os/p2v-target/export
%{_datadir}/ganeti/os/p2v-target/ganeti_api_version
%attr(755,root,root) %{_datadir}/ganeti/os/p2v-target/import
%attr(755,root,root) %{_datadir}/ganeti/os/p2v-target/rename
%{_datadir}/ganeti/os/p2v-target/variants.list
%attr(755,root,root) %{_sbindir}/make_ramboot_initrd.py

%files source
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/p2v_transfer.py
