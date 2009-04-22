# TODO:
#	- check why the tests fail and fix that
#	  maybe it depends on network, vserver or so? WFM

# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		srcname		commons-net
Summary:	Commons Net - utility functions and components
Summary(pl.UTF-8):	Commons Net - funkcje i komponenty narzędziowe
Name:		java-commons-net
Version:	1.4.1
Release:	4
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/jakarta/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	ccbb3f67b55e8a7a676499db4386673c
Patch0:		jakarta-%{srcname}-disable_tests.patch
URL:		http://jakarta.apache.org/commons/net/
BuildRequires:	ant >= 1.5
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	java-oro >= 2.0.8
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-oro >= 2.0.8
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Commons Net is a set of utility functions and reusable components that should
be a help in any Java environment.

%description -l pl.UTF-8
Commons Net to zestaw funkcji narzędziowych i komponentów wielokrotnego
użycia, które mogą być pomocne w każdym środowisku Javy.

%package javadoc
Summary:	Commons Net documentation
Summary(pl.UTF-8):	Dokumentacja do Commons Net
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Commons Net documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Commons Net.

%prep
%setup -q -n commons-net-%{version}
%patch0 -p1

%build
cp LICENSE.txt LICENSE
CLASSPATH="$(build-classpath oro junit)"
export JAVA_HOME="%{java_home}"

# needed for tests, for some reason they ignore $CLASSPATH
mkdir -p target/lib
ln -sf %{_javadir}/oro.jar target/lib

%ant dist \
	-Dnoget=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

install dist/*.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf commons-net-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-net.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -R dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
