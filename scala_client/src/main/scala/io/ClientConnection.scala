package io

import java.io._
import java.net.Socket
import java.util.concurrent.LinkedBlockingQueue
import scala.annotation.tailrec

import org.json4s._
import org.json4s.native.JsonMethods._


class ClientConnection(val socket: Socket, val producedQueue: LinkedBlockingQueue[JValue]) extends Runnable {
	private val in = socket.getInputStream
	private val out = new PrintWriter(socket.getOutputStream(), false) //no autoflush
	
	val messageQueue = new LinkedBlockingQueue[JValue]()

	private val producerThread = new Thread(MessageProducer)
	private val consumerThread = new Thread(MessageConsumer)

	override def run {
		producerThread.start
		consumerThread.start
		producerThread.join
		consumerThread.join
	}

	private object MessageProducer extends Runnable {
		private val messageBuffer = new Array[Byte](1048576)
		private var bufferSize = 0

		override def run {
			while(true) {
				val read = in.read(messageBuffer, bufferSize, 1024)
				bufferSize += read
				if (read <= 0) return //socket closed
				handleInput
			}
		}
		
		private def readMessageSize(): Long = { //mimic uint_32 with jvm long 
			var size = 0L
			for (i <- 0 to 3) {
				val b = messageBuffer(i)
				size = size | (( b & 0xFF) << (8 * (3 - i)))
			}
			size
		}

		@tailrec
		private def handleInput() {
			if (bufferSize <= 4) return
			val messageSize = readMessageSize.asInstanceOf[Int]
			if (bufferSize >= messageSize + 4) {
				val message = new String(messageBuffer.slice(4, messageSize + 4), "UTF-8")
				bufferSize -= messageSize + 4
				//shift buffer left
				Array.copy(messageBuffer, messageSize + 4, messageBuffer, 0, bufferSize)  
				try {
					producedQueue.put(parse(message))
					println("produced: " + message)
				} catch  {
					case t: Throwable => {
						println("Error parsing message: " + message)
						throw t
					}
				}
				
				handleInput //check if there is still more messages to be handled
			}
		}
	}

	private object MessageConsumer extends Runnable {
		
		private def writeMessageSize(message: String) = {
			val size = message.size.asInstanceOf[Long]
			val bytes = new Array[Byte](4)
			for (i <- 0 to 3) {
				bytes(i) = ((size >> (8 * (3 - i))) & 0xFF).toByte
			}
			new String(bytes, "UTF-8")
		}

		override def run {
			while(true) {
				//blocking
				val message = compact(render(messageQueue.take()))
				out.write(writeMessageSize(message) +  message)
				out.flush 
			}
		}
	}


}