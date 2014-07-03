package game.animation

trait Activatible {
	val idle: SpriteAnimation
	val active: SpriteAnimation
}

object PlayerAnimation {
	val sheet = ImageUtil.loadImage("/sprites/Panda.png")
	val animationLength = 400 //0.4s

	val down = new Activatible {
		override val idle = new SpriteAnimation(sheet, (32, 32)) {
			val frames = getFramesAt((1,1), (2,1))
		}
		override val active = new SpriteAnimation(sheet, (32, 32)) {
			val frames = getFramesAt((1,2), (2,2), (3,2))
		}
	}

	val up = new Activatible {
		override val idle = new SpriteAnimation(sheet, (32, 32)) {
			val frames = getFramesAt((1,3))
		}
		override val active = new SpriteAnimation(sheet, (32, 32)) {
			val frames = getFramesAt((1,3), (2,3), (3,3))
		}
	}

	val right = new Activatible {
		override val idle = new SpriteAnimation(sheet, (32, 32)) {
			val frames = getFramesAt((1,5), (2,5))
		}
		override val active = new SpriteAnimation(sheet, (32, 32)) {
			val frames = getFramesAt((1,4), (2,4), (3,4))
		}
	}

	val left = new Activatible  {
		override val idle = SpriteAnimation.flipHorizontal(right.idle)
		override val active = SpriteAnimation.flipHorizontal(right.active)
	}

	def getFrame(started: Long, direction: String, active: Boolean) = {
		val animationDirection = direction match {
			case "down" => down
			case "up" => up
			case "left" => left
			case "right" => right
			case _ => throw new IllegalArgumentException("Invalid direction: %s".format(direction))
		}
		
		val animation = 
			if(active) animationDirection.active
			else animationDirection.idle
		animation.loopFrames(started, animationLength)
	}

	val getAlignment = down.active.getAlignment _
}