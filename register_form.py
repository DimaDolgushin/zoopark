from PySide6.QtWidgets import QDialog, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from src.server.base.models import User
from src.client.api.session import Session


class RegisterWindow(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.__initUi()
        self.settingUi()
        self.show()

    def __initUi(self) -> None:
        self.setWindowTitle('Register')
        self.setMinimumSize(370, 225)

        self.main_v_layout = QVBoxLayout()
        self.label_lineedit_h_layout = QHBoxLayout()
        self.label_v_layout = QVBoxLayout()
        self.line_edit_v_layout = QVBoxLayout()

        self.label_login = QLabel()
        self.label_password = QLabel()
        self.label_power_level = QLabel()
        self.label_confirm = QLabel()

        self.spacer = QSpacerItem(0, 10)

        self.line_edit_login = QLineEdit()
        self.line_edit_password = QLineEdit()
        self.line_edit_power_level = QLineEdit()
        self.line_edit_confirm = QLineEdit()

        self.register_button = QPushButton()

    def settingUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.addLayout(self.label_lineedit_h_layout)
        self.label_lineedit_h_layout.addLayout(self.label_v_layout)
        self.label_lineedit_h_layout.addLayout(self.line_edit_v_layout)

        self.label_v_layout.addWidget(self.label_login)
        self.label_v_layout.addWidget(self.label_power_level)
        self.label_v_layout.addSpacerItem(self.spacer)
        self.label_v_layout.addWidget(self.label_password)
        self.label_v_layout.addWidget(self.label_confirm)

        self.line_edit_v_layout.addWidget(self.line_edit_login)
        self.line_edit_v_layout.addWidget(self.line_edit_power_level)
        self.line_edit_v_layout.addSpacerItem(self.spacer)
        self.line_edit_v_layout.addWidget(self.line_edit_password)
        self.line_edit_v_layout.addWidget(self.line_edit_confirm)

        self.main_v_layout.addWidget(self.register_button)

        self.label_login.setText("Login")
        self.label_power_level.setText("Power level")
        self.label_password.setText("Password")
        self.label_confirm.setText("Confirm")
        self.register_button.setText("Register")

        self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.line_edit_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button.clicked.connect(self.on_register_button_clicked)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return.numerator:
            self.register()

    def on_register_button_clicked(self) -> None:
        self.register()

    def data_is_valid(self) -> bool:
        if self.line_edit_password.text() != self.line_edit_confirm.text():
            self.parent().show_message(
                text="Incorrect confirm password",
                error=True,
                parent=self)
            return False

        for line in (self.line_edit_login, self.line_edit_power_level, self.line_edit_password, self.line_edit_confirm):
            if line.text() == "":
                self.parent().show_message(text="One or More fields are empty", error=True, parent=self)
                return False

            return True

    def register(self) -> None:
        if not self.data_is_valid():
            return

        user = User(
            login=self.line_edit_login.text(),
            power_level=int(self.line_edit_power_level.text()),
            password=self.line_edit_password.text()
        )

        session = Session()
        session.register(user)

        if session.error:
            return self.parent().show_message(
                text=session.error,
                error=True,
                parent=self)

        if session.auth:
            self.parent().show_message(
                text='Successful register',
                error=False,
                parent=self
            )

        self.parent().open_login_dialog()
        self.close()
