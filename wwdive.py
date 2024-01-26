
from re import I
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Static, DataTable, Label, TextArea
from textual.containers import Container, Vertical
from textual import events
from textual.message import Message
from textual import log

import wwdiveUtils as wwdu

class OverlayTable(Container):
  dt = DataTable()
  
  class Selected(Message):
    def __init__(self, overlay_name: str) -> None:
      self.overlay_name = overlay_name
      super().__init__()
  
  def __init__(self, title: str) -> None:
    super().__init__()
    self._title = title
  
  def _test_dt(self) -> DataTable:
    l = wwdu.get_overlays()
    self.dt.add_columns("overlay name", "files")
    for x in l:
      self.dt.add_row(x[0], x[1])
    return self.dt
  
  def on_mount(self) -> None:
    table = self.query_one(DataTable)
    table.cursor_type = "row"
    self.styles.border = ("heavy", "gray")
  
  def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
    log("Row = ", self.dt.get_cell_at((message.cursor_row, 0)))
    super().post_message(self.Selected(self.dt.get_cell_at((message.cursor_row, 0))))
   
  def compose(self) -> ComposeResult:
    yield self._test_dt()

class OverlayDetailTable(Container):
  overlay_name = "ansible"
  dt = DataTable()

  class Selected(Message):
    def __init__(self, overlay_file_name: str) -> None:
      self.overlay_file_name = overlay_file_name
      log("OverlayDetailTable.Selected() overlay_file_name = ", overlay_file_name)
      super().__init__()
  
  def __init__(self, title: str) -> None:
    super().__init__()
    self._title = title
  
  def on_mount(self) -> None:
    table = self.query_one(DataTable)
    table.cursor_type = "row"
    self.styles.border = ("heavy", "white")
    self.styles.column_span = 2
   
  def _test_dt(self) -> DataTable:
    l = wwdu.get_overlay_files(self.overlay_name)
    self.dt.clear()
    self.dt.add_columns("PERM MODE", "UID", "GID", "SYSTEM-OVERLAY", "FILE PATH")
    for x in l:
      r = x.split()
      self.dt.add_row(r[0],r[1],r[2],r[3],r[4])
    return self.dt
  
  def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
    log("OverlayDetailTable() selected ", self.dt.get_cell_at((message.cursor_row, 4)))
    super().post_message(self.Selected(self.dt.get_cell_at((message.cursor_row, 4))))
  
  def compose(self) -> ComposeResult:
    #yield Label(self._title)
    yield self._test_dt()


class FileViewer(TextArea):
  overlay_name = ""
  file_to_show = ""
  
  def load_file(self):
    log("load_file() called with ", self.overlay_name, self.file_to_show)
    self.load_text(wwdu.get_file_content(self.overlay_name, self.file_to_show))
  
  def on_mount(self) -> None:
    self.styles.column_span = 3
  
  def on_focus(self) -> None:
    self.load_text(wwdu.get_file_content(self.overlay_name, self.file_to_show))
    #self.load_text(wwdu.get_file_content("ansible", "/usr/bin/post_install.sh"))

class MyApp(App):
  CSS_PATH = "wwdive.tcss"
  ODT = OverlayDetailTable("Overlay Detail")
  FV = FileViewer("File Viewer")

  def compose(self) -> ComposeResult:
    yield OverlayTable("Overlays")
    yield self.ODT
    #yield Static("Two", classes="box")
    yield self.FV

  def on_overlay_table_selected(self, message: OverlayTable.Selected) -> None:
    self.ODT.overlay_name = message.overlay_name
    self.ODT._test_dt()
  
  def on_overlay_detail_table_selected(self, message: OverlayDetailTable.Selected) -> None:
    self.FV.overlay_name = self.ODT.overlay_name
    self.FV.file_to_show = message.overlay_file_name
    self.FV.load_file()

#  def on_key(self, event: events.Key) -> None:
#    if event.key.isdecimal():
#      self.screen.styles.background = self.COLORS[int(event.key)]

if __name__ == "__main__":
  app = MyApp()
  app.run()


