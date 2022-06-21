import sys
from PyQt6 import QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QMainWindow,QFileDialog
import os
import glob
from mark import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
import shutil

class MyPyQT_Form(QMainWindow,Ui_MainWindow):
    def __init__(self):
        """
        初始化
        """
        self.file_num = 0
        self.number = 0
        self.filename = ""
        self.change_name = ""
        self.out_dir = ""
        self.image_dir = ""
        self.img_arr = []
        super().__init__()
        self.setupUi(self)
        self.showImage.setStyleSheet("border: 2px solid blue")
        # 定时器：30ms捕获一帧
        # self._timer = QtCore.QTimer(self)
        # self._timer.timeout.connect(self._queryFrame)
        # self._timer.setInterval(30)

    def get_input(self):
        self.change_name= self.QTinput.text() + '.jpg'
        self.QToutput.clear()
        self.QToutput.append("<h2>照片的位置为：</h2>")
        self.QToutput.append("{:s}".format(self.out_dir))
        self.QToutput.append("<h2>照片的名字为：</h2>")
        self.QToutput.append("{:s}".format(self.change_name))
            # print(2)




    def confirm_imf(self):
        if self.out_dir == "" or self.image_dir == "":
            QMessageBox.information(self,"提示","请选择文件夹")
            return
        else:
            #self.mycopyfile(self.img_arr[self.number],self.out_dir)
            try:
                shutil.copy(self.img_arr[self.number], self.out_dir )
                os.rename(self.out_dir +"/" +  os.path.basename(self.img_arr[self.number]), os.path.join(self.out_dir,self.change_name))
                with open(os.path.join(self.out_dir, "label.txt"), mode="a+", encoding="utf-8") as f:
                    f.write(self.out_dir + '\t' + self.change_name + '\n')

                self.next_img()
            except:
                self.next_img()
                pass

    def next_img(self):
        if self.number >= self.file_num:
            QMessageBox.information(self, "提示", "图片读取完毕")
            return
        print(self.img_arr[self.number])
        self.number += 1
        p = QPixmap(self.img_arr[self.number])
        self.showImage.setPixmap(p)
        self.showImage.setStyleSheet("border: 2px solid blue")
        self.showImage.setScaledContents(True)
        self.QToutput.clear()
        self.QTinput.clear()


    def delete(self):
        choice = QMessageBox.question(self.confirm_input, "确认", "确认要删除该照片吗？",QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            os.remove(self.img_arr[self.number])
            self.next_img()

    def select_image_dir(self):
        self.number = 0
        self.image_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "")
        self.file_num = len(os.listdir(self.image_dir))
        self.img_arr = []
        for filename in os.listdir(self.image_dir):
            self.img_arr.append(os.path.join(self.image_dir,filename))

        # 当窗口非继承QtWidgets.QDialog时，self可替换成 None

    def select_image_out(self):
        self.out_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "")
        with open(os.path.join(self.out_dir, "label.txt"),mode="w",encoding="utf-8") as f:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec())