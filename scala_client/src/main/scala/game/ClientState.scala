package game

import java.util.concurrent.LinkedBlockingQueue
import scala.collection.mutable.Map
import scala.collection.mutable.ArrayBuffer
import org.json4s._
import org.json4s.native.JsonMethods._
import org.json4s.JsonDSL._

import scala.collection.JavaConversions._

import gui.GameFrame
import game.commands._

class ClientLogic(val fps: Int, val canvas: GameFrame) extends Runnable {
	val commandQueue = new LinkedBlockingQueue[Any]()
	val messageQueue = new LinkedBlockingQueue[JValue]()
	val spriteMap = Map[Int, Sprite]()

	var clientOut: LinkedBlockingQueue[JValue] = null

	override def run {
		while(true) {
			val before = System.currentTimeMillis
			update
			val after = System.currentTimeMillis
			val toSleep = (1000.0 / fps - (after - before)).toInt
			if (toSleep > 0) Thread.sleep(toSleep)
		}
	}

	private def update {
		consumeMessages
		dispatchCommands
	}

	private def consumeMessages {
		val messages = {
			val temp = new java.util.ArrayList[JValue](messageQueue.size)
			messageQueue.drainTo(temp)
			temp
		}
		messages.foreach(message => updateSprites(message))
	}

	private def updateSprites(message: JValue) {
		implicit val formats = DefaultFormats 

		if ((message \ "type").extract[String] !=  "update") return

		val deleted = for (JObject(sprite) <- message \ "data" \ "deleted") yield Sprite(sprite)
		val updated = for (JObject(sprite) <- message \ "data" \ "updated") yield Sprite(sprite)
		val added = for (JObject(sprite) <- message \ "data" \ "new") yield Sprite(sprite)

		deleted.foreach(s => {
			s.onDelete()
			spriteMap -= s.id
		})

		updated.foreach(s => spriteMap += (s.id -> s))
		added.foreach(s => spriteMap += (s.id -> s))

		canvas.updateSprites(spriteMap.values)
	}

	private def dispatchCommands {
		commandQueue.map(c => commandToJSON(c)).foreach(c => clientOut.put(c))
	}

	private def commandToJSON(command: Any): JValue = command match {
		case BombCommand => ("type" -> "bomb") ~ ("data" -> "")
		case MoveCommand(direction) =>
			("type" -> "move") ~ 
			("data" -> ("command" -> direction))
		case _ => throw new IllegalArgumentException("Invalid client command")
	}

}