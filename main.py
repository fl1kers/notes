from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget, QPushButton, QLabel,QListWidget, \
    QLineEdit,QTextEdit, QHBoxLayout, QVBoxLayout ,QInputDialog , QMessageBox
import json

app = QApplication([])
win = QWidget()
win.setWindowTitle("Розумні замітки для розумних")
win.resize(900,600)
button1 = QPushButton("Створити Замітку")
button2 = QPushButton("Видалити Замітку")
button3 = QPushButton("Зберегти замітку")
button4 = QPushButton("Додати до замітки")
button5 = QPushButton("Відкріпити від замітки")
button6 = QPushButton("Шукати замітки по тегу")
label = QLabel("Список заміток")
label1 = QLabel("Список тегів")
list = QListWidget()
list1 = QListWidget()
teg = QLineEdit()
teg.setPlaceholderText("Введіть тег...")
tes = QTextEdit()

main_layout = QHBoxLayout()
col = QVBoxLayout()
col.addWidget(label)
col.addWidget(list)


row_1 =QHBoxLayout()
row_1.addWidget(button1)
row_1.addWidget(button2)
col.addWidget(button3)
col.addLayout(row_1)

col.addWidget(label1)
col.addWidget(list1)
col.addWidget(teg)

row_2 =QHBoxLayout()
row_2.addWidget(button4)
row_2.addWidget(button5)
col.addWidget(button6)
col.addLayout(row_2)


main_layout.addWidget(tes, stretch=2)
main_layout.addLayout(col, stretch=1)
win.setLayout(main_layout)

def show_note():
    key = list.selectedItems()[0].text()
    tes.setText(notes[key]['текст'])
    list1.clear()
    list1.addItems(notes[key]["теги"])


def add_note():
    name, ok = QInputDialog.getText(win, "Додати замітку", "Уведіть назву замітки:")
    if ok and name != "":
        notes[name] = {"текст": "", "теги": []}
        list.addItem(name)

def save_note():
    if list.selectedItems():
        key = list.selectedItems()[0].text()
        notes[key]["текст"] = tes.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes,file,sort_keys = True)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def del_note():
    if list.selectedItems():
        box = QMessageBox(text="Ви дійсно хочете вдалити замітку?")
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if box.exec() == QMessageBox.Ok:
            key = list.selectedItems()[0].text()
            del notes[key]
            tes.clear()
            list.clear()
            list.addItems(notes)
            list1.clear()
            with open("notes_data.json", "w")as file:
                json.dump(notes,file, sort_keys=True)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def add_tag():
    if list.selectedItems():
        key = list.selectedItems()[0].text()
        tag = teg.text()
        if tag != "" and not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list1.clear()
            list1.addItems(notes[key]["теги"])
            teg.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes,file,sort_keys=True)
    else:
        QMessageBox(text="Замітка не обрана").exec_()
    
def del_tag():
    if list.selectedItems() and list1.selectedItems():
        key = list.selectedItems()[0].text()
        tag = list1.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list1.clear()
        list1.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def search_tag():
    tag = teg.text()
    if button6.text() == "Шукати замітки по тегу" and tag != "":
        notes_filered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filered[note] = notes[note]
        list.clear()
        list.addItems(notes_filered)
        list1.clear()
        button6.setText("Скинути пошук")
    elif button6.text() == "Скинути пошук":
        list.clear()
        list.addItems(notes)
        list1.clear()
        teg.clear()
        button6.setText("Шукати замітки по тегу")

list.itemClicked.connect(show_note)
button1.clicked.connect(add_note)
button3.clicked.connect(save_note)
button2.clicked.connect(del_note)
button4.clicked.connect(add_tag)
button5.clicked.connect(del_tag)
button6.clicked.connect(search_tag)

win.show()



with open("notes_data.json", "r") as file:
    notes =json.load(file)
list.addItems(notes)
app.exec_()