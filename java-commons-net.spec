Summary:	Jakarta Commons Net - utility functions and components
Summary(pl):	Jakarta Commons Net - funkcje i komponenty narzêdziowe
Name:		jakarta-commons-net
Version:	1.2.2
Release:	0.1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/net/source/commons-net-%{version}-src.tar.gz
# Source0-md5:	3856e8b3f50bdfffbf186e07c477f73b
URL:		http://jakarta.apache.org/
BuildRequires:	jakarta-ant >= 1.5
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
cd net
cp LICENSE.txt LICENSE
ant -Dnoget=1 dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

install net/dist/*.jar $RPM_BUILD_ROOT%{_javalibdir}
ln -sf commons-net-%{version}.jar $RPM_BUILD_ROOT%{_javalibdir}/commons-net.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc net/dist/LICENSE net/dist/RELEASE-NOTES.txt net/dist/docs/api
%{_javalibdir}/*.jar
