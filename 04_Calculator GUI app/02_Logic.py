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
        
        # 03 # store numbers
        self.temp_nums = []
        self.fin_nums = []

        self.show()  # 01 #

    def keypad(self): # 02 #
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        # Create Buttons
        self.result_field = qtw.QLineEdit()
        # 03 # update, add functionality
        btn_result = qtw.QPushButton('Enter', clicked= self.func_result)    
        btn_clear = qtw.QPushButton('Clear',  clicked= self.clear_calc)    
        btn_9 = qtw.QPushButton('9', clicked= lambda: self.num_press('9'))    
        btn_8 = qtw.QPushButton('8', clicked= lambda: self.num_press('8'))    
        btn_7 = qtw.QPushButton('7', clicked= lambda: self.num_press('7'))    
        btn_6 = qtw.QPushButton('6', clicked= lambda: self.num_press('6'))    
        btn_5 = qtw.QPushButton('5', clicked= lambda: self.num_press('5'))    
        btn_4 = qtw.QPushButton('4', clicked= lambda: self.num_press('4'))    
        btn_3 = qtw.QPushButton('3', clicked= lambda: self.num_press('3'))    
        btn_2 = qtw.QPushButton('2', clicked= lambda: self.num_press('2'))    
        btn_1 = qtw.QPushButton('1', clicked= lambda: self.num_press('1'))    
        btn_0 = qtw.QPushButton('0', clicked= lambda: self.num_press('0'))    
        btn_plus = qtw.QPushButton('+', clicked= lambda: self.func_press('+'))    
        btn_mins = qtw.QPushButton('-', clicked= lambda: self.func_press('-'))    
        btn_mult = qtw.QPushButton('x', clicked= lambda: self.func_press('*'))    
        btn_divd = qtw.QPushButton('÷', clicked= lambda: self.func_press('/'))

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

    def num_press(self, key_number): # 03 #
        self.temp_nums.append(key_number) # add button number to temp list
        temp_string = ''.join(self.temp_nums)
        if self.fin_nums:
            self.result_field.setText(''.join(self.fin_nums) + temp_string)
        else: 
            self.result_field.setText(temp_string)

    def func_press(self, operator): # 03 #
        temp_string = ''.join(self.temp_nums)
        self.fin_nums.append(temp_string)
        self.fin_nums.append(operator)
        self.temp_nums = []
        self.result_field.setText(''.join(self.fin_nums))

    def func_result(self): # 03 #
        fin_string = ''.join(self.fin_nums) + ''.join(self.temp_nums)
        result_string = eval(fin_string)
        fin_string += '='
        fin_string += str(result_string)
        self.result_field.setText(fin_string)

    def clear_calc(self): # 03 #
        self.result_field.clear()
        self.temp_nums = []
        self.fin_nums = []


# 01 # Objects
app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion')) # 02 # Style
app.exec_()