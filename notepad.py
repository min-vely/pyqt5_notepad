import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QStatusBar, QFontDialog)
from PyQt5.QtGui import QIcon

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.initUI()

    def initUI(self):
        # 중앙 텍스트 편집 위젯 설정
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # 메뉴바 생성
        self.create_menu_bar()

        # 상태바 생성
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('준비')

        # 윈도우 설정
        self.setWindowTitle('메모장')
        self.setGeometry(300, 300, 800, 600)
        self.show()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # 파일 메뉴
        file_menu = menu_bar.addMenu('&파일')

        new_action = QAction('새 파일', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('열기', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('저장', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('다른 이름으로 저장...', self)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction('끝내기', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 편집 메뉴
        edit_menu = menu_bar.addMenu('&편집')

        undo_action = QAction('실행 취소', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('다시 실행', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction('잘라내기', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('복사', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('붙여넣기', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()

        font_action = QAction('글꼴...', self)
        font_action.triggered.connect(self.show_font_dialog)
        edit_menu.addAction(font_action)


        # 보기 메뉴
        view_menu = menu_bar.addMenu('&보기')
        
        toggle_status_bar_action = QAction('상태 표시줄', self, checkable=True)
        toggle_status_bar_action.setChecked(True)
        toggle_status_bar_action.triggered.connect(self.toggle_status_bar)
        view_menu.addAction(toggle_status_bar_action)


    def new_file(self):
        self.text_edit.clear()
        self.current_file = None
        self.statusBar.showMessage('새 파일이 생성되었습니다')

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 열기", "", "텍스트 파일 (*.txt);;모든 파일 (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
                self.current_file = file_name
                self.statusBar.showMessage(f'열림: {file_name}')
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 열 수 없습니다: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.statusBar.showMessage(f'저장됨: {self.current_file}')
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 저장할 수 없습니다: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "다른 이름으로 저장", "", "텍스트 파일 (*.txt);;모든 파일 (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.current_file = file_name
                self.statusBar.showMessage(f'다른 이름으로 저장됨: {file_name}')
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 저장할 수 없습니다: {e}")

    def toggle_status_bar(self, state):
        if state:
            self.statusBar.show()
        else:
            self.statusBar.hide()
            
    def show_font_dialog(self):
        font, ok = QFontDialog.getFont(self.text_edit.currentFont(), self)
        if ok:
            self.text_edit.setCurrentFont(font)

    def closeEvent(self, event):
        # 앱을 닫기 전에 변경사항 저장 여부 확인
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(self, '메시지',
                        "종료하시겠습니까? 저장되지 않은 작업은 손실됩니다.", QMessageBox.Yes |
                        QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())