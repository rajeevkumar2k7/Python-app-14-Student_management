import PyQt6.QtWidgets as qt
import PyQt6.QtCore as QC
import PyQt6.QtGui as qa
import sys
import mysql.connector as ms
import os

sql_pwd = os.environ.get('MYSQL_PASS')


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        # Design Main window screen #
        # Set Title of the APP
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 500)

        # Add menu item
        file_menu_item = self.menuBar().addMenu('&File')    
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        # Add action item under menu item
        add_student_action = qa.QAction(qa.QIcon('icons/add.png'),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = qa.QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)  

        search_action = qa.QAction(qa.QIcon('icons/search.png'),'Search', self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Add toolbar
        toolbar = qt.QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
   
        # Create table on main window
        self.table = qt.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Add status bar
        self.status_bar = qt.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.table.cellClicked.connect(self.cell_clicked)

        
    def load_data(self):
        '''This function load data on main window table'''
        connection = ms.connect(host='localhost', user='root', password=sql_pwd, 
                                database = 'StudentManagement')
        
        my_cursor = connection.cursor()
        query = 'select * from Students'
        my_cursor.execute(query)
        result = my_cursor.fetchall()

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_no, data in enumerate(row_data):
                self.table.setItem(row_number, column_no, qt.QTableWidgetItem(str(data)))
    
    def cell_clicked(self):
        edit_button = qt.QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)
        
        delete_button = qt.QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)
        
        children = self.findChildren(qt.QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
    
    def search(self):
        dialog = SearchDialog()
        dialog.exec()
    
    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()
    
    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class EditDialog(qt.QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Update Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = qt.QVBoxLayout()

        # Get student name form selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        self.student_id = main_window.table.item(index, 0).text()

        self.student_name = qt.QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Get course name from selected row
        course_name = main_window.table.item(index, 2).text()
        self.course_name = qt.QComboBox()
        courses = ['Biolology', 'Maths', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile no
        mobile = main_window.table.item(index, 3).text()
        self.mobile = qt.QLineEdit(mobile)
        self.mobile.setPlaceholderText("mobile")
        layout.addWidget(self.mobile)



        button = qt.QPushButton('Update')
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = ms.connect(host='localhost', user='root', password=sql_pwd, database='StudentManagement')
        my_cursor = connection.cursor()
        query = 'UPDATE students SET name = %s, course = %s , mobile = %s WHERE ID = %s'
        value = (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()), 
                 self.mobile.text(), self.student_id)
        my_cursor.execute(query, value)
        connection.commit()
        main_window.load_data()
    

class DeleteDialog(qt.QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Delete Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = qt.QVBoxLayout()

        # Get student name form selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        self.student_id = main_window.table.item(index, 0).text()

        self.student_name = qt.QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Get course name from selected row
        course_name = main_window.table.item(index, 2).text()
        self.course_name = qt.QComboBox()
        courses = ['Biolology', 'Maths', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile no
        mobile = main_window.table.item(index, 3).text()
        self.mobile = qt.QLineEdit(mobile)
        self.mobile.setPlaceholderText("mobile")
        layout.addWidget(self.mobile)



        button = qt.QPushButton('Delete')
        button.clicked.connect(self.delete_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def delete_student(self):
        connection = ms.connect(host='localhost', user='root', password=sql_pwd, database='StudentManagement')
        my_cursor = connection.cursor()
        query = 'DELETE FROM students WHERE name = %s AND course = %s AND mobile = %s AND ID = %s'
        value = (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()), 
                 self.mobile.text(), self.student_id)
        my_cursor.execute(query, value)
        connection.commit()
        main_window.load_data()


class InsertDialog(qt.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = qt.QVBoxLayout()

        self.student_name = qt.QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = qt.QComboBox()
        courses = ['Biolology', 'Maths', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = qt.QLineEdit()
        self.mobile.setPlaceholderText("mobile")
        layout.addWidget(self.mobile)



        button = qt.QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        connection = ms.connect(host='localhost', user='root', 
                                   password=sql_pwd, database='StudentManagement')
        my_cursor = connection.cursor()

        query = 'INSERT INTO Students(name, course, mobile) VALUES (%s, %s, %s)'
        value = (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()), 
                 self.mobile.text())

        my_cursor.execute(query, value)
        connection.commit()
        main_window.load_data()
           
    
class SearchDialog(qt.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search the Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = qt.QVBoxLayout()

        self.student_name = qt.QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        button = qt.QPushButton()
        button.setText('Search')
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)


    def search(self):
        name = self.student_name.text()
        value = []
        value.append(name)

        connection = ms.connect(host='localhost', user='root', password=sql_pwd, 
                                database='StudentManagement')
        my_cursor = connection.cursor()
        query = 'SELECT * FROM students WHERE Name = %s'
        my_cursor.execute(query, value)
        result = my_cursor.fetchall()
        print(result)

        items = main_window.table.findItems(name, QC.Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        
        my_cursor.close()
        connection.close()


class AboutDialog(qt.QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content='This app is built to practice purpose. Feel free to make any changes'
        self.setText(content)



app = qt.QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())