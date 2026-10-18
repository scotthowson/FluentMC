#!/usr/bin/env sh
# Needs Java 25. Uses GraalVM if present, else whatever 'java' is on PATH.
cd "$(dirname "$0")"
JAVA="${JAVA:-$(command -v java)}"
[ -x /usr/lib/jvm/graalvm-jdk-25/bin/java ] && JAVA=/usr/lib/jvm/graalvm-jdk-25/bin/java
exec "$JAVA" -Xms6G -Xmx6G -XX:+UseZGC -XX:+AlwaysPreTouch -Dfile.encoding=UTF-8 -jar fabric-server-mc.26.3-loader.0.20.0-launcher.1.1.2.jar nogui
