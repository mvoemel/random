from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QToolBar, QStatusBar, QMessageBox, QSizePolicy
import PySide6.QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from ui.MainTableWidget import MainTableWidget

class MainAppWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle('Test')
        self.setGeometry(400, 50, 600, 400)
        # self.resize(1000, 500)


        #MenuBar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        quit_action = file_menu.addAction('Quit')
        quit_action.triggered.connect(self.quit_app)

        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction('Copy')
        edit_menu.addAction('Cut')
        edit_menu.addAction('Paste')
        edit_menu.addAction('Undo')
        edit_menu.addAction('Redo')

        menu_bar.addMenu('Window')
        menu_bar.addMenu('Setting')
        menu_bar.addMenu('Help')
        

        #Toolbar
        toolbar = QToolBar('My main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(PySide6.QtCore.Qt.LeftToolBarArea, toolbar)
        toolbar.setMovable(False)
        # toolbar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        toolbar.addAction(quit_action)

        action1 = QAction('Some Action', self)
        action1.setStatusTip('Status message for some action')
        action1.triggered.connect(self.toolbar_button_click)
        toolbar.addAction(action1)

        action2 = QAction(QIcon('assets/settings-icon.png'), 'Another Action', self)
        action2.setStatusTip('Status message for another action')
        action2.triggered.connect(self.toolbar_button_click)
        action2.setCheckable(True)
        toolbar.addAction(action2)

        toolbar.addSeparator()
        message_button = QPushButton('Message Box')
        message_button.clicked.connect(self.message_box_click)
        toolbar.addWidget(message_button)


        #StatusBar
        self.setStatusBar(QStatusBar(self))


        #CentralWidget
        mainTableWidget = MainTableWidget()
        self.setCentralWidget(mainTableWidget)

    def quit_app(self):
        self.app.quit()

    def toolbar_button_click(self):
        self.statusBar().showMessage('Toolbar Button clicked', 3000)

    def message_box_click(self):
        # Static messagebox methods: critical, information, question, warning, about
        ret = QMessageBox.critical(self, 'Message Box', 
                                   'This is a message box', 
                                   QMessageBox.Ok | QMessageBox.Cancel)
        # message = QMessageBox()
        # message.setMinimumSize(700, 200)
        # message.setWindowTitle('Message Box')
        # message.setText('This is a message box')
        # message.setInformativeText('This is an informative message box')
        # message.setIcon(QMessageBox.Critical)
        # message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # message.setDefaultButton(QMessageBox.Ok)
        # ret = message.exec()
        if ret == QMessageBox.Ok:
            print('User chose ok')
        else:
            print('User chose cancel')
