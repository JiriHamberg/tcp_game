import io.ClientConnection
import java.util.concurrent.LinkedBlockingQueue
import java.net.Socket
import org.json4s._
import org.json4s.native.JsonMethods._
import org.json4s.JsonDSL._

object Main { 

	def main(args: Array[String]) {
		val messageQueue = new LinkedBlockingQueue[JValue]()
		val socket = new Socket("127.0.0.1", 13373)

		val connection = new ClientConnection(socket, messageQueue)

		val connectionThread = new Thread(connection)
		connectionThread.start

		val connectionRequest = ("type" -> "join") ~ ("data" -> "")
		connection.messageQueue.put(connectionRequest)

		connectionThread.join
	}
}