Name:     nimf
Summary:  An input method framework
Version:  2019.07.24
Release:  1%{?dist}
License:  LGPLv3+
Group:    User Interface/Desktops
URL:      https://gitlab.com/nimf-i18n/nimf
Source0:  https://gitlab.com/nimf-i18n/nimf/-/archive/master/nimf-master.tar.bz2

BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: glib2-devel
BuildRequires: pkgconfig
BuildRequires: intltool >= 0.50.1
BuildRequires: gtk3-devel
BuildRequires: gtk2-devel
BuildRequires: qt4-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtbase-private-devel
BuildRequires: libappindicator-gtk3-devel
BuildRequires: librsvg2-tools
BuildRequires: google-noto-cjk-fonts
BuildRequires: libhangul-devel
BuildRequires: anthy-devel
BuildRequires: anthy
BuildRequires: libxkbcommon-devel
BuildRequires: wayland-devel
BuildRequires: libxklavier-devel
BuildRequires: gtk-doc

Requires: anthy
Requires: glib2
Requires: gtk3
Requires: im-chooser
Requires: libappindicator-gtk3
Requires: libhangul
Requires: libxkbcommon
Requires: libxklavier
Requires(post):   %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives

%define _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/nimf.conf

%description
Nimf is a lightweight, fast and extensible input method framework.

%package devel
Summary:  Development files for nimf
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: gtk3-devel

%description devel
This package contains development files.

%prep
%setup -q

%build
./autogen.sh --prefix=/usr --libdir=%{_libdir} --enable-gtk-doc \
  --with-imsettings-data --disable-nimf-m17n --disable-nimf-rime
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%clean

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%{_bindir}/update-gtk-immodules %{_host} || :
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :
%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_xinputconf} 55 || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%{_bindir}/update-gtk-immodules %{_host} || :
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :
if [ "$1" = "0" ]; then
  %{_sbindir}/alternatives --remove xinputrc %{_xinputconf} || :
  # if alternative was set to manual, reset to auto
  [ -L %{_sysconfdir}/alternatives/xinputrc -a "`readlink %{_sysconfdir}/alternatives/xinputrc`" = "%{_xinputconf}" ] && %{_sbindir}/alternatives --auto xinputrc || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%config %{_xinputconf}
%config %{_sysconfdir}/apparmor.d/abstractions/nimf
%{_bindir}/*
%{_libdir}/gtk-2.0/*
%{_libdir}/gtk-3.0/*
%{_libdir}/libnimf.so.*
%{_libdir}/nimf/*
%{_libdir}/qt4/*
%{_libdir}/qt5/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/*
%{_datadir}/icons/*
%{_datadir}/locale/*
%{_datadir}/man/*
%{_sysconfdir}/input.d/nimf.conf
%{_sysconfdir}/xdg/autostart/*

%files devel
%{_datadir}/gtk-doc/*
%{_includedir}/*
%{_libdir}/libnimf.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Jul 24 2019 Hodong Kim <cogniti@gmail.com> - 2019.07.24-1
- See https://gitlab.com/nimf-i18n/nimf/blob/master/debian/changelog