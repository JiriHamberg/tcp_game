package game.animation

object Tiles {
	val sheet = ImageUtil.loadImage("/sprites/tiles.png")

	val brick = new SpriteAnimation(sheet, (32, 32)) {
		val frames = getFramesAt((2, 4))
	}

	val tile = new SpriteAnimation(sheet, (32, 32)) {
		val frames = getFramesAt((4, 5))
	}
}