Summary: A GNU stream text editor.
Name: sed
Version: 4.0.5
Release: 1
Copyright: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.gz
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: %{_tmppath}/%{name}-root

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q

%build

%configure
make %{_smp_mflags}

echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall

pushd ${RPM_BUILD_ROOT}

%ifos linux
mkdir -p ./bin
mv .%{_bindir}/sed ./bin/sed
rmdir .%{_bindir}
%endif

gzip -9nf .%{_infodir}/sed.info*
rm -f .%{_infodir}/dir

popd

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/sed.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/sed.info.gz %{_infodir}/dir
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS NEWS THANKS README AUTHORS TODO
%ifos linux
/bin/sed 
%else
%{_bindir}/sed
%endif
%{_infodir}/*.info*
%{_mandir}/man*/*

%changelog
* Thu Jan 23 2003 Jakub Jelinek <jakub@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt to fix x86-64 miscompilation
- run make check in %%build

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com>
- Remove stale URLs from documentation (#62519)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update to 2000.11.28 patch
- Rebuild for 7.1 tree

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Jan 18 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild with glibc 2.1.3 to fix an mmap64 bug in sys/mman.h

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
