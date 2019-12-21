"""
A learning test of calculator by Harry Zhang
"""

import sys
from math import log, log10, e, pi, sin, cos, tan, asin, acos, atan
from PyQt5.QtWidgets import  QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, \
     QPushButton, QTabWidget, QTextBrowser, QGroupBox, QRadioButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Window(QWidget):
    """
    A form for calculator
    """
    def __init__(self, f):
        super().__init__()
        self.setWindowTitle("calculator by Harry")
        self.setGeometry(100, 100, 400, 200)
        m_layout = QVBoxLayout()
        self.setLayout(m_layout)

        self.font = f
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.tbrowser = QTextBrowser()
        m_layout.addWidget(self.tbrowser)
        self.input = "welcome"
        self.res = "= "
        self.recall = ""
        self.mr = ""
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)
        self.tbrowser.setMinimumHeight(140)
        self.tbrowser.setFont(self.font)

        self.input_flag = ""
        self.x_f = 0
        self.n_f = 0

        self.num_system = QGroupBox()
        m_layout.addWidget(self.num_system)
        num_system_layout = QHBoxLayout(self.num_system)
        self.num_system_d = QRadioButton("Decimal")
        self.num_system_d.setFont(self.font)
        self.num_system_d.setChecked(True)
        self.num_system_d.clicked.connect(self.num_system_onClicked)
        num_system_layout.addWidget(self.num_system_d)
        self.num_system_b = QRadioButton("toBin")
        self.num_system_b.setFont(self.font)
        self.num_system_b.setEnabled(False)
        self.num_system_b.clicked.connect(self.num_system_onClicked)
        num_system_layout.addWidget(self.num_system_b)
        self.num_system_h = QRadioButton("toHex")
        self.num_system_h.setFont(self.font)
        self.num_system_h.setEnabled(False)
        self.num_system_h.clicked.connect(self.num_system_onClicked)
        num_system_layout.addWidget(self.num_system_h)


        self.tab_widget = QTabWidget()
        m_layout.addWidget(self.tab_widget)
        self.tab_widget.setFont(self.font)
# tab_1 layout
        self.tab_1 = QWidget()
        self.tab_widget.addTab(self.tab_1, "calculatin")
        tab_1_layout = QHBoxLayout(self.tab_1)
        tab_1_layout.setSpacing(0)

        self.tab_1_widget_h1 = QWidget()
        tab_1_layout.addWidget(self.tab_1_widget_h1)
        tab_1_widget_h1_layout = QVBoxLayout(self.tab_1_widget_h1)
        tab_1_widget_h1_layout.setContentsMargins(0, 0, 0, 0)
        tab_1_widget_h1_layout.setSpacing(0)

        v_1 = ["mc", "C", "7", "4", "1", "%"]
        for i in v_1:
            b_tmp = QPushButton(i)
            b_tmp.setObjectName(i)
            b_tmp.setSizePolicy(size_policy)
            if i in ["7", "4", "1", "%"]:
                b_tmp.setShortcut(i)
            elif i == "C":
                b_tmp.setShortcut('c')
            tab_1_widget_h1_layout.addWidget(b_tmp)

        self.tab_1_widget_h2 = QWidget()
        tab_1_layout.addWidget(self.tab_1_widget_h2)
        tab_1_widget_h2_layout = QVBoxLayout(self.tab_1_widget_h2)
        tab_1_widget_h2_layout.setContentsMargins(0, 0, 0, 0)
        tab_1_widget_h2_layout.setSpacing(0)

        v_2 = ["m+", "/", "8", "5", "2", "0"]
        for i in v_2:
            b_tmp = QPushButton(i)
            b_tmp.setObjectName(i)
            b_tmp.setSizePolicy(size_policy)
            if i != "m+":
                b_tmp.setShortcut(i)
            tab_1_widget_h2_layout.addWidget(b_tmp)

        self.tab_1_widget_h3 = QWidget()
        tab_1_layout.addWidget(self.tab_1_widget_h3)
        tab_1_widget_h3_layout = QVBoxLayout(self.tab_1_widget_h3)
        tab_1_widget_h3_layout.setContentsMargins(0, 0, 0, 0)
        tab_1_widget_h3_layout.setSpacing(0)

        v_3 = ["m-", "*", "9", "6", "3", "."]
        for i in v_3:
            b_tmp = QPushButton(i)
            b_tmp.setObjectName(i)
            b_tmp.setSizePolicy(size_policy)
            if i != "m-":
                b_tmp.setShortcut(i)
            tab_1_widget_h3_layout.addWidget(b_tmp)

        self.tab_1_widget_h4 = QWidget()
        tab_1_layout.addWidget(self.tab_1_widget_h4)
        tab_1_widget_h4_layout = QVBoxLayout(self.tab_1_widget_h4)
        tab_1_widget_h4_layout.setContentsMargins(0, 0, 0, 0)
        tab_1_widget_h4_layout.setSpacing(0)

        self.tab_1_widget_h4_1 = QWidget()
        tab_1_widget_h4_layout.addWidget(self.tab_1_widget_h4_1)
        tab_1_widget_h4_1_layout = QVBoxLayout(self.tab_1_widget_h4_1)
        tab_1_widget_h4_1_layout.setContentsMargins(0, 0, 0, 0)
        tab_1_widget_h4_1_layout.setSpacing(0)

        v_4_1 = ["mr", "<-"]
        for i in v_4_1:
            b_tmp = QPushButton(i)
            b_tmp.setObjectName(i)
            b_tmp.setSizePolicy(size_policy)
            if i == "<-":
                b_tmp.setShortcut(Qt.Key_Backspace)
            tab_1_widget_h4_1_layout.addWidget(b_tmp)

        self.tab_1_widget_h4_2 = QWidget()
        tab_1_widget_h4_layout.addWidget(self.tab_1_widget_h4_2)
        tab_1_widget_h4_2_layout = QVBoxLayout(self.tab_1_widget_h4_2)
        tab_1_widget_h4_2_layout.setContentsMargins(0, 0, 0, 0)
        tab_1_widget_h4_2_layout.setSpacing(0)

        v_4_2 = ["-", "+"]
        for i in v_4_2:
            b_tmp = QPushButton(i)
            b_tmp.setObjectName(i)
            b_tmp.setShortcut(i)
            b_tmp.setSizePolicy(size_policy)
            tab_1_widget_h4_2_layout.addWidget(b_tmp)

        self.equal = QPushButton("=")
        tab_1_widget_h4_layout.addWidget(self.equal)
        self.equal.setSizePolicy(size_policy)
        self.equal.setStyleSheet("background-color: rgb(0,190,255); color: rgb(248,248,255)")
        self.equal.setObjectName("=")
        self.equal.setShortcut("=")
        self.equal.clicked.connect(self.equal_clicked)



