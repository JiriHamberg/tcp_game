package gui

import scala.swing._
import scala.swing.BorderPanel.Position._

import gui.GameFrame
import game._

class GameMenuBar(val gameFrame: GameFrame) extends MenuBar {
	contents += new Menu("Games") {
		contents += new MenuItem(Action("Join a Game") { onJoinGame() })
	}

	private def onJoinGame() {
		new JoinDialog()
	}
}

class JoinDialog extends Dialog {
	val hostName = new TextField
	val port = new TextField

	val joinButton = Button("Join") {
        onButtonPressed()
	}

	def onButtonPressed() {
		val h = hostName.text
		var p = -1
		try {
			p = port.text.toInt
		} catch {
			case e: NumberFormatException => {
				Dialog.showMessage(null, "Port must be an integer", "Join Error", Dialog.Message.Error)
				return
			}
		}

		join(h, p) match {
			case Successful => close()
			case Refused(reason: String) => 
				Dialog.showMessage(null, reason, "Join Error", Dialog.Message.Error)
		}
	}

	def join(address: String, port: Int): ConnectionStatus = Client.connect(address, port, 30)

	modal = true

	contents = new BorderPanel {
    	layout(new BoxPanel(Orientation.Vertical) {
      	  border = Swing.EmptyBorder(5,5,5,5)
	      contents += new Label("Hostname:")
	      contents += hostName
	      contents += new Label("Port:")
	      contents += port
    	}) = Center

    	layout(new FlowPanel(FlowPanel.Alignment.Right)(
	      	joinButton	
    	)) = South
    }

	centerOnScreen()
	open()
}