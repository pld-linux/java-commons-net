# TODO:
# - does not build with java_gcj_compat

%bcond_without	javadoc		# don't build javadoc
%bcond_with	java_sun	# use java_sun

%include        /usr/lib/rpm/macros.java

%define		srcname		commons-net
Summary:	Commons Net - utility functions and components
Summary(pl.UTF-8):	Commons Net - funkcje i komponenty narzędziowe
Name:		java-commons-net
Version:	2.0
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	583630202369df3cf996cbdba4d8634b
URL:		http://commons.apache.org/net/
BuildRequires:	ant >= 1.5
BuildRequires:	jakarta-oro >= 2.0.8
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{!?with_java_sun:BuildRequires:	java-gnu-classpath}
%{?with_java:BuildRequires:	java-sun}
#BuildRequires:	jaxp
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jakarta-oro >= 2.0.8
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

# java.util.regexp from libgcj-4.3 does not provide Mather.toMatchResult()
# method, so we have to use one provided by glibj (from gnu-classpath).
# toMatchResult is implemented in libgcj-4.4, so most probably, when gcc-4.4
# will be released, we can can drop gnu-classpath dependency
%if %{without java_sun}
  glibj_jar=$(find-jar glibj)
%endif

CLASSPATH=$CLASSPATH:$(build-classpath oro junit)
export CLASSPATH
export JAVA_HOME="%{java_home}"

mkdir build

%javac \
	-classpath $CLASSPATH \
	-d build \
	-source 1.5 \
	-target 1.5 \
	%{!?with_java_sun:-bootclasspath "$glibj_jar"} \
	$(find src/main/java/org -name '*.java')

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

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
