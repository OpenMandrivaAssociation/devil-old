%define oname DevIL
%define major 1
%define libIL %mklibname IL-old %{major}
%define libILU %mklibname ILU-old %{major}
%define libILUT %mklibname ILUT-old %{major}
%define devname %mklibname %{name}-old -d

Summary:	Open source image library
Name:		devil-old
Version:	1.7.8
Release:	14
License:	LGPLv2+
Group:		System/Libraries
Url:		http://openil.sourceforge.net/
Source0:	http://downloads.sourceforge.net/openil/%{oname}-%{version}.tar.gz
Patch0:		devil-1.7.8-CVE-2009-3994.patch
Patch1:		devil-1.7.8-libpng15.patch

BuildRequires:	file
BuildRequires:	libtool
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libmng)
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(allegro)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(zlib)

%description
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package 	utils-old
Summary:	Tools provided by %{oname}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description	utils-old
This package contains tools provided by %{oname}.

%files utils-old
%{_bindir}/ilur
#-------------------------------------------------------------------------
%package -n %{libIL}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Obsoletes:	%{_lib}devil1 < %{version}-%{release}

%description -n	%{libIL}
This package contains the shared library for %{oname}.

%files -n %{libIL}
%{_libdir}/libIL.so.%{major}*
#-------------------------------------------------------------------------
%package -n %{libILU}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Conflicts:	%{_lib}devil1 < %{version}-%{release}

%description -n	%{libILU}
This package contains the shared library for %{oname}.
%files -n %{libILU}
%{_libdir}/libILU.so.%{major}*
#-------------------------------------------------------------------------
%package -n %{libILUT}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Conflicts:	%{_lib}devil1 < %{version}-%{release}

%description -n	%{libILUT}
This package contains the shared library for %{oname}.

%files -n %{libILUT}
%{_libdir}/libILUT.so.%{major}*
#-------------------------------------------------------------------------
%package -n %{devname}
Summary:	Development headers and libraries for writing programs using %{oname}
Group:		Development/C
Requires:	%{libIL} = %{version}-%{release}
Requires:	%{libILU} = %{version}-%{release}
Requires:	%{libILUT} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
%define __noautoreq 'devel\\(liballeg.*'
Obsoletes:	%{_lib}devel-static-devel = %{version}-%{release}

%description -n	%{devname}
Development headers and libraries for writing programs using %{oname}.

%files -n %{devname}
%doc AUTHORS CREDITS ChangeLog Libraries.txt README.unix
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/IL
%{_infodir}/*.info.*
#-------------------------------------------------------------------------
%prep
%setup -qn devil-%{version}
%apply_patches

chmod 644 AUTHORS CREDITS ChangeLog Libraries.txt README.unix

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# Don't second-guess compiler flags -- std=gnu99 isn't valid for C++
sed -i -e 's,-std=gnu99 ,,g' m4/devil-definitions.m4 configure
# C++ doesn't have restrict, but it has __restrict
sed -i -e 's,restrict,__restrict,g' include/IL/il.h

%build
export CFLAGS="%{optflags} -Ofast -funroll-loops -ffast-math -fomit-frame-pointer"
# using autogen.sh results in configure failing with a problem in
# ADD_CFLAGS, as of 0.7.3 - AdamW 2008/12
#autoreconf

%configure	\
	--disable-static \
	--enable-shared \
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

%make CPPFLAGS="-DNOINLINE"

%install
%makeinstall_std









