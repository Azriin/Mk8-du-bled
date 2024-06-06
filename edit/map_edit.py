import pyxel
import squarebuilder as sb
import toolbuilder as tool
import circleBuilder as cb
import distBuilder as db

class Editor:
    def __init__(self):
        pyxel.init(256, 256, "Mk8 du bled", fps=30)
        pyxel.image(0).load(0, 0, "../images/images.png")
        pyxel.mouse(True)
        self.tool = {
            "road": cb.roadBuilder(),
            "wall": sb.CreationMurs(),
            "separator": sb.CreationSep(),
            "dist next": db.CreationPoint() 
        }
        self.guiTool = tool.GUITool()
        pyxel.run(self.draw, self.update)

    def draw(self):
        pyxel.cls(11)
        for key in self.tool:
            self.tool[key].draw()
        self.guiTool.draw()

    def update(self):
        if not self.guiTool.get_actif() and self.guiTool.get_key() != None:
            if self.guiTool.get_key() == "dist next":
                self.tool[self.guiTool.get_key()].update(self.tool["separator"].getLst())
            else: self.tool[self.guiTool.get_key()].update()
            
        self.guiTool.update()

Editor()