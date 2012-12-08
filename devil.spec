##%define _disable_ld_no_undefined	1

%define	oname DevIL

%define	major 1
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d
%define	staticname	%mklibname %{name} -s -d

Summary:	Open source image library
Name:		devil
Version:	1.7.8
Release:	%mkrel 5
License:	LGPLv2+
Group:		System/Libraries
URL:		http://openil.sourceforge.net/
Source0:	http://downloads.sourceforge.net/openil/%{oname}-%{version}.tar.gz
Patch0:		devil-1.7.8-CVE-2009-3994.patch
Patch1:		devil-1.7.8-libpng15.patch
BuildRequires:	zlib-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	SDL-devel
BuildRequires:	png-devel
BuildRequires:	lcms-devel
BuildRequires:	mng-devel
BuildRequires:	mesaglu-devel
BuildRequires:	allegro-devel
BuildRequires:	ungif-devel
BuildRequires:	libtool
BuildRequires:	jasper-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	file

%description
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package -n %{libname}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Provides:	lib%{name}
Provides:	%{name}

%description -n	%{libname}
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package -n %{develname}
Summary:	Development headers and libraries for writing programs using %{oname}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	allegro-devel
%if %{mdvver} >= 201200
%define __noautoreq 'devel\\(liballeg.*'
%else
%define	_requires_exceptions	devel(liballeg.*
%endif
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}devil1-devel

%description -n	%{develname}
Development headers and libraries for writing programs using %{oname}.

%package -n %{staticname}
Summary:	Static library for %{oname}
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{_lib}devil1-static-devel

%description -n %{staticname}
Static library for %{oname}.

%package 	utils
Summary:	Tools provided by %{oname}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-utils = %{version}-%{release}

%description	utils
This package contains tools provided by %{oname}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

chmod 644 AUTHORS CREDITS ChangeLog Libraries.txt README.unix

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
export CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math -fomit-frame-pointer -fexpensive-optimizations"
# using autogen.sh results in configure failing with a problem in
# ADD_CFLAGS, as of 0.7.3 - AdamW 2008/12
#autoreconf

%configure2_5x	\
	--enable-shared \
	--enable-static \
	--enable-IL \
	--enable-ILU \
	--enable-ILUT \
	%ifnarch ix86
	--enable-x86_64 \
	--enable-sse \
	--enable-sse2 \
	--disable-sse3 \
	%else
	--enable-x86 \
	--disable-x86_64
	--disable-sse \
	--disable-sse2 \
	--disable-sse3 \
	%endif
	--with-x \
	--with-zlib=yes \
	--enable-release

%make

%install
%__rm -rf %{buildroot}
%makeinstall_std

%clean
%__rm -rf %{buildroot}

