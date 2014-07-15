package game

import org.json4s._
import org.json4s.native.JsonMethods._
import scala.swing._

import game.animation._

abstract class Sprite(val pos: (Int, Int), val dim: (Int, Int), val id: Int) {
	def paint(g: Graphics2D): Unit

	def onDelete() = {}
}

object Sprite {
	def apply(data: JObject) = {
		implicit val formats = DefaultFormats 
		val pos = ((data \ "pos")(0).extractOpt[Int].get, (data \ "pos")(1).extractOpt[Int].get)
		val dim = ((data \ "dim")(0).extractOpt[Int].get, (data \ "dim")(1).extractOpt[Int].get)
		val id = (data \ "sprite_id").extractOpt[Int].get
		val spriteType = (data \ "type").extractOpt[String].get

		spriteType match {
			case "player" => new PlayerSprite(pos, dim, id, data)
			case "bomb" => new BombSprite(pos, dim, id, data)
			case "explosion" => new ExplosionSprite(pos, dim, id, data)
			case "item" => new ItemSprite(pos, dim, id, data)
			case "brick" => new BrickSprite(pos, dim, id)
			case "tile" => new TileSprite(pos, dim, id)

			case _ => 
				new Sprite(pos, dim, id) {
					override def paint(g: Graphics2D) {
						g.setColor(new Color(255, 0, 0))
						g.drawRect(pos._1, pos._2, dim._1, dim._2)
					}
				}
		}
	}
}

class PlayerSprite(pos: (Int, Int), dim: (Int, Int), id: Int, val active: Boolean, val direction: String, val lastUpdated: Long) extends Sprite(pos, dim, id) {
	def this(pos: (Int, Int), dim: (Int, Int), id: Int, data: JObject)(implicit formats: Formats = DefaultFormats ) = 
		this(pos, dim, id, 
			(data \ "active").extractOpt[Boolean].get, 
			(data \ "direction").extractOpt[String].get,
			(data \ "last_state_change").extractOpt[Long].get
		)

	override def paint(g: Graphics2D) {
		val img = PlayerAnimation.getFrame(lastUpdated, direction, active)
		val align = PlayerAnimation.getAlignment(dim)
		g.drawImage(img, pos._1 + align._1, pos._2 + align._2, null)
	}
}

class BrickSprite(pos: (Int, Int), dim: (Int, Int), id: Int) extends Sprite(pos, dim, id) {
	override def paint(g: Graphics2D) {
		val img = Tiles.brick.frames(0)
		g.drawImage(img, pos._1, pos._2, null)
	}
}

class TileSprite(pos: (Int, Int), dim: (Int, Int), id: Int) extends Sprite(pos, dim, id) {
	override def paint(g: Graphics2D) {
		val img = Tiles.tile.frames(0)
		g.drawImage(img, pos._1, pos._2, null)
	}
}

class BombSprite(pos: (Int, Int), dim: (Int, Int), id: Int, val tick: Int, val tickCount: Int) extends Sprite(pos, dim, id) {
	def this(pos: (Int, Int), dim: (Int, Int), id: Int, data: JObject)(implicit formats: Formats = DefaultFormats ) = 
		this(pos, dim, id, 
			(data \ "timer").extractOpt[Int].get, 
			(data \ "timer_start").extractOpt[Int].get
		)
	override def paint(g: Graphics2D) {
		val img = Bomb.getBombFrame(tick, tickCount)
		val align = (0, -32)
		g.drawImage(img, pos._1 + align._1, pos._2 + align._2, null)
	}

	override def onDelete() {
		game.sound.Bomb.playExplosionSound
	}
}

class ExplosionSprite(pos: (Int, Int), dim: (Int, Int), id: Int, val tick: Int, val tickCount: Int) extends Sprite(pos, dim, id) {
	def this(pos: (Int, Int), dim: (Int, Int), id: Int, data: JObject)(implicit formats: Formats = DefaultFormats ) = 
		this(pos, dim, id, 
			(data \ "timer").extractOpt[Int].get, 
			(data \ "timer_start").extractOpt[Int].get
		)
	override def paint(g: Graphics2D) {
		val img = Bomb.getExplosionFrame(tick, tickCount)
		val align = (0, -32)
		g.drawImage(img, pos._1 + align._1, pos._2 + align._2, null)
	}
}

class ItemSprite(pos: (Int, Int), dim: (Int, Int), id: Int, val tick: Int, val tickCount: Int, val itemType: String) extends Sprite(pos, dim, id) {
	def this(pos: (Int, Int), dim: (Int, Int), id: Int, data: JObject)(implicit formats: Formats = DefaultFormats ) = 
		this(pos, dim, id, 
			(data \ "timer").extractOpt[Int].get, 
			(data \ "timer_start").extractOpt[Int].get,
			(data \ "item_type").extractOpt[String].get
		)

	override def paint(g: Graphics2D) {
		val color = itemType match {
			case "bomb_power" => "yellow"
			case "bomb_speed" => "blue"
			case _ => "none"
		}
		val img = Crystal.getCrystalFrame(tick, tickCount, color)
		val align = (0, 0)
		g.drawImage(img, pos._1 + align._1, pos._2 + align._2, null)
	}

	override def onDelete() {
		//println("item collected!")
		game.sound.Item.playCollectSound
	}
}