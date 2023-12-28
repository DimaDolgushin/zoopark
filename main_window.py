from PySide6 import QtWidgets, QtCore, QtGui
from src.client.login_form import LoginWindow
from src.client.register_form import RegisterWindow
from src.client.api.session import Session
from src.server.base.models import User
from src.client.api import resolvers
from src.client.tools import get_pixmap_path
import threading
from src.client.zoo_add import AddZoo


session: Session = Session()
main_win = None


def include_widgets_by_pl(element: dict[str, QtWidgets.QWidget]):
    global session

    for key, item in element.items():
        if not issubclass(type(item), QtWidgets.QWidget):
            continue

        if item.property('power_level') is not None:
            item.show() if session.user.power_level >= item.property('power_level') else item.hide()

        include_widgets_by_pl(item.__dict__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        try:
            if type(self.__connect_check()) == dict:
                self.show_message(
                    text='Server not available',
                    error=True,
                    parent=self)
        except TypeError:
            pass

        self.__initUi()
        self.__setupUi()
        self.show()

    @resolvers.server_available
    def __connect_check(self, answer: dict | None) -> None:
        return

    def __initUi(self) -> None:
        self.central_widget = QtWidgets.QWidget()
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.page_list = PageListMenu()
        # self.zoo_list = ZooList()
        self.user_list = UserList()
        self.widget_container = QtWidgets.QWidget()
        self.widget_container_layout = QtWidgets.QVBoxLayout()
        self.authorization_menu = AuthorizationMenu()
        self.user_profile = UserProfile()

    def __setupUi(self) -> None:
        self.resize(930, 615)
        self.setWindowTitle('Zoo Client')
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_h_layout)
        self.widget_container.setLayout(self.widget_container_layout)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_container_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # self.page_list.zoo_item.bind_widget(self.zoo_list)
        self.page_list.user_item.bind_widget(self.user_list)

        self.main_h_layout.addWidget(self.page_list)
        self.main_h_layout.addWidget(self.widget_container)
        self.main_h_layout.addWidget(self.authorization_menu)
        self.main_h_layout.addWidget(self.user_profile)

        include_widgets_by_pl(self.__dict__)
        global main_win
        main_win = self
        self.user_profile.hide()

    def leave(self):
        self.authorization_menu.show()
        self.user_profile.hide()
        include_widgets_by_pl(self.__dict__)

    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        messagebox = QtWidgets.QMessageBox(self if not parent else parent)
        messagebox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        messagebox.setWindowTitle("Error" if error else "Information")
        messagebox.setText(text)
        messagebox.setIcon(QtWidgets.QMessageBox.Icon.Critical if error else QtWidgets.QMessageBox.Icon.Information)
        messagebox.show()

    def set_session(self, new_session: Session):
        global session
        session = new_session
        self.authorization()

    def authorization(self):
        self.authorization_menu.hide()
        self.user_profile.show()
        self.user_profile.fill_line_edits()
        include_widgets_by_pl(self.__dict__)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        exit()


class ZooList(QtWidgets.QWidget):
    add_zoo_signal = QtCore.Signal(str, str, str)
    stop_flag: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.tool_h_layout = QtWidgets.QHBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.create_zoo_button = QtWidgets.QPushButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_h_layout.setContentsMargins(0, 10, 0, 0)
        self.tool_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.main_v_layout.addLayout(self.tool_h_layout)
        self.tool_h_layout.addWidget(self.create_zoo_button)
        self.main_v_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        self.create_zoo_button.setIcon(QtGui.QPixmap(get_pixmap_path('add.png')))
        self.create_zoo_button.setFixedSize(24, 24)
        self.create_zoo_button.setProperty('power_level', 2)

        self.create_zoo_button.clicked.connect(self.create_zoo)
        self.add_zoo_signal.connect(self.add_zoo_slot)

        self.update_zoos()

    def create_zoo(self) -> None:
        AddZoo(self)

    def update_zoos(self) -> None:
        self.clear_zoos()
        threading.Thread(target=self.load_zoos).start()

    def load_zoos(self):
        for zoo in resolvers.get_all_zoos()["result"]:
            if self.stop_flag:
                exit()

            city = resolvers.get_city_by_id()


