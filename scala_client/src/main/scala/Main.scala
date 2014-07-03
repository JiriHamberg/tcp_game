package game

import io.ClientConnection
import java.util.concurrent.LinkedBlockingQueue
import java.net.Socket
import org.json4s._
import org.json4s.native.JsonMethods._
import org.json4s.JsonDSL._

import scala.swing._

import gui.GameGUI
import game._

object Main { 

	def main(args: Array[String]) {
		val address = args(0)
		val port = args(1).toInt
		val socket = new Socket(address, port) // "127.0.0.1", 13373
		val clientLogic = new ClientLogic(30, GameGUI.gameFrame)
		val connection = new ClientConnection(socket, clientLogic.messageQueue)
		clientLogic.clientOut = connection.messageQueue
		GameGUI.gameFrame.commandOut = clientLogic.commandQueue
		
		val connectionRequest = ("type" -> "join") ~ ("data" -> "")
		connection.messageQueue.put(connectionRequest)


		new Thread(clientLogic).start
		new Thread(connection).start

		GameGUI.main(args)
	}
}