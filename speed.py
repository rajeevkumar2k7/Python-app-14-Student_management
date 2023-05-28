import PyQt6.QtWidgets as qt
import sys, os


class SpeedCalculate(qt.QWidget):
    def __init__(self):
        super().__init__()

        grid = qt.QGridLayout()

        distance_label = qt.QLabel("Distance travel:")
        self.distance_text = qt.QLineEdit()
        #metrics = qt.QListWidget()
        #metrics.addItem(['KM', 'Miles'])

        time_lable = qt.QLineEdit("Time in hrs:")
        self.time_text = qt.QLineEdit()

        calculate_button = qt.QPushButton("Click to know speed")
        calculate_button.clicked.connect(self.calculate)
        self.output_label = qt.QLabel("")

        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_text,0,1)
        #grid.addWidget(metrics,0,2)
        grid.addWidget(time_lable,1,0)
        grid.addWidget(self.time_text, 1,1)
        grid.addWidget(calculate_button,2,0,1,2)
        grid.addWidget(self.output_label, 3,0,1,3)
    
        self.setLayout(grid)

    def calculate(self):
        speed = int(self.distance_text.text())/int(self.time_text.text())
        self.output_label.setText(f'Your speed is {speed} Km/hr')


app = qt.QApplication(sys.argv)
calculate_speed = SpeedCalculate()
calculate_speed.show()
sys.exit(app.exec())