%files -n %{libname}
%doc AUTHORS CREDITS ChangeLog Libraries.txt README.unix
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/IL
%{_infodir}/*.info.*

%files -n %{staticname}
%{_libdir}/*.a

%files utils
%{_bindir}/ilur


%changelog
* Sun Mar 25 2012 Andrey Bondrov <abondrov@mandriva.org> 1.7.8-5mdv2012.0
+ Revision: 786678
- Rebuild to deal with .la files issue, add patches for CVE-2009-3994 and libpng15 issues

* Fri Dec 17 2010 Funda Wang <fwang@mandriva.org> 1.7.8-4mdv2011.0
+ Revision: 622469
- rebuild for new directfb

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.8-3mdv2011.0
+ Revision: 610239
- rebuild

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 1.7.8-2mdv2010.0
+ Revision: 419751
- rebuild for new libjpeg v7

* Tue Jul 28 2009 Emmanuel Andry <eandry@mandriva.org> 1.7.8-1mdv2010.0
+ Revision: 402804
- New version 1.7.8
- new package devil-utils

* Sat Mar 07 2009 Emmanuel Andry <eandry@mandriva.org> 1.7.7-1mdv2009.1
+ Revision: 351816
- New version 1.7.7
- BR OpenEXR-devel
- update files list

* Wed Mar 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.5-3mdv2009.1
+ Revision: 348589
- fix static devel package dependencies

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.5-2mdv2009.1
+ Revision: 348165
- rebuild

* Mon Jan 26 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.7.5-1mdv2009.1
+ Revision: 333804
- allegro libraries are now compiled with -fPIC for x86_64, this should fix compiling of devil libraries
- tune up configure options

  + Emmanuel Andry <eandry@mandriva.org>
    - drop P1 and P3, files to patch are not present anymore

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 1.7.3-2mdv2009.1
+ Revision: 319214
- fix obsoletes

* Sun Dec 14 2008 Adam Williamson <awilliamson@mandriva.org> 1.7.3-1mdv2009.1
+ Revision: 314091
- add headers.patch to fix a couple of header locations
- and, ok, no_undefined is needed...
- turns out we now need a configure flag to get ILU and ILUT built
- use autoreconf not autogen.sh (it doesn't work right)
- add void.patch: fix inappropriate use of typedef void as a function argument
  (breaks compilation of anything that builds against devil)
- rediff underlinking.patch
- new release 1.7.3
- small cleanups
- no need to disable no_undefined

* Mon Nov 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7.2-2mdv2009.1
+ Revision: 301687
- use _disable_ld_no_undefined due to internal linking problems
- fix build
- rebuilt against new libxcb

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.7.2
    - fix license

* Tue Sep 02 2008 Emmanuel Andry <eandry@mandriva.org> 1.7.1-2mdv2009.0
+ Revision: 278748
- obsolete old devel package

* Wed Aug 27 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.7.1-1mdv2009.0
+ Revision: 276604
- update to new version 1.7.1
- Patch1: rediff
- drop patches 0,2,3,4 fixed upstream
- disable sse optimizations on ix86
- spec file clean

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.6.7-15mdv2008.1
+ Revision: 170796
- rebuild

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 1.6.7-14mdv2008.1
+ Revision: 144830
- fix headers with recent gcc (header-void.patch from debian)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix autoconf-2.5x path

* Sat May 26 2007 Funda Wang <fwang@mandriva.org> 1.6.7-13mdv2008.0
+ Revision: 31422
- Rebuild for directfb 1.0


* Fri Jan 19 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.6.7-12mdv2007.0
+ Revision: 110733
- fix bogus dependency on devel(liballeg* for lib64 too

* Fri Jan 19 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.6.7-11mdv2007.1
+ Revision: 110640
- add buildrequires on libtool
- use our own libtool, this will avoid rpath & linking issues

* Fri Jan 19 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.6.7-9mdv2007.1
+ Revision: 110587
- fix binary-or-shlib-defines-rpath
- add debian fixes for png on x86_64, endianness fixes, header fixes etc. (P0)
  fix linking against libungif (P1)
  fix linking against allegro (P2, from fedora)
  more header fiexes (P3, from fedora)
- fix building of shared libIL library on 64 bit

* Mon Dec 04 2006 Olivier Blin <oblin@mandriva.com> 1.6.7-8mdv2007.1
+ Revision: 90559
- remove hardcoded mkrel definition
- Import devil

* Fri Apr 07 2006 Lenny Cartier <lenny@mandriva.com> 1.6.7-7mdk
- use -enable-static

* Wed Mar 22 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.6.7-6mdk
- add package for static libraries

* Fri Sep 23 2005 Guillaume Bedot <littletux@mandriva.org> 1.6.7-5mdk
- rebuild with allegro-4.2.0

* Fri Aug 19 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.6.7-4mdk
- rebuild against new allegro

* Sat Apr 16 2005 Guillaume Bedot <littletux@mandriva.org> 1.6.7-3mdk
- make it easy to build with allegro or allegro-testing.
- rebuilt with allegro-testing.
- use mkrel.

* Wed Feb 16 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6.7-2mdk
- fix buildrequires

* Mon Jan 03 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6.7-1mdk
- 1.6.7
- drop P0 & P1
- compile with -O3

