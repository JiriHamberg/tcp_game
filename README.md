tcp_game
========
Bomberman-like game with python backend and a scala client implementation (pygame client is no longer up to date). 
Uses plain old tcp sockets for communication by json messages over a minimal custom protocol.

The python backend uses version 2.7 of python and only depends on the standard library.

The scala client is managed using sbt build tool. To build a standalone jar, use "sbt one-jar" in the scala-client folder.
