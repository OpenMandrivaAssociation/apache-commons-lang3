Name:		apache-commons-lang3
Version:	3.21.0
Release:	2
Summary:	Helper utilities for the java.lang API
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-lang/
Source0:	https://archive.apache.org/dist/commons/lang/source/commons-lang3-%{version}-src.tar.gz
# Gradle 9.9.1 strictly pins org.apache.commons:commons-lang3 3.20.0.
Source1:	https://archive.apache.org/dist/commons/lang/source/commons-lang3-3.20.0-src.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(org.apache.commons:commons-parent:pom::)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-lang3 --link %{name} --alias commons-lang3:commons-lang3

%description
Apache Commons Lang provides extra methods for classes in java.lang.
3.21.0 stays the default jar. Gradle 9.9.1 strictly pins 3.20.0, so
that jar is installed beside it.

%prep
%setup -q -n commons-lang3-%{version}-src
%setup -q -T -D -a 1 -n commons-lang3-%{version}-src
find . -name '*.jar' -delete

%build -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
mkdir -p lang320/classes
find commons-lang3-3.20.0-src/src/main/java -name '*.java' > lang320/sources.list
test -s lang320/sources.list
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-d lang320/classes @lang320/sources.list
"$JAVA_HOME/bin/jar" cf lang320/commons-lang3.jar -C lang320/classes .
cat > lang320/commons-lang3.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>3.20.0</version>
  <name>Apache Commons Lang</name>
  <description>Helper utilities for the java.lang API.</description>
  <url>https://commons.apache.org/proper/commons-lang/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
</project>
EOF

%install -p
sysjar install --buildroot %{buildroot} \
	--artifact lang320/commons-lang3.pom:lang320/commons-lang3.jar \
	--file-name commons-lang3-3.20.0 \
	--filelist .mfiles320
# 3.21.0 owns commons-lang3.sysjar. 3.20.0 keeps a second index file.
/bin/mv %{buildroot}/usr/share/sysjar/index/org.apache.commons/commons-lang3.sysjar \
	%{buildroot}/usr/share/sysjar/index/org.apache.commons/commons-lang3-3.20.0.sysjar
sed -i 's|/usr/share/sysjar/index/org.apache.commons/commons-lang3\.sysjar|/usr/share/sysjar/index/org.apache.commons/commons-lang3-3.20.0.sysjar|' .mfiles320

%install -a
while IFS= read -r line; do
	grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
done < .mfiles320

%check -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cat > LangSmoke.java << 'EOF'
import org.apache.commons.lang3.StringUtils;
public class LangSmoke {
	public static void main(String[] args) {
		String value = StringUtils.repeat("ab", 2);
		if (!"abab".equals(value)) {
			throw new AssertionError(value);
		}
		System.out.println(args[0] + " " + value);
	}
}
EOF
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/commons-lang3.jar LangSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/commons-lang3.jar:." LangSmoke lang321_ok | tee check321.log
grep -F -q 'lang321_ok abab' check321.log
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/commons-lang3-3.20.0.jar LangSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/commons-lang3-3.20.0.jar:." LangSmoke lang320_ok | tee check320.log
grep -F -q 'lang320_ok abab' check320.log

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
