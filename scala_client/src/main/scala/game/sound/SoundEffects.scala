package game.sound

import game.sound.SoundSystem

import scala.util.Random

object Item {
	val audioResources = (1 to 10).map(i => SoundSystem.loadAudioResource("/sound_effects/coin%d.wav".format(i)))

	def playCollectSound {
		val audioResource = audioResources(Random.nextInt(10))
		SoundSystem.playSound(audioResource, 5.0f)
	}
}

object Bomb {
	val audioResource = SoundSystem.loadAudioResource("/sound_effects/atari_boom.wav")
	
	def playExplosionSound {
		SoundSystem.playSound(audioResource)
	}
}