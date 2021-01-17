# -*- coding: utf-8 -*-
import itertools
import random
import sys
from PyQt5 import QtWidgets
from GuiDesign import Ui_MainWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from ThreadDraw import ThreadDraw

class MainClassGUI(Ui_MainWindow,ApplicationContext):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)

        self.pushButton.clicked.connect(self.buttonClickStart)
        self.textEdit.textChanged.connect(self.changeText)
        self.thread_start_draw = ThreadDraw()
        self.path = self.get_resource("config.conf")

        self.ins_username = ""
        self.ins_password = ""
        self.link = ""
        self.number_of_person_in_comment = ""
        self.max_number_of_comment = ""
        self.word_in_comment = ""
        self.comment_combinations = ""
        self.telegram_name = ""

        self.readConf()

    def readConf(self):
        import json
        f = open(self.path, "r")
        data = json.load(f)

        self.lineEdit.setText(data['username'])
        self.lineEdit_2.setText(data['password'])
        self.lineEdit_3.setText(data['link'])
        self.spinBox.setValue(int(data['count_person']))
        self.lineEdit_4.setText(data['max_number_of_comment'])
        self.lineEdit_5.setText(data['word_in_comment'])
        self.lineEdit_7.setText(data['telegram_name'])

        prs=""
        for i in data['persons']:
            prs = prs + i + "\n"
            self.textEdit.setText(prs)

        self.textEdit.setText(self.textEdit.toPlainText().strip())

    def createValues(self):
        self.ins_username = self.lineEdit.text()
        self.ins_password = self.lineEdit_2.text()
        self.link = self.lineEdit_3.text()
        self.number_of_person_in_comment = self.spinBox.value()
        self.max_number_of_comment = self.lineEdit_4.text()
        self.word_in_comment = self.lineEdit_5.text()
        self.telegram_name = self.lineEdit_7.text()

        persons = []
        for person in self.textEdit.toPlainText().strip().split('\n'):
            persons.append("@"+person)

        self.comment_combinations = list(itertools.combinations(persons,self.number_of_person_in_comment ))
        random.shuffle(self.comment_combinations)

        self.textEdit_3.setText("")
        for i in self.comment_combinations:
            self.textEdit_3.setText(self.textEdit_3.toPlainText()+str(i)+"\n")

    def changeText(self):
        nmb_prs = self.textEdit.toPlainText().strip().split('\n')
        self.label_9.setText("Kişi Sayısı: " + str(len(nmb_prs)))

    def buttonClickStart(self):
        print("Butona basıldı.")

        self.createValues()
        self.label_8.setText("Yorum sayısı: "+str(len(self.comment_combinations)))
        self.pushButton.setEnabled(False)

        self.thread_start_draw.change_value_information_process_output.connect(self.process_output)

        self.thread_start_draw.ins_username = self.ins_username
        self.thread_start_draw.ins_password = self.ins_password
        self.thread_start_draw.link = self.link
        self.thread_start_draw.number_of_person_in_comment = self.number_of_person_in_comment
        self.thread_start_draw.max_number_of_comment = self.max_number_of_comment
        self.thread_start_draw.word_in_comment = self.word_in_comment
        self.thread_start_draw.comment_combinations = self.comment_combinations
        self.thread_start_draw.telegram_name = self.telegram_name

        self.thread_start_draw.start()

    def process_output(self,val):
        print(val)
        self.textEdit_2.setText(self.textEdit_2.toPlainText()+str(val)+"\n")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainClassGUI()
    ui.MainWindow.show()
    sys.exit(app.exec_())