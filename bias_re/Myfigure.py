from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide6.QtCore import Qt


class MyNavigationToolbar(NavigationToolbar):
    toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        (None, None, None, None),
        ('Pan',
         'Left button pans, Right button zooms\n'
         'x/y fixes axis, CTRL fixes aspect',
         'move', 'pan'),
        ('Zoom', 'Zoom to rectangle\nx/y fixes axis, CTRL fixes aspect',
         'zoom_to_rect', 'zoom'),
        ("Customize", "Edit axis, curve and image parameters",
         "qt4_editor_options", "edit_parameters"),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure')
    )

    # def __init__(self, canvas, parent=None):
    #     super().__init__(canvas, parent)
    #     try:
    #         # Reduce icon size to make the toolbar shorter vertically
    #         self.setIconSize(self.iconSize().scaled(16, 16, Qt.KeepAspectRatio))
    #     except Exception:
    #         pass
    #     try:
    #         # Use icons-only compact style to further reduce height; keeps tooltips
    #         self.setToolButtonStyle(Qt.ToolButtonIconOnly)
    #     except Exception:
    #         pass