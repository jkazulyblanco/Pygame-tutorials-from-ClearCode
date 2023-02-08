# 01 # Setup | # 02 # Layout | # 03 # Logic |

# ▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄

# 01 # Imports
import PyQt5.QtWidgets as qtw

# 01 # Main Window
class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator T-800')
        
        # 02 # 1-layout, 2-create button, 3-add button to layout
        self.setLayout(qtw.QVBoxLayout())
        # btn1 = qtw.QPushButton('Test')
        # self.layout().addWidget(btn1)
        self.keypad()

        self.show()  # 01 #

    def keypad(self): # 02 #
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        # Create Buttons
        self.result_field = qtw.QLineEdit()
        btn_result = qtw.QPushButton('Enter')    
        btn_clear = qtw.QPushButton('Clear')    
        btn_9 = qtw.QPushButton('9')    
        btn_8 = qtw.QPushButton('8')    
        btn_7 = qtw.QPushButton('7')    
        btn_6 = qtw.QPushButton('6')    
        btn_5 = qtw.QPushButton('5')    
        btn_4 = qtw.QPushButton('4')    
        btn_3 = qtw.QPushButton('3')    
        btn_2 = qtw.QPushButton('2')    
        btn_1 = qtw.QPushButton('1')    
        btn_0 = qtw.QPushButton('0')    
        btn_plus = qtw.QPushButton('+')    
        btn_mins = qtw.QPushButton('-')    
        btn_mult = qtw.QPushButton('x')    
        btn_divd = qtw.QPushButton('÷')

        # Adding the buttons to the layoout
        # ( widget, row, col, # cells x, # cells y)
        container.layout().addWidget(self.result_field,0,0,1,4)
        container.layout().addWidget(btn_result,1,0,1,2)
        container.layout().addWidget(btn_clear,1,2,1,2)
        container.layout().addWidget(btn_7,2,0)
        container.layout().addWidget(btn_8,2,1)
        container.layout().addWidget(btn_9,2,2)
        container.layout().addWidget(btn_plus,2,3)
        container.layout().addWidget(btn_4,3,0)
        container.layout().addWidget(btn_5,3,1)
        container.layout().addWidget(btn_6,3,2)
        container.layout().addWidget(btn_mins,3,3)
        container.layout().addWidget(btn_1,4,0)
        container.layout().addWidget(btn_2,4,1)
        container.layout().addWidget(btn_3,4,2)
        container.layout().addWidget(btn_mult,4,3)
        container.layout().addWidget(btn_0,5,0,1,3)
        container.layout().addWidget(btn_divd,5,3)

        # put the widgets on the main window
        self.layout().addWidget(container)

# 01 # Objects
app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion')) # 02 # Style
app.exec_()