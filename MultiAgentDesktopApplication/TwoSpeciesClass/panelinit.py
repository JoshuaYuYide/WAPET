from OneSpecieClass.panelinit import PanelInit, GridWidget

class PanelInitTwo(PanelInit):
    def left_element(self):
        super().left_element()
        self.species.addItem("prey")
        self.species.addItem("predator")