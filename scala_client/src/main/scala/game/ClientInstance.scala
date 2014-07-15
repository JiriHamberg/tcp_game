package game

import java.util.concurrent.LinkedBlockingQueue
import java.net.Socket
import java.io.IOException

import org.json4s._
import org.json4s.native.JsonMethods._
import org.json4s.JsonDSL._
import scala.swing._

import gui.GameGUI
import io.ClientConnection

abstract sealed class ConnectionStatus
case object Successful extends ConnectionStatus
case class Refused(reason: String) extends ConnectionStatus

class Client private (val socket: Socket, val fps: Int) {
	val clientLogic = new ClientLogic(30, GameGUI.gameFrame)
	val connection = new ClientConnection(socket, clientLogic.messageQueue)
	clientLogic.clientOut = connection.messageQueue
	GameGUI.gameFrame.commandOut = clientLogic.commandQueue

	val logicThread = new Thread(clientLogic) //.start
	val connectionThread = new Thread(connection) //.start

	val connectionRequest = ("type" -> "join") ~ ("data" -> "")
	connection.messageQueue.put(connectionRequest)

	logicThread.start
	connectionThread.start
}

object Client {

	private var client = None: Option[Client]

	def connect(address: String, port: Int, fps: Int): ConnectionStatus = {

		disconnect()

		tryConnect(address, port) match {
			case Right(socket: Socket) => {
				client = Option(apply(socket, fps))
				Successful 
			}
			case Left(s: String) => Refused(s)
		}
	}

	private def disconnect() {
		client.foreach { client =>
			client.logicThread.interrupt
			client.connectionThread.interrupt
			try {
				client.socket.close
			} catch {
				case e: IOException => println("io-exception during socket close")
			}
			GameGUI.gameFrame.onDisconnect()
		}
	}

	private def tryConnect(address: String, port: Int): Either[String, Socket] = {
		try {
			return Right(new Socket(address, port))
		} catch {
			case e: IOException => return Left("Connection refused")
			case t: Throwable => throw t
		}
	}

	private def apply(socket: Socket, fps: Int) = new Client(socket, fps)

}