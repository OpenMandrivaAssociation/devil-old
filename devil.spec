%define	oname DevIL

%define major 1
%define	libname	%mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define	staticname %mklibname %{name} -s -d

Summary:	Open source image library
Name:		devil
Version:	1.7.2
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Libraries
URL:		http://openil.sourceforge.net/
Source0:	http://downloads.sourceforge.net/openil/%{oname}-%{version}.tar.gz
Patch1:		DevIL-1.7.1-underlinking.patch
BuildRequires:	zlib-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	SDL-devel
BuildRequires:	png-devel
BuildRequires:	lcms-devel
BuildRequires:	mng-devel
BuildRequires:	MesaGLU-devel
BuildRequires:  allegro-devel
BuildRequires:	ungif-devel
BuildRequires:	libtool
BuildRequires:	jasper-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%define	_requires_exceptions	devel(liballeg.*
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel

%description -n	%{develname}
Development headers and libraries for writing programs using %{oname}.

%package -n     %{staticname}
Summary:	Static library for %{oname}
Group:          Development/C
Requires:       %{libname}-devel = %{version}-%{release}
Provides:       lib%{name}-static-devel = %{version}-%{release}
Provides:       %{name}-static-devel = %{version}-%{release}
Obsoletes:      %{libname}-static-devel = %{version}-%{release}

%description -n %{staticname}
Static library for %{oname}.

%prep
%setup -q -c
%patch1 -p0 -b .lgif

chmod 644 AUTHORS CREDITS ChangeLog Libraries.txt README.unix

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
export CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math -fomit-frame-pointer -fexpensive-optimizations"

./autogen.sh

%configure2_5x	--with-pic \
		--with-gnu-ld \
		--enable-shared \
		--enable-static \
		%ifnarch ix86
		--enable-x86_64 \
		--enable-sse \
		--enable-sse2 \
		--disable-sse3 \
		%else
		--enable-x86 \
		--disable-sse \
		--disable-sse2 \
		--disable-sse3 \
		%endif
		--with-x
%make 

%install
rm -rf %{buildroot}
%makeinstall_std

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS CREDITS ChangeLog Libraries.txt README.unix
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/IL

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/*.a
