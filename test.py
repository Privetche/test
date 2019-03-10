# -*- coding: utf-8 -*-
from datetime import date
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
import mysql.connector
import pandas as pd
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

def main():

    Qt = QtCore.Qt
    def restart_app():
        os.system("scratch_2.py")
        sys.exit()

    class PandasModel(QtCore.QAbstractTableModel):

        def __init__(self, data, parent=None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self.data = data
            self._data = self.data.copy(deep=True)

        def rowCount(self, parent=None):
            return len(self._data.values)

        def columnCount(self, parent=None):
            return self._data.columns.size

        def data(self, index, role=Qt.DisplayRole):
            if index.isValid():
                if role == Qt.DisplayRole:
                    return QtCore.QVariant(unicode(str(
                        self.data.values[index.row()][index.column()])))
            return QtCore.QString()

        def headerData(self, col, orientation, role):
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self._data.columns[col]

        def reset_filter(self):
            self.data = self._data.copy(deep=True)

        def filter_data(self):
            self.data = self._data.copy(deep=True)
            value1 = unicode(str(box1.text()))
            value2 = unicode(str(box2.text()))
            value3 = unicode(str(box3.text()))
            value4 = unicode(str(box4.text()))
            value5 = unicode(str(box5.text()))
            value6 = unicode(str(box6.text()))
            value7 = unicode(str(box7.text()))
            value8 = unicode(str(box8.text()))
            self.data = self.data[self.data[u'Фамилия'].str.contains(value1)]
            self.data = self.data[self.data[u'Имя'].str.contains(value2)]
            self.data = self.data[self.data[u'Отчество'].str.contains(value3)]
            self.data = self.data[self.data[u'Дата рождения'].str.contains(value4)]
            self.data = self.data[self.data[u'Серия полиса'].str.contains(value5)]
            self.data = self.data[self.data[u'Номер полиса'].str.contains(value6)]
            self.data = self.data[self.data[u'Серия документа'].str.contains(value7)]
            self.data = self.data[self.data[u'Номер документа'].str.contains(value8)]
            # return df
            print(self.data)
    def get_data():

        def calculate_age(born):
            today = date.today()
            return str(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
        def birthdate_string(birthdate):
            birthdate = birthdate.strftime("%m.%d.%Y")
            return birthdate

        try:
            try:
                with open("config.txt") as file:
                    array = [row.strip() for row in file]
                cnx = mysql.connector.connect(user=array[0], password=array[1],
                                              host=array[2],
                                              database=array[3],
                                              auth_plugin='mysql_native_password',
                                              use_unicode=True, charset="utf8")
                cursor = cnx.cursor()
                query = (
                    "SELECT firstName, lastName, patrName, birthDate, sex, endDate, policyKind_id, clientpolicy.serial, clientpolicy.number, documentType_id, clientdocument.serial, clientdocument.number FROM client inner join clientdocument on client.id=clientdocument.client_id inner join clientpolicy on client.id=clientpolicy.client_id;")
                columns = (
                    u'Имя', u'Фамилия', u'Отчество', u'Дата рождения', u'Пол', 'endDate', u'Тип полиса',
                    u'Серия полиса',
                    u'Номер полиса', u'Тип документа', u'Серия документа', u'Номер документа')
                cursor.execute(query)
                data = cursor.fetchall()
                df = pd.DataFrame(data=data, columns=columns)
                df[u'Пол'].replace(2, 'женский', inplace=True)
                df[u'Пол'].replace(1, 'мужской', inplace=True)
                df[u'Тип полиса'].replace(1, 'временный', inplace=True)
                df[u'Тип полиса'].replace(2, 'старый', inplace=True)
                df[u'Тип полиса'].replace(3, 'новый', inplace=True)
                df[u'Тип документа'].replace(1, 'паспорт', inplace=True)
                df[u'Тип документа'].replace(1, 'свидетельство о рождении', inplace=True)
                df[u'Возраст'] = df[u'Дата рождения'].apply(calculate_age)
                df[u'Дата рождения'] = df[u'Дата рождения'].apply(birthdate_string)
                df = df[
                    [u'Фамилия', u'Имя', u'Отчество', u'Дата рождения', u'Возраст', u'Пол', u'Тип полиса',
                     u'Серия полиса',
                     u'Номер полиса', u'Тип документа', u'Серия документа', u'Номер документа']]
                pd.set_option('display.max_columns', None)
                cnx.close()
                cursor.close()
                return df
            except IOError:
                f = open("config.txt", "w+")
                f.truncate(0)
                f.write("login"'\n'"password"'\n'"127.0.0.1"'\n'"databaseName")
                f.close()
                restart_app()
        except (mysql.connector.errors.ProgrammingError,mysql.connector.errors.NotSupportedError,IndexError):

            def connection_retry():
                msgbox.close()
                connection_window()

            application = QtGui.QApplication(sys.argv)
            msgbox = QtGui.QWidget()
            msgbox.resize(290, 100)
            msgbox.setWindowTitle('Error')
            label = QtGui.QLabel(u'Возникла ошибка при подключении базы данных', msgbox)
            label.move(20, 30)
            button=QtGui.QPushButton("OK", msgbox)
            #msgbox.connect(QtGui.QPushButton('OK'), QtCore.SIGNAL('clicked()'), connection_window)
            button.move(100, 60)
            QObject.connect(button, SIGNAL('clicked()'), connection_retry)
            msgbox.show()
            application.exec_()

    def connection_window():

        window2 = QtGui.QDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        window2.resize(400, 200)
        window2.setWindowTitle(u'Подключить БД')
        label1 = QtGui.QLabel('User', window2)
        label1.move(30, 30)
        label1 = QtGui.QLabel('Password', window2)
        label1.move(30, 60)
        label1 = QtGui.QLabel('Host', window2)
        label1.move(30, 90)
        label1 = QtGui.QLabel('Database', window2)
        label1.move(30, 120)

        input1 = QtGui.QLineEdit(window2)
        input1.move(100, 27)
        input2 = QtGui.QLineEdit(window2)
        input2.move(100, 57)
        input3 = QtGui.QLineEdit(window2)
        input3.move(100, 87)
        input3.setText('127.0.0.1')
        input4 = QtGui.QLineEdit(window2)
        input4.move(100, 117)

        def edit_config():
            with open("config.txt", 'w') as file:
                file.truncate(0)
                file.write(str(input1.text() + '\n'))
                file.write(str(input2.text() + '\n'))
                file.write(str(input3.text() + '\n'))
                file.write(str(input4.text()))
            window2.close()
            try:
                widget.close()
            except Exception:
                sys.exc_clear()
            restart_app()

        button = QtGui.QPushButton(u"Подключить БД", window2)
        button.move(285, 75)
        QObject.connect(button, SIGNAL('clicked()'), edit_config)
        response = window2.exec_()


    # print (get_data())
    df = get_data()
    print(df.info())
    Qt = QtCore.Qt
    application = QtGui.QApplication(sys.argv)
    widget = QtGui.QWidget()
    widget.resize(900, 550)
    widget.setWindowTitle(u'Пациенты')
    view = QtGui.QTableView(widget)
    view.resize(900, 285)
    model = PandasModel(df)
    view.setModel(model)

    lbl1 = QtGui.QLabel(u'Фамилия', widget)
    lbl1.move(35, 310)
    lbl2 = QtGui.QLabel(u'Имя', widget)
    lbl2.move(35, 335)
    lbl3 = QtGui.QLabel(u'Отчество', widget)
    lbl3.move(35, 360)
    lbl4 = QtGui.QLabel(u'Дата рождения', widget)
    lbl4.move(35, 385)
    lbl5 = QtGui.QLabel(u'Серия полиса', widget)
    lbl5.move(35, 410)
    lbl6 = QtGui.QLabel(u'Номер полиса', widget)
    lbl6.move(35, 435)
    lbl7 = QtGui.QLabel(u'Серия документа', widget)
    lbl7.move(35, 460)
    lbl8 = QtGui.QLabel(u'Номер документа', widget)
    lbl8.move(35, 485)

    box1 = QtGui.QLineEdit(widget)
    box1.move(150, 306)
    box2 = QtGui.QLineEdit(widget)
    box2.move(150, 331)
    box3 = QtGui.QLineEdit(widget)
    box3.move(150, 356)
    box4 = QtGui.QLineEdit(widget)
    box4.move(150, 381)
    box5 = QtGui.QLineEdit(widget)
    box5.move(150, 406)
    box6 = QtGui.QLineEdit(widget)
    box6.move(150, 431)
    box7 = QtGui.QLineEdit(widget)
    box7.move(150, 456)
    box8 = QtGui.QLineEdit(widget)
    box8.move(150, 481)

    button1 = QtGui.QPushButton(u"Отфильтровать", widget)
    button1.move(500, 360)
    button2 = QtGui.QPushButton(u"Сбросить фильтр", widget)
    button2.move(500, 400)
    button3 = QtGui.QPushButton(u"Подключение БД", widget)
    button3.move(500, 440)
    QObject.connect(button1, SIGNAL('clicked()'), model.filter_data)
    QObject.connect(button2, SIGNAL('clicked()'), model.reset_filter)
    QObject.connect(button3, SIGNAL('clicked()'), connection_window)

    widget.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    while True:
        main()