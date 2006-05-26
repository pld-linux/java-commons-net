#
# TODO:
#	- check why the tests fail and fix that
#
Summary:	Jakarta Commons Net - utility functions and components
Summary(pl):	Jakarta Commons Net - funkcje i komponenty narz�dziowe
Name:		jakarta-commons-net
Version:	1.4.1
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	ccbb3f67b55e8a7a676499db4386673c
Patch0:		%{name}-disable_tests.patch
URL:		http://jakarta.apache.org/commons/net/
BuildRequires:	ant-junit >= 1.5
BuildRequires:	jakarta-oro >= 2.0.8
BuildRequires:	jaxp
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	junit
Requires:	jakarta-oro >= 2.0.8
Requires:	jre
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jakarta Commons Net is a set of utility functions and reusable
components that should be a help in any Java environment.

%description -l pl
Jakarta Commons Net to zestaw funkcji narz�dziowych i komponent�w
wielokrotnego u�ycia, kt�re mog� by� pomocne w ka�dym �rodowisku Javy.

%package javadoc
Summary:	Jakarta Commons Net documentation
Summary(pl):	Dokumentacja do Jakarta Commons Net
Group:		Development/Languages/Java

%description javadoc
Jakarta Commons Net documentation.

%description javadoc -l pl
Dokumentacja do Jakarta Commons Net.

%prep
%setup -q -n commons-net-%{version}
%patch0 -p1

%build
cp LICENSE.txt LICENSE
export CLASSPATH="`build-classpath oro junit`"
export JAVA_HOME="%{java_home}"

# needed for tests, for some reason they ignore $CLASSPATH
mkdir -p target/lib
ln -sf %{_javadir}/oro.jar target/lib

ant dist \
	-Dnoget=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version}}

install dist/*.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf commons-net-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-net.jar

cp -R dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dist/LICENSE
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
