package game.animation

object Bomb {
	val sheet = ImageUtil.loadImage("/sprites/BombExploding.png")

	val bombAnimation = new SpriteAnimation(sheet, (32, 64)) {
		val frames = getFramesAt( (1 to 7).map(i => (i, 1)) : _* )
	}

	val explosionAnimation = new SpriteAnimation(sheet, (32, 64)) {
		val frames = getFramesAt( (8 to 13).map(i => (i, 1)) : _* )
	}

	/*private def getFrameByTick(tick: Int, tickCount: Int, animation: SpriteAnimation) = {
		animation.frames((((tickCount - tick) / (tickCount.toDouble + 1)) * animation.frames.size).toInt)
	}*/

	def getBombFrame(tick: Int, tickCount: Int) = bombAnimation.getFrameByTick(tick, tickCount)
	def getExplosionFrame(tick: Int, tickCount: Int) = explosionAnimation.getFrameByTick(tick, tickCount)
}