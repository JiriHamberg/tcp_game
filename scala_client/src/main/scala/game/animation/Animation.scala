package game.animation

import java.awt.Graphics2D
import java.awt.Image
import java.awt.image.BufferedImage
import java.awt.geom.AffineTransform
import java.awt.image.AffineTransformOp

import java.io.File
import javax.imageio._

import scala.io.Source

object ImageUtil {
	private def getAbsolutePath(relativePath: String) = {
		getClass.getResource(relativePath).toURI
	}

	def loadImage(relativePath: String): BufferedImage = {
		//ImageIO.read(new File(getAbsolutePath(relativePath)))
		ImageIO.read(getClass().getResource(relativePath))
	}

	def flipHorizontal(img: BufferedImage) = {
		val tx = AffineTransform.getScaleInstance(-1, 1)
		tx.translate(-img.getWidth(null), 0)
		val op = new AffineTransformOp(tx, AffineTransformOp.TYPE_NEAREST_NEIGHBOR)
		op.filter(img, null)
	}
}


abstract class SpriteAnimation(val sheet: BufferedImage, val dim: (Int, Int)) {
	val frames: Seq[BufferedImage]

	def getFrameAtPos(pos: (Int, Int)): BufferedImage = {
		sheet.getSubimage((pos._1 - 1) * dim._1, (pos._2 - 1) * dim._2, dim._1, dim._2)
	}

	def getFramesAt(positions: (Int, Int)*) = {
		positions.map(getFrameAtPos(_))
	}

	def loopFrames(started: Long, animationLength: Long): BufferedImage = {
		val now = System.currentTimeMillis
		frames( ((((now - started) % animationLength.toInt ) / animationLength.toDouble) * frames.size).toInt )
	}

	def getFrameByTick(tick: Int, tickCount: Int, revolutions: Int = 1) = {
		frames((((revolutions * (tickCount - tick)) / (tickCount.toDouble + 1)) * frames.size).toInt % frames.size)
	}

	def getAlignment(spriteDim: (Int, Int)) = {
		( (spriteDim._1 - dim._1) / 2, (spriteDim._2 - dim._2) / 2  )
	}

} 

object SpriteAnimation {
	def flipHorizontal[A <: SpriteAnimation](animation: A ) = 
		new SpriteAnimation(animation.sheet, animation.dim) {
			val frames = animation.frames.map(ImageUtil.flipHorizontal(_))
		}
}