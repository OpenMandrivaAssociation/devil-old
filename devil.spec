%define	oname	DevIL
%define	name	devil
%define	version	1.6.7
%define release %mkrel 15

%define	major	1
%define	lib_name_orig	lib%{name}
%define	lib_name	%mklibname %{name} %{major}
%define	lib_name_devel	%mklibname %{name} %{major} -d
%define	lib_name_static_devel	%mklibname %{name} %{major} -s -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{oname}-%{version}.tar.bz2
Patch0:		devil-1.6.7-debian-fixes.patch
Patch1:		devil-1.6.7-link-against-gif.patch
Patch2:		devil-1.6.7-fix-allegro-linking.patch
Patch3:		devil-1.6.7-headerfixes.patch
Patch4:		devil-1.6.7-header-void.patch
License:	LGPL
Group:		System/Libraries
URL:		http://openil.sourceforge.net/
Summary:	Image library
BuildRequires:	zlib-devel jpeg-devel tiff-devel autoconf2.5 SDL-devel
BuildRequires:	png-devel lcms-devel mng-devel MesaGLU-devel
BuildRequires:  allegro-devel ungif-devel libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package -n	%{lib_name}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Provides:	%{lib_name_orig}
Provides:	%{name}

%description -n	%{lib_name}
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package -n	%{lib_name_devel}
Summary:	Development headers and libraries for writing programs using %{oname}
Group:		Development/C
Requires:	%{lib_name} = %{version} allegro-devel
%define	_requires_exceptions	devel(liballeg.*
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name_devel}
Development headers and libraries for writing programs using %{oname}

%package -n     %{lib_name_static_devel}
Summary:        NAS static library
Group:          Development/C
Requires:       %{lib_name}-devel = %{version}
Provides:       %{lib_name_orig}-static-devel = %{version}-%{release}
Provides:       %{name}-static-devel = %{version}-%{release}

%description -n %{lib_name_static_devel}
NAS static library.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1 -b .debian
%patch1 -p1 -b .lgif
%patch2 -p1 -b .allegro
%patch3 -p1 -b .headerfixes
%patch4 -p0

%build
autoconf
CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math -fomit-frame-pointer -fexpensive-optimizations" \
%configure2_5x	--with-pic \
		--with-gnu-ld \
		--enable-shared \
		--with-x \
		--enable-static
%make LIBTOOL=%{_bindir}/libtool

%install
rm -rf %{buildroot}
%makeinstall

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%doc AUTHORS BUGS CREDITS ChangeLog INSTALL Libraries.txt NEWS README.unix
%{_libdir}/*.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/IL

%files -n %{lib_name_static_devel}
%defattr(644,root,root,755)
%{_libdir}/*.a


