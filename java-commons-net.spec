Summary:	Jakarta Commons Net - utility functions and components
Summary(pl):	Jakarta Commons Net - funkcje i komponenty narzêdziowe
Name:		jakarta-commons-net
Version:	1.4.1
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	ccbb3f67b55e8a7a676499db4386673c
URL:		http://jakarta.apache.org/commons/net/
BuildRequires:	jakarta-ant(junit) >= 1.5
BuildRequires:	jakarta-oro >= 2.0.8
BuildRequires:	jaxp
BuildRequires:	junit
Requires:	jakarta-oro >= 2.0.8
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	%{_datadir}/java

%description
Jakarta Commons Net is a set of utility functions and reusable
components that should be a help in any Java environment.

%description -l pl
Jakarta Commons Net to zestaw funkcji narzêdziowych i komponentów
wielokrotnego u¿ycia, które mog± byæ pomocne w ka¿dym ¶rodowisku Javy.

%prep
%setup -q -n commons-net-%{version}

%build
cp LICENSE.txt LICENSE
# for tests
export CLASSPATH=%{_javadir}/oro.jar
ant dist \
	-Dnoget=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

install dist/*.jar $RPM_BUILD_ROOT%{_javalibdir}
ln -sf commons-net-%{version}.jar $RPM_BUILD_ROOT%{_javalibdir}/commons-net.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dist/LICENSE dist/docs/api
%{_javalibdir}/*.jar
