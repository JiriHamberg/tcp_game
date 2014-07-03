import com.github.retronym.SbtOneJar._

oneJarSettings

name := "BomberClient"

version := "0.1"

scalaVersion := "2.11.1"

libraryDependencies += "org.json4s" %% "json4s-native" % "3.2.9"

libraryDependencies += "org.scala-lang" % "scala-swing" % "2.11.0-M7"

libraryDependencies += "commons-lang" % "commons-lang" % "2.6"

//packageOptions in (Compile, packageBin) +=
//    Package.ManifestAttributes( "Main-Class" -> "game.Main" )

mainClass in (Compile,run) := Some("game.Main")

mainClass in oneJar := Some("game.Main")