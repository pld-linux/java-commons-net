# NOTE:
# - ftp timezone test is broken. It depends on file timestamps on some remote
#   ftp machine. But these files have changed since this test was written!!!

%bcond_with		tests		# tests are broken. see note above.
%bcond_without	javadoc		# don't build javadoc

%include	/usr/lib/rpm/macros.java
%define		srcname	commons-net
Summary:	Commons Net - utility functions and components
Summary(pl.UTF-8):	Commons Net - funkcje i komponenty narzędziowe
Name:		java-commons-net
Version:	2.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	583630202369df3cf996cbdba4d8634b
Source1:	%{name}-build.xml
URL:		http://commons.apache.org/net/
BuildRequires:	ant
%{?with_tests:BuildRequires:	ant-junit}
%{!?with_java_sun:BuildRequires:	java-gnu-classpath}
BuildRequires:	java-oro >= 2.0.8
BuildRequires:	jdk
BuildRequires:	jpackage-utils
%{?with_tests:BuildRequires:	junit}
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-oro >= 2.0.8
Provides:	jakarta-commons-net
Obsoletes:	jakarta-commons-net
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jakarta Commons Net is a set of utility functions and reusable
components that should be a help in any Java environment.

%description -l pl.UTF-8
Jakarta Commons Net to zestaw funkcji narzędziowych i komponentów
wielokrotnego użycia, które mogą być pomocne w każdym środowisku Javy.

%package javadoc
Summary:	Jakarta Commons Net documentation
Summary(pl.UTF-8):	Dokumentacja do Jakarta Commons Net
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	jakarta-commons-net-javadoc

%description javadoc
Jakarta Commons Net documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do Jakarta Commons Net.

%prep
%setup -q -n commons-net-%{version}-src

%build

cp %{SOURCE1} build.xml

# java.util.regexp from libgcj-4.3 does not provide Mather.toMatchResult()
# method, so we have to use one provided by glibj (from gnu-classpath).
# toMatchResult is implemented in libgcj-4.4, so most probably, when gcc-4.4
# will be released, we can drop gnu-classpath dependency

%if %{without java_sun}
  glibj_jar=$(find-jar glibj)
%endif

%if %{with java_sun}
%define compiler sun
%else
%define compiler gcj
%endif

CLASSPATH=$(build-classpath oro)

%ant clean compile-%{compiler} jar \
	-Dversion=%{version} \
	%{!?with_java_sun:-Dbootstrap=$glibj_jar} \

%if %{with tests}
CLASSPATH=$CLASSPATH:$(build-classpath junit)
%ant tests-compile-%{compiler} tests \
	-Dversion=%{version} \
	%{!?with_java_sun:-Dbootstrap=$glibj_jar} \
%endif

%if %{with javadoc}
%javadoc -d apidocs \
	%{?with_java_sun:org.apache.commons.net} \
	$(find src/main/java/org -name '*.java')
%endif

%jar -cf %{srcname}-%{version}.jar -C build .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{srcname}-%{version}}

install %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with javadoc}
cp -R apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
