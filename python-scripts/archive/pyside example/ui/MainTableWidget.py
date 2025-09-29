from PySide6.QtWidgets import QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QSizePolicy, QGridLayout, QGroupBox, QCheckBox, QRadioButton, QButtonGroup, QListWidget, QAbstractItemView, QTabWidget, QComboBox
from PySide6.QtGui import QPixmap, Qt

class MainTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Components
        label = QLabel('Your name (plain text or html): ')
        image_label = QLabel()
        image_label.setPixmap(QPixmap('assets/settings-icon.png').scaled(20, 20, Qt.KeepAspectRatio))
        self.line_edit = QLineEdit()
        self.line_edit.textChanged.connect(self.text_changed)
        button = QPushButton('Print my name')
        button.clicked.connect(self.handleButtonClicked)
        self.line_edit_text_holder = QLabel('-- Your name --')

        # Text edit box
        self.text_edit_box = QTextEdit()
        copy_button = QPushButton('Copy')
        copy_button.clicked.connect(self.text_edit_box.copy)
        cut_button = QPushButton('Cut')
        cut_button.clicked.connect(self.text_edit_box.cut)
        paste_button = QPushButton('Paste')
        paste_button.clicked.connect(self.text_edit_box.paste)
        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.text_edit_box.clear)
        html_button = QPushButton('Html')
        html_button.clicked.connect(self.setHtml)
        plain_button = QPushButton('Plain text')
        plain_button.clicked.connect(self.setPlainText)

        # -> Size policy: how widgets behave if container space is expanded or shrinked
        label_size_policy = QLabel("Some text: ")
        line_edit_size_policy = QLineEdit()
        line_edit_size_policy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) #default setting

        h_layout_size_policy = QHBoxLayout()
        h_layout_size_policy.addWidget(label_size_policy)
        h_layout_size_policy.addWidget(line_edit_size_policy)

        button1_size_policy = QPushButton("Button 1")
        button2_size_policy = QPushButton("Button 2")
        button3_size_policy = QPushButton("Button 3")

        # -> Stretch: ho much of the available space (in the layout) is occupied by the widgets
        # You specify the stretch when you add things to the layout
        h_layout_size_policy2 = QHBoxLayout()
        h_layout_size_policy2.addWidget(button1_size_policy, 2)
        h_layout_size_policy2.addWidget(button2_size_policy, 1)
        h_layout_size_policy2.addWidget(button3_size_policy, 1)

        v_layout_size_policy = QVBoxLayout()
        v_layout_size_policy.addLayout(h_layout_size_policy)
        v_layout_size_policy.addLayout(h_layout_size_policy2)

        # Components and text edit box Layout
        layout_horizontal_inner = QHBoxLayout()
        layout_horizontal_inner.addWidget(label)
        layout_horizontal_inner.addWidget(image_label)
        layout_horizontal_inner.addWidget(self.line_edit)

        layout_horizontal_inner2 = QHBoxLayout()
        layout_horizontal_inner2.addWidget(copy_button)
        layout_horizontal_inner2.addWidget(cut_button)
        layout_horizontal_inner2.addWidget(paste_button)
        layout_horizontal_inner2.addWidget(clear_button)
        layout_horizontal_inner2.addWidget(html_button)
        layout_horizontal_inner2.addWidget(plain_button)



        # Grid layout
        grid_widget_container = QWidget()
        button1_grid = QPushButton('One')
        button2_grid = QPushButton('Two')
        button3_grid = QPushButton('Three')
        button3_grid.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        button4_grid = QPushButton('Four')
        button5_grid = QPushButton('Five')
        button6_grid = QPushButton('Six')
        button7_grid = QPushButton('Seven')

        grid_layout = QGridLayout()
        grid_layout.addWidget(button1_grid, 0, 0)
        grid_layout.addWidget(button2_grid, 0, 1, 1, 2) # take up 1 row and 2 columns
        grid_layout.addWidget(button3_grid, 1, 0, 2, 1) # take up 2 rows and 1 column
        grid_layout.addWidget(button4_grid, 1, 1)
        grid_layout.addWidget(button5_grid, 1, 2)
        grid_layout.addWidget(button6_grid, 2, 1)
        grid_layout.addWidget(button7_grid, 2, 2)
        grid_widget_container.setLayout(grid_layout)



        # Checkboxes, Radio buttons
        check_radio_container = QWidget()
        os_groupbox = QGroupBox('Choose operating system')
        windows_checkbox = QCheckBox('Windows')
        windows_checkbox.toggled.connect(self.windows_box_toggled)
        linux_checkbox = QCheckBox('Linux')
        linux_checkbox.toggled.connect(self.linux_box_toggled)
        mac_checkbox = QCheckBox('Mac')
        mac_checkbox.toggled.connect(self.mac_box_toggled)

        os_layout = QVBoxLayout()
        os_layout.addWidget(windows_checkbox)
        os_layout.addWidget(linux_checkbox)
        os_layout.addWidget(mac_checkbox)
        os_groupbox.setLayout(os_layout)

        # exclusive checkboxes
        drinks_groupbox = QGroupBox('Choose a drink')
        beer_checkbox = QCheckBox('Beer')
        juice_checkbox = QCheckBox('Juice')
        coffee_checkbox = QCheckBox('Coffee')
        beer_checkbox.setChecked(True)

        exclusive_button_group = QButtonGroup(self)
        exclusive_button_group.addButton(beer_checkbox)
        exclusive_button_group.addButton(juice_checkbox)
        exclusive_button_group.addButton(coffee_checkbox)
        exclusive_button_group.setExclusive(True)

        drink_layout = QVBoxLayout()
        drink_layout.addWidget(beer_checkbox)
        drink_layout.addWidget(juice_checkbox)
        drink_layout.addWidget(coffee_checkbox)
        drinks_groupbox.setLayout(drink_layout)

        # Radio buttons
        answers = QGroupBox('Choose an answer')
        answer_a = QRadioButton('A')
        answer_b = QRadioButton('B')
        answer_c = QRadioButton('C')
        answer_a.setChecked(True)

        answer_layout = QVBoxLayout()
        answer_layout.addWidget(answer_a)
        answer_layout.addWidget(answer_b)
        answer_layout.addWidget(answer_c)
        answers.setLayout(answer_layout)

        # here be carefull what and how you add the widgets and layouts
        check_box_layout = QHBoxLayout()
        check_box_layout.addWidget(os_groupbox)
        check_box_layout.addWidget(drinks_groupbox)
        check_radio_layout = QVBoxLayout()
        check_radio_layout.addLayout(check_box_layout)
        check_radio_layout.addWidget(answers)
        check_radio_container.setLayout(check_radio_layout)



        # List widget
        list_widget_container = QWidget()
        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_widget.addItem('Item 1')
        self.list_widget.addItems(['Item 2', 'Item 3'])
        self.list_widget.currentItemChanged.connect(self.list_widget_item_changed)
        self.list_widget.currentTextChanged.connect(self.list_widget_text_changed)

        button_add_list_item = QPushButton('Add item')
        button_add_list_item.clicked.connect(self.add_item_to_list)
        button_delete_list_item = QPushButton('Delete item')
        button_delete_list_item.clicked.connect(self.delete_item_to_list)
        button_count_list_items = QPushButton('Count items')
        button_count_list_items.clicked.connect(self.count_items_in_list)
        button_select_list_items = QPushButton('Selected items')
        button_select_list_items.clicked.connect(self.selected_items_in_list)

        layout_horizontal_list_widget = QHBoxLayout()
        layout_vertical_list_widget = QVBoxLayout()
        layout_vertical_list_widget.addWidget(button_add_list_item)
        layout_vertical_list_widget.addWidget(button_delete_list_item)
        layout_vertical_list_widget.addWidget(button_count_list_items)
        layout_vertical_list_widget.addWidget(button_select_list_items)
        layout_horizontal_list_widget.addWidget(self.list_widget)
        layout_horizontal_list_widget.addLayout(layout_vertical_list_widget)
        list_widget_container.setLayout(layout_horizontal_list_widget)



        # Tab widget
        tab_widget = QTabWidget(self)
        tab_widget.addTab(check_radio_container, 'Checkboxes & Radio buttons')
        tab_widget.addTab(list_widget_container, 'List widget')
        tab_widget.addTab(grid_widget_container, 'Grid layout')



        #Combobox widget
        combobox_container = QWidget()
        self.combobox = QComboBox(self)
        self.combobox.addItem('Mercury')
        self.combobox.addItems(['Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus'])

        button_current_value_combobox = QPushButton('Current value')
        button_current_value_combobox.clicked.connect(self.current_value_combobox)
        button_set_value_combobox = QPushButton('Set value')
        button_set_value_combobox.clicked.connect(self.set_value_combobox)
        button_get_values_combobox = QPushButton('Get values')
        button_get_values_combobox.clicked.connect(self.get_values_combobox)

        combobox_h_layout = QHBoxLayout()
        combobox_h_layout.addWidget(self.combobox)
        combobox_h_layout.addWidget(button_current_value_combobox)
        combobox_h_layout.addWidget(button_set_value_combobox)
        combobox_h_layout.addWidget(button_get_values_combobox)
        combobox_h_layout.addSpacing(100)
        combobox_container.setLayout(combobox_h_layout)

        

        # Master layout
        layout_vertical = QVBoxLayout()
        layout_vertical.addLayout(layout_horizontal_inner)
        layout_vertical.addWidget(button)
        layout_vertical.addWidget(self.line_edit_text_holder)
        layout_vertical.addLayout(layout_horizontal_inner2)
        layout_vertical.addWidget(self.text_edit_box)
        layout_vertical.addLayout(v_layout_size_policy)
        layout_vertical.addSpacing(20)
        layout_vertical.addWidget(combobox_container)
        layout_vertical.addSpacing(20)
        layout_vertical.addWidget(tab_widget)
        self.setLayout(layout_vertical)

    def handleButtonClicked(self):
        print('Your name is ', self.line_edit.text())

    def text_changed(self):
        self.line_edit_text_holder.setText('Hello '+ self.line_edit.text())

    def setHtml(self):
        self.text_edit_box.setHtml(self.line_edit.text())

    def setPlainText(self):
        self.text_edit_box.setPlainText(self.line_edit.text())

    def windows_box_toggled(self, checked):
        if checked:
            print("windows_box checked")
        else:
            print("windows_box unchecked")
        

    def linux_box_toggled(self, checked):
        if checked:
            print("linux_box checked")
        else:
            print("linux_box unchecked")
    
    def mac_box_toggled(self, checked):
        if checked:
            print("mac_box checked")
        else:
            print("mac_box unchecked")

    def list_widget_item_changed(self, item):
        print("list_widget_item_changed: %s" % item.text())

    def list_widget_text_changed(self, text):
        print("list_widget_text_changed: %s" % text)

    def add_item_to_list(self):
        self.list_widget.addItem('New item')

    def delete_item_to_list(self):
        self.list_widget.takeItem(self.list_widget.currentRow())

    def count_items_in_list(self):
        print('Item count: %d' % self.list_widget.count())

    def selected_items_in_list(self):
        list = self.list_widget.selectedItems()
        for i in list:
            print(i.text())
    
    def current_value_combobox(self):
        print("Current item: ", self.combobox.currentText(), " - ", "Current index: ", self.combobox.currentIndex())

    def set_value_combobox(self):
        self.combobox.setCurrentIndex(2)

    def get_values_combobox(self):
        for i in range(self.combobox.count()):
            print('index [', i, ']: ', self.combobox.itemText(i))
