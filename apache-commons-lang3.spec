Name:		apache-commons-lang3
Version:	3.21.0
Release:	1
Summary:	Helper utilities for the java.lang API
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-lang/
Source0:	https://archive.apache.org/dist/commons/lang/source/commons-lang3-%{version}-src.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(org.apache.commons:commons-parent:pom:)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-lang3 --link %{name} --alias commons-lang3:commons-lang3

%description
Apache Commons Lang provides extra methods for classes in java.lang.

%prep
%setup -q -n commons-lang3-%{version}-src

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
