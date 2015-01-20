package game.sound

import java.io.ByteArrayInputStream
import javax.sound.sampled.AudioInputStream
import javax.sound.sampled.AudioFormat

class AudioResource(val format: AudioFormat, val frameLength: Long, val audioData: Array[Byte]) {
	def getAudioInputStream() = {
		val byteArrayInputStream = new ByteArrayInputStream(audioData)
		new AudioInputStream(byteArrayInputStream, format, frameLength)
	}
}

object SoundSystem {
	import java.io._
	import java.net.URL
	import javax.sound.sampled._

	private var backgroundStream = None: Option[AudioInputStream]

	def getAudioStream(audioResourcePath: String) = {
		val url = getClass().getResource(audioResourcePath)
		AudioSystem.getAudioInputStream(url)
	}

	/* Loads an audio resource to memory for creating multiple audiostreams
	 * with only one file access.
	 */
	def loadAudioResource(resourcePath: String): AudioResource = {
		println("LOADING RESOURCE %s".format(resourcePath))
		val audioStream = getAudioStream(resourcePath)
		val outputStream = new ByteArrayOutputStream()
		val byteBuffer = new Array[Byte](1024)
		var readBytes = audioStream.read(byteBuffer, 0, 1024)
		while(readBytes >= 0) {
			outputStream.write(byteBuffer, 0, readBytes)
			readBytes = audioStream.read(byteBuffer, 0, 1024)
		}
		new AudioResource(audioStream.getFormat(), audioStream.getFrameLength(), outputStream.toByteArray)
	}

	def playSound(audio: AudioResource, volumeAdjustment: Float = 0.0f) {
		val stream = audio.getAudioInputStream()
		val info = new DataLine.Info(classOf[Clip], audio.format)
		//val clip = AudioSystem.getClip
		val clip = AudioSystem.getLine(info).asInstanceOf[Clip]
		clip.open(stream)
		//openJDK does not seem to support "Master control" - Great!
		//adjustVolume(clip, volumeAdjustment)
		addDefaultLineListener(clip)
		clip.start()
	}

	def addDefaultLineListener(clip: Clip) {
		clip.addLineListener(new LineListener {
			override def update(e: LineEvent) {
				if(e.getType == LineEvent.Type.STOP) {
					e.getLine.close()
				}
			}
		})
	}

	def adjustVolume(clip: Clip, adjustment: Float) {
		val control = clip.getControl(FloatControl.Type.MASTER_GAIN).asInstanceOf[FloatControl]
		control.setValue(adjustment)
	}

	def playBackground(audioResourcePath: String, volumeAdjustment: Float = 0.0f) {
		val stream = getAudioStream(audioResourcePath)
		backgroundStream.foreach(_.close())
		backgroundStream = Some(stream)
		backgroundStream.foreach( stream => {
			val clip = AudioSystem.getClip
			clip.open(stream)
			adjustVolume(clip, volumeAdjustment)
			addDefaultLineListener(clip)
			clip.loop(Clip.LOOP_CONTINUOUSLY)
		})
	}
}