class ZooItem(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()



class UserList(QtWidgets.QWidget):
    add_zoo_signal = QtCore.Signal(str, str, int)
    stop_flag: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.tool_h_layout = QtWidgets.QHBoxLayout()

    def __setupUi(self) -> None:
        self.resize(930, 615)


class PageListMenu(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.zoo_item = MenuItem()
        self.user_item = MenuItem()

    def __setupUi(self) -> None:
        self.setMaximumWidth(150)
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_v_layout.setContentsMargins(5, 5, 5, 5)
        self.opened_widget = self.zoo_item

        self.zoo_item.setup('zoo.png', 'Zoo')
        self.user_item.setup('user.png', 'Users')

        self.main_v_layout.addWidget(self.zoo_item)
        self.main_v_layout.addWidget(self.user_item)

        self.zoo_item.setProperty('power_level', 0)
        self.user_item.setProperty('power_level', 1)


class MenuItem(QtWidgets.QFrame):
    connection_def = None
    widget: QtWidgets.QWidget = None

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.container_widget = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QHBoxLayout()
        self.icon = QtWidgets.QLabel()
        self.title = QtWidgets.QLabel()

    def __setupUi(self) -> None:
        self.setLayout(self.main_h_layout)
        self.main_h_layout.addWidget(self.container_widget)
        self.container_widget.setLayout(self.container_layout)
        self.main_h_layout.setContentsMargins(5, 5, 5, 5)
        self.container_layout.setContentsMargins(5, 5, 5, 5)

        self.title.setStyleSheet('color: black')

        self.container_layout.addWidget(self.icon)
        self.container_layout.addWidget(self.title)
        self.icon.setFixedSize(32, 32)

    def setup(self, icon_name: str, title: str):
        self.set_title(title)
        self.set_icon(icon_name)

    def set_icon(self, icon_name: str):
        self.icon.setPixmap(QtGui.QPixmap(get_pixmap_path(icon_name)))

    def set_title(self, title: str) -> None:
        self.title.setText(title)

    def bind_widget(self, widget: QtWidgets.QWidget):
        self.widget = widget

    def on_mouse_enter(self):
        self.setStyleSheet('QFrame{background-color: darkgray; border-radius: 15px}')
        self.title.setStyleSheet('color: white')

    def on_mouse_leave(self):
        self.setStyleSheet('QFrame{background-color: none; border-radius: 15px}')
        self.title.setStyleSheet('color: black')

    def on_mouse_clicked(self):
        if self.connection_def:
            self.connection_def()

    def connect_function(self, foo):
        self.connection_def = foo

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        self.on_mouse_enter()

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.on_mouse_leave()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.on_mouse_clicked()

    def switch_page(self):
        for item in self.parent().__dict__:
            page: MenuItem = self.parent().__dict__[item]

            if type(page) == MenuItem:
                page.widget.show() if page == self else page.widget.hide()


class AuthorizationMenu(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.login_button = QtWidgets.QPushButton()
        self.register_button = QtWidgets.QPushButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.setMaximumWidth(120)

        self.main_v_layout.addWidget(self.login_button)
        self.main_v_layout.addWidget(self.register_button)

        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.login_button.setText('Login')
        self.register_button.setText('Register')

        self.login_button.clicked.connect(self.on_login_click)
        self.register_button.clicked.connect(self.on_register_click)

    def on_login_click(self) -> None:
        self.open_login_dialog()

    def on_register_click(self) -> None:
        self.open_register_dialog()

    def open_login_dialog(self):
        LoginWindow(self.parent().parent())  # Надеюсь увидеть этот комментарий и всё-таки отрефакторить код

    def open_register_dialog(self):
        RegisterWindow(self)

    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        self.parent().parent().show_message(
            text=text,
            error=error,
            parent=parent
        )


class UserProfile(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()

        self.login_layout = QtWidgets.QHBoxLayout()
        self.password_layout = QtWidgets.QHBoxLayout()
        self.confirm_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.login_label = QtWidgets.QLabel()
        self.password_label = QtWidgets.QLabel()
        self.confirm_password_label = QtWidgets.QLabel()
        self.power_level_label = QtWidgets.QLabel()

        self.login_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit = QtWidgets.QLineEdit()
        self.confirm_password_line_edit = QtWidgets.QLineEdit()

        self.edit_button = QtWidgets.QPushButton()
        self.allow_button = QtWidgets.QPushButton()
        self.clear_button = QtWidgets.QPushButton()

        self.spacer = QtWidgets.QSpacerItem(0, 10)

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.setMaximumWidth(250)
        self.main_v_layout.addLayout(self.login_layout)
        self.main_v_layout.addSpacerItem(self.spacer)
        self.main_v_layout.addLayout(self.password_layout)
        self.main_v_layout.addLayout(self.confirm_layout)
        self.main_v_layout.addWidget(self.power_level_label)
        self.main_v_layout.addSpacerItem(self.spacer)
        self.main_v_layout.addLayout(self.button_layout)

        self.login_layout.addWidget(self.login_label)
        self.password_layout.addWidget(self.password_label)
        self.confirm_layout.addWidget(self.confirm_password_label)

        self.login_layout.addWidget(self.login_line_edit)
        self.password_layout.addWidget(self.password_line_edit)
        self.confirm_layout.addWidget(self.confirm_password_line_edit)

        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.allow_button)
        self.button_layout.addWidget(self.clear_button)

        self.edit_button.setText('Edit')
        self.allow_button.setText('Allow')
        self.clear_button.setText('Leave')

        self.login_label.setText('Login:')
        self.password_label.setText('Password:')
        self.confirm_password_label.setText('Confirm:')
        self.power_level_label.setText('Power level: 0')

        self.login_line_edit.setFixedWidth(150)
        self.password_line_edit.setFixedWidth(150)
        self.confirm_password_line_edit.setFixedWidth(150)

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.set_line_edit_enable(False)

        self.allow_button.setEnabled(False)

        self.clear_button.setEnabled(True)

        self.edit_button.clicked.connect(self.on_edit_click)
        self.allow_button.clicked.connect(self.on_allow_click)
        self.clear_button.clicked.connect(self.on_clear_click)

    def set_line_edit_enable(self, enabled: bool) -> None:
        self.login_line_edit.setEnabled(enabled)
        self.password_line_edit.setEnabled(enabled)
        self.confirm_password_line_edit.setEnabled(enabled)

    def fill_line_edits(self) -> None:
        global session
        self.login_line_edit.setText(session.user.login)
        self.password_line_edit.setText(session.user.password)
        self.power_level_label.setText(f'Power level: {str(session.user.power_level)}')

    def on_edit_click(self) -> None:
        self.edit_button.setEnabled(False)
        self.allow_button.setEnabled(True)
        self.set_line_edit_enable(True)

    def on_clear_click(self) -> None:
        session.clear()
        main_win.leave()

    def validate_password(self) -> bool:
        global session
        return self.confirm_password_line_edit.text() == self.password_line_edit.text()

    def on_allow_click(self) -> None:
        global session

        if not self.validate_password():
            return self.parent().parent().show_message(
                text='Incorrect confirm password',
                error=True,
                parent=self
            )

        user = User(
            id=session.user.id,
            login=self.login_line_edit.text(),
            password=self.password_line_edit.text(),
            power_level=session.user.power_level
        )

        session.update(user)

        if session.error:
            return self.parent().parent().show_message(
                text=session.error,
                error=True,
                parent=self
            )

        self.parent().parent().show_message(
            text='Successfully',
            parent=self
        )

        self.set_line_edit_enable(False)
        self.allow_button.setEnabled(False)
        self.edit_button.setEnabled(True)