# tab_2 layout
        self.tab_2 = QWidget()
        self.tab_widget.addTab(self.tab_2, "function")

        tab_2_layout = QGridLayout(self.tab_2)
        tab_2_layout.setSpacing(0)

        f_list = ["(", ")", "x!", "xˉ¹", "x²", "x³", "xⁿ", "√x", "ⁿ√x", \
            "e", "ln", "log", "sin", "cos", "tan", "π", "Deg", "lnv"]
        n_tmp = 0
        for i in range(6):
            for j in range(3):
                b_tmp2 = QPushButton(f_list[n_tmp])
                b_tmp2.setObjectName(f_list[n_tmp])
                b_tmp2.setSizePolicy(size_policy)
                tab_2_layout.addWidget(b_tmp2, i, j)
                n_tmp += 1

        btn_list = self.findChildren(QPushButton)

        func1_btn = ["mc", "m+", "m-", "mr"]
        input1_btn = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "%"]
        input2_btn = ["(", ")", "π", "e"]
        cal1_btn = ["C", "/", "*", "<-", "-", "+"]
        func2_btn = ["x!", "xˉ¹", "x²", "x³", "xⁿ", "√x", "ⁿ√x", "ln", "log", "sin", "cos", "tan", "Deg", "lnv"]


        for btn in btn_list:
            if btn.objectName() in cal1_btn:
                btn.setStyleSheet("background-color: rgb(220,220,220); color: rgb(0,190,255)")
                if btn.objectName() in ["/", "*", "-", "+"]:
                    btn.clicked.connect(self.input_clicked)
                elif btn.objectName() == "C":
                    btn.clicked.connect(self.clear_clicked)
                elif btn.objectName() == "<-":
                    btn.clicked.connect(self.back_clicked)

            elif btn.objectName() in input1_btn:
                btn.setStyleSheet("background-color: rgb(248,248,255)")
                btn.clicked.connect(self.input_clicked)

            elif btn.objectName() in input2_btn:
                btn.setStyleSheet("background-color: rgb(220,220,220); color: rgb(100,100,100)")
                btn.clicked.connect(self.input_clicked)

            elif btn.objectName() in func1_btn:
                btn.setStyleSheet("background-color: rgb(220,220,220); color: rgb(100,100,100)")
                btn.clicked.connect(self.func1_clicked)

            elif btn.objectName() in func2_btn:
                btn.setStyleSheet("background-color: rgb(220,220,220); color: rgb(100,100,100)")
                btn.clicked.connect(self.func2_clicked)


    def func1_clicked(self):
        """
        memory func_clicked
        """
        sender = self.sender()
        try:
            if sender.objectName() == "mc":
                self.get_browser_data()
                self.mr = ""
            elif sender.objectName() in ["m+", "m-"]:
                self.equal_clicked()
                self.get_browser_data()
                temp3 = float(self.res[self.res.index("=")+2:])
                if self.mr == "":
                    self.mr = "M=" + str(temp3)
                else:
                    if sender.objectName() == "m+":
                        self.mr = "M=" + str(float(self.mr[self.mr.index("=")+1:])+temp3)
                    else:
                        self.mr = "M=" + str(float(self.mr[self.mr.index("=")+1:])-temp3)

            elif sender.objectName() == "mr":
                self.get_browser_data()
                if self.mr != "":
                    self.res = "= " + self.mr[self.mr.index("=")+1:]
                else:
                    self.recall = "Input error."
        except:
            self.recall = "Input error."
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)

    def func2_clicked(self):
        """
        func_clicked
        """
        sender = self.sender()
        self.equal_clicked()
        self.get_browser_data()
        if self.recall == "Input error.":
            self.recall = ""
        if self.res == "= ":
            self.input = ""
        else:
            self.input = self.res[2:]
        temp1 = 0
        temp2 = 0
        x_f = float(self.input)

        try:
            if sender.objectName() == "x!":
                if int(x_f) < 1:
                    self.recall = "Input error."
                    self.res = "= "
                else:
                    y_tmp = 1
                    for i in range(1, int(x_f)+1):
                        y_tmp = y_tmp * i
                    self.input = str(int(x_f))+"!"
                    self.res = "= " + str(y_tmp)

            elif sender.objectName() == "xˉ¹":
                if x_f == 0:
                    self.recall = "Input error."
                    self.res = "= "
                else:
                    self.input = str(x_f)+"ˉ¹"
                    self.res = "= " + str(1/x_f)

            elif sender.objectName() == "x²":
                self.input = str(x_f)+"²"
                self.res = "= " + str(x_f**2)

            elif sender.objectName() == "x³":
                self.input = str(x_f)+"³"
                self.res = "= " + str(x_f**3)

            elif sender.objectName() == "xⁿ":
                self.input_flag = "xⁿ"
                self.input = str(x_f)+"^"+"n="
                self.x_f = x_f

            elif sender.objectName() == "√x":
                if x_f < 0:
                    self.recall = "Input error."
                    self.res = "= "
                else:
                    self.input = "√"+str(x_f)
                    self.res = "= " + str(x_f**(1/2))

            elif sender.objectName() == "ⁿ√x":
                self.input_flag = "ⁿ√x"
                self.input = str(x_f)+"^"+"1/n="
                self.x_f = x_f

            elif sender.objectName() == "ln":
                if x_f <= 0:
                    self.recall = "Input error."
                    self.res = "= "
                else:
                    self.input = "ln "+str(x_f)
                    self.res = "= " + str(log(x_f))

            elif sender.objectName() == "eⁿ":
                self.input = "e^ "+str(x_f)
                self.res = "= " + str(e**x_f)

            elif sender.objectName() == "log":
                if x_f <= 0:
                    self.recall = "Input error."
                    self.res = "= "
                else:
                    self.input = "log "+str(x_f)
                    self.res = "= " + str(log10(x_f))

            elif sender.objectName() == "10ⁿ":
                self.input = "10^ "+str(x_f)
                self.res = "= " + str(10**x_f)

            elif sender.objectName() == "sin":
                self.input = "sin "+str(x_f)
                self.res = "= " + str(sin(x_f))

            elif sender.objectName() == "sinˉ¹":
                self.input = "sinˉ¹ "+str(x_f)
                self.res = "= " + str(asin(x_f))

            elif sender.objectName() == "cos":
                self.input = "cos "+str(x_f)
                self.res = "= " + str(cos(x_f))

            elif sender.objectName() == "cosˉ¹":
                self.input = "cosˉ¹ "+str(x_f)
                self.res = "= " + str(acos(x_f))

            elif sender.objectName() == "tan":
                self.input = "tan "+str(x_f)
                self.res = "= " + str(tan(x_f))

            elif sender.objectName() == "tanˉ¹":
                self.input = "tanˉ¹ "+str(x_f)
                self.res = "= " + str(atan(x_f))

            elif sender.objectName() == "Deg":
                if self.input[0:3] == "Rad":
                    self.input = "Deg "+str(temp2)
                    self.res = "= " + str(temp2/pi*180)
                else:
                    self.input = "Deg "+str(x_f)
                    temp1 = x_f/pi*180
                    self.res = "= " + str(temp1)+"°"
                sender.setObjectName("Rad")

            elif sender.objectName() == "Rad":
                if self.input[0:3] == "Deg":
                    self.input = "Rad "+str(temp1)
                    self.res = "= " + str(temp1/180*pi)
                else:
                    self.input = "Rad "+str(x_f)
                    temp2 = x_f/180*pi
                    self.res = "= " + str(temp2)
                sender.setObjectName("Deg")

            elif sender.objectName() == "lnv":
                func = [("sin", "sinˉ¹"), ("cos", "cosˉ¹"), ("tan", "tanˉ¹"), ("ln", "eⁿ"), ("log", "10ⁿ")]
                for j in range(5):
                    for i in range(2):
                        if self.findChild((QPushButton,), func[j][i]):
                            btn = self.findChild((QPushButton,), func[j][i])
                            if i == 0:
                                k = 1
                            elif i == 1:
                                k = 0
                    btn.setObjectName(func[j][k])
                    btn.setText(func[j][k])

        except:
            self.recall = "Input error."
        self.tab_widget.setCurrentIndex(0)
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)


    def num_system_onClicked(self):
        """
        num_system_onClicked
        """
        self.equal_clicked()
        self.get_browser_data()
        self.input = self.res[2:]
        if self.num_system_d.isChecked():
            self.res = "= " + self.input
            self.recall = ""
        elif self.num_system_b.isChecked():
            self.res = "= " + str(bin(int(float(self.input))))
            self.recall = "Integer part to Bin."
        elif self.num_system_h.isChecked():
            self.res = "= " + str(hex(int(float(self.input))))
            self.recall = "Integer part to Hex."
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)


    def clear_clicked(self):
        """
        "C" button_clicked
        """
        self.input = ""
        self.res = "= "
        self.recall = ""
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)


    def back_clicked(self):
        """
        "<-" button_clicked
        """
        self.get_browser_data()
        self.input = self.input[0:-1]
        if self.recall == "Input error.":
            self.recall = ""
            self.res = "= "
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)


    def input_clicked(self):
        """
        input_clicked
        """
        self.num_system_d.setChecked(True)
        self.get_browser_data()

        if self.input == "welcome":
            self.input = ""
        if self.recall == "Input error.":
            self.recall = ""
            self.res = "= "
        sender = self.sender()
        if sender.objectName() == "π":
            self.input = self.input + "3.1416"
        elif sender.objectName() == "e":
            self.input = self.input + "2.7183"
        else:
            self.input = self.input + sender.objectName()

        if sender.objectName() not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "<-", "="]:
            self.num_system_b.setEnabled(False)
            self.num_system_h.setEnabled(False)
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)



    def get_browser_data(self):
        """
        get_browser_data
        """
        text_list = self.tbrowser.toPlainText().splitlines()
        if len(text_list) == 0:
            self.input = ""
            self.res = "= "
            self.recall = ""
            self.mr = ""
        elif len(text_list) == 1:
            self.input = text_list[0]
            self.res = "= "
            self.recall = ""
            self.mr = ""
        elif len(text_list) == 2:
            self.input = text_list[0]
            self.res = text_list[1]
            self.recall = ""
            self.mr = ""
        elif len(text_list) == 3:
            self.input = text_list[0]
            self.res = text_list[1]
            self.recall = text_list[2]
            self.mr = ""
        elif len(text_list) == 4:
            self.input = text_list[0]
            self.res = text_list[1]
            self.recall = text_list[2]
            self.mr = text_list[3]


    def equal_clicked(self):
        """
        "=" button_clicked
        """
        self.get_browser_data()
        if self.input_flag in ["xⁿ", "ⁿ√x"]:
            if self.input[self.input.index("=")+1:] == "":
                self.n_f = 0
            else:
                self.n_f = float(self.input[self.input.index("=")+1:])

            if self.input_flag == "xⁿ":
                self.res = "= "+ str(self.x_f**self.n_f)
            elif self.input_flag == "ⁿ√x":
                self.res = "= "+ str(self.x_f**(1/self.n_f))
            self.input_flag = ""
            self.n_f = 0
        else:
            if self.input == "welcome":
                self.input = ""

            if self.recall == "Input error.":
                self.recall = ""
            else:
                self.input = self.input.replace("%", "/100")

            try:
                self.res = "= "+ str(eval(self.input))
                self.num_system_b.setEnabled(True)
                self.num_system_h.setEnabled(True)
            except:
                self.recall = "Input error."
        self.tbrowser.setText(self.input + "\n" + self.res + "\n" + self.recall + "\n" + self.mr)



if __name__ == "__main__":
    FONT = QFont()
    FONT.setFamily("Microsoft YaHei UI")
    FONT.setPointSize(12)
    FONT.setBold(True)

    APP = QApplication(sys.argv)
    WIN = Window(FONT)
    WIN.show()
    sys.exit(APP.exec_())
