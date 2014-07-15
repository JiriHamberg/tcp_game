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
		GameGUI.main(args)
	}
	
}