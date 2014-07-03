package game.animation

object Crystal {
	private val revolutions = 12
	private val crystalByColor = Map(
		"blue" -> "/sprites/crystal-blue.png",
		"green" -> "/sprites/crystal-green.png",
		"grey" -> "/sprites/crystal-grey.png",
		"orange" -> "/sprites/crystal-orange.png",
		"pink" -> "/sprites/crystal-pink.png",
		"yellow" -> "/sprites/crystal-yellow.png"
		).map(t => (t._1, makeAnimation(t._2)))

	private def makeAnimation(sheetPath: String) = {
		new SpriteAnimation(ImageUtil.loadImage(sheetPath), (32, 32)) {
			val frames = getFramesAt( (1 to 8).map(i => (i, 1)) : _* )
		}
	}

	def getCrystalFrame(tick: Int, tickCount: Int, color: String) = {
		crystalByColor(color).getFrameByTick(tick, tickCount, revolutions)
	} 
}