package game

import org.json4s._
import org.json4s.native.JsonMethods._
import scala.swing._

abstract class Sprite(val pos: (Int, Int), val dim: (Int, Int), val id: Int) {
	def paint(g: Graphics2D): Unit	
}

object Sprite {
	def apply(data: JObject) = {
		implicit val formats = DefaultFormats 
		val pos = ((data \ "pos")(0).extractOpt[Int].get, (data \ "pos")(1).extractOpt[Int].get)
		val dim = ((data \ "dim")(0).extractOpt[Int].get, (data \ "dim")(1).extractOpt[Int].get)
		val id = (data \ "sprite_id").extractOpt[Int].get

		new Sprite(pos, dim, id) {
			override def paint(g: Graphics2D) {
				g.setColor(new Color(255, 0, 0))
				g.drawRect(pos._1, pos._2, dim._1, dim._2)
			}
		}

	}
}


/*class PlayerSprite(val pos: (Int, Int), val dim: (Int, Int), val id: Int) extends Sprite {
	
	override def paint(g: Graphics2D) {
	}	
}*/
