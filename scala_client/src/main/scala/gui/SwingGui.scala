package gui

import java.util.concurrent.LinkedBlockingQueue
import scala.collection.JavaConversions._
import scala.swing._
import scala.swing.event._
import scala.swing.event.Key._
import java.awt.event._

import game.Sprite
import game.commands._
import game.sound._

class GameFrame extends MainFrame {
	val sprites =  new LinkedBlockingQueue[Sprite]() 
	var commandOut: LinkedBlockingQueue[Any] = null

	val gamePanel = new Panel {
		preferredSize = new Dimension(800, 640)
 		opaque = true
		focusable = true

 		listenTo(keys)

 		reactions += {
	    	case KeyPressed(_, key, _, _) => onKeyPressed(key)
	        case KeyReleased(_, key, _, _) => onKeyReleased(key)
	   
	        case x: Any => {} //println(x)
    	}

    	def onKeyPressed(key: Value) = key match {
    		case Key.Space => commandOut.put(BombCommand)
    		case Key.A => commandOut.put(MoveCommand("left"))
    		case Key.W => commandOut.put(MoveCommand("up"))
    		case Key.D => commandOut.put(MoveCommand("right"))
    		case Key.S => commandOut.put(MoveCommand("down"))
    		case _ => {}	
    	}

    	def onKeyReleased(key: Value) = key match {
    		case Key.Space => commandOut.remove(BombCommand)
    		case Key.A => commandOut.remove(MoveCommand("left"))
    		case Key.W => commandOut.remove(MoveCommand("up"))
    		case Key.D => commandOut.remove(MoveCommand("right"))
    		case Key.S => commandOut.remove(MoveCommand("down"))
    		case _ => {}
    	}
    	

		override def paint(g: Graphics2D) = {
			g.setBackground(new Color(0,255,0))
			sprites.foreach(s => s.paint(g))
		}
	}

	menuBar = new GameMenuBar(this)

	title = "Bomber"
	contents = new FlowPanel {
		contents += gamePanel
	}

	centerOnScreen

	reactions += {
		case WindowClosing(e) => {
    		println("Exiting...")
    		System.exit(0)
    	}
    }

    def updateSprites(currentSprites: Iterable[Sprite]) {
    	sprites.clear
    	currentSprites.foreach(s => sprites.put(s))
    	this.repaint
    }

    def onDisconnect() {
    	sprites.clear
    	commandOut = null
    	this.repaint
    }
}

object GameGUI extends SimpleSwingApplication {
	val gameFrame = new GameFrame
	
	def top = gameFrame

	//force lazy objects to be initialized
	def loadResources() {
		game.sound.Bomb
		game.sound.Item
		game.animation.Bomb
		game.animation.Crystal
		game.animation.PlayerAnimation
		game.animation.Tiles		
	}

	loadResources()
	//SoundSystem.playBackground("/sound_effects/PizzaParty.au", -20.0f)
}