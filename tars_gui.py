import sys
import math
import time
from datetime import datetime

# pyrefly: ignore [missing-import]
from PySide6.QtCore import (
    Qt,
    QTimer,
    QPoint,
    QRectF,
    Signal,
)
# pyrefly: ignore [missing-import]
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
    QLinearGradient,
)
# pyrefly: ignore [missing-import]
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QFrame,
    QSizePolicy,
)


# ============================================================
# COLORS
# ============================================================

BG = QColor("#02070D")
PANEL = QColor("#06111A")
PANEL2 = QColor("#071722")

CYAN = QColor("#00D9FF")
CYAN2 = QColor("#00A8D8")
CYAN_DIM = QColor("#08718C")

TEXT = QColor("#D8F8FF")
TEXT_DIM = QColor("#6E9AA8")

GREEN = QColor("#00FF91")
RED = QColor("#FF315C")


# ============================================================
# GLOW FRAME
# ============================================================

class GlowFrame(QFrame):

    def __init__(self, parent=None, show_reactor=False):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            QFrame {
                background: rgba(4, 13, 21, 220);
                border: 1px solid #07394A;
                border-radius: 10px;
            }
        """)

        # Optional big circulating circle sitting behind everything
        # else that gets added to this frame's layout.
        self.reactor = None

        if show_reactor:

            self.setStyleSheet("""
                QFrame {
                    background: rgba(4, 13, 21, 150);
                    border: 1px solid #07394A;
                    border-radius: 10px;
                }
            """)

            self.reactor = Reactor(self)
            self.reactor.setStyleSheet("background: transparent;")
            self.reactor.lower()

    def resizeEvent(self, event):

        if self.reactor is not None:

            self.reactor.setGeometry(self.rect())
            self.reactor.lower()

        super().resizeEvent(event)


# ============================================================
# ANIMATED REACTOR
# ============================================================

class Reactor(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.angle = 0
        self.pulse = 0
        self.active = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(25)

        self.setMinimumSize(300, 300)

    def animate(self):

        self.angle = (self.angle + 1.2) % 360

        self.pulse += 0.045

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        cx = self.width() / 2
        cy = self.height() / 2

        center = QPoint(
            int(cx),
            int(cy)
        )

        base = min(
            self.width(),
            self.height()
        )

        radius = base * 0.22

        # ------------------------------------------------
        # DARK RADIAL BACKGROUND
        # ------------------------------------------------

        gradient = QLinearGradient(
            0,
            0,
            self.width(),
            self.height()
        )

        gradient.setColorAt(
            0,
            QColor("#02060B")
        )

        gradient.setColorAt(
            0.5,
            QColor("#03121B")
        )

        gradient.setColorAt(
            1,
            QColor("#02060B")
        )

        painter.fillRect(
            self.rect(),
            gradient
        )

        # ------------------------------------------------
        # GRID
        # ------------------------------------------------

        painter.setPen(
            QPen(
                QColor(0, 100, 130, 35),
                1
            )
        )

        grid = 35

        for x in range(0, self.width(), grid):

            painter.drawLine(
                x,
                0,
                x,
                self.height()
            )

        for y in range(0, self.height(), grid):

            painter.drawLine(
                0,
                y,
                self.width(),
                y
            )

        # ------------------------------------------------
        # RADIAL RINGS
        # ------------------------------------------------

        for i in range(7):

            r = radius + i * 28

            alpha = max(
                20,
                110 - i * 13
            )

            painter.setPen(
                QPen(
                    QColor(
                        CYAN.red(),
                        CYAN.green(),
                        CYAN.blue(),
                        alpha
                    ),
                    1
                )
            )

            painter.drawEllipse(
                center,
                int(r),
                int(r)
            )

        # ------------------------------------------------
        # ROTATING SEGMENTS
        # ------------------------------------------------

        painter.save()

        painter.translate(
            cx,
            cy
        )

        painter.rotate(
            self.angle
        )

        for i in range(8):

            painter.setPen(
                QPen(
                    QColor(
                        CYAN.red(),
                        CYAN.green(),
                        CYAN.blue(),
                        180
                    ),
                    2
                )
            )

            start = i * 45

            painter.drawArc(
                QRectF(
                    -radius - 75,
                    -radius - 75,
                    (radius + 75) * 2,
                    (radius + 75) * 2,
                ),
                start * 16,
                18 * 16
            )

        painter.restore()

        # ------------------------------------------------
        # OUTER ROTATING DOTS
        # ------------------------------------------------

        painter.save()

        painter.translate(
            cx,
            cy
        )

        painter.rotate(
            -self.angle * 1.7
        )

        for i in range(12):

            angle = math.radians(
                i * 30
            )

            x = math.cos(angle) * (
                radius + 90
            )

            y = math.sin(angle) * (
                radius + 90
            )

            painter.setBrush(
                QColor(
                    CYAN.red(),
                    CYAN.green(),
                    CYAN.blue(),
                    180 if i % 2 == 0 else 70
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawEllipse(
                QPoint(
                    int(x),
                    int(y)
                ),
                3,
                3
            )

        painter.restore()

        # ------------------------------------------------
        # CORE GLOW
        # ------------------------------------------------

        pulse = (
            math.sin(self.pulse) + 1
        ) / 2

        for i in range(5):

            rr = radius * (
                1.2 - i * 0.17
            )

            alpha = int(
                25 + pulse * 35
            )

            painter.setBrush(
                QColor(
                    0,
                    210,
                    255,
                    alpha
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawEllipse(
                center,
                int(rr),
                int(rr)
            )

        # ------------------------------------------------
        # CORE
        # ------------------------------------------------

        painter.setBrush(
            QColor("#06283A")
        )

        painter.setPen(
            QPen(
                CYAN,
                2
            )
        )

        painter.drawEllipse(
            center,
            int(radius * 0.55),
            int(radius * 0.55)
        )

        painter.setBrush(
            QColor("#00DFFF")
        )

        painter.drawEllipse(
            center,
            9,
            9
        )

        # ------------------------------------------------
        # TARS TEXT
        # ------------------------------------------------

        painter.setPen(
            QColor(
                CYAN.red(),
                CYAN.green(),
                CYAN.blue(),
                90
            )
        )

        font = QFont(
            "Consolas",
            16
        )

        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            QRectF(
                cx - 80,
                cy + radius + 115,
                160,
                30
            ),
            Qt.AlignCenter,
            "T A R S"
        )


# ============================================================
# CUSTOM TITLE BAR
# ============================================================

class TitleBar(QWidget):

    def __init__(
        self,
        window,
    ):
        super().__init__()

        self.window = window
        self.drag_position = None

        self.setFixedHeight(55)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            22,
            0,
            10,
            0
        )

        layout.setSpacing(8)

        title = QLabel(
            "TARS  //  LOCAL INTELLIGENCE SYSTEM"
        )

        title.setStyleSheet("""
            QLabel {
                color: #66E8FF;
                font-family: Consolas;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)

        layout.addWidget(
            title
        )

        layout.addStretch()

        # MINIMIZE

        self.min_button = QPushButton(
            "—"
        )

        # MAXIMIZE

        self.max_button = QPushButton(
            "□"
        )

        # CLOSE

        self.close_button = QPushButton(
            "×"
        )

        for button in [
            self.min_button,
            self.max_button,
            self.close_button
        ]:

            button.setFixedSize(
                42,
                34
            )

            button.setCursor(
                Qt.PointingHandCursor
            )

        self.min_button.clicked.connect(
            self.window.showMinimized
        )

        self.max_button.clicked.connect(
            self.window.toggle_maximize
        )

        self.close_button.clicked.connect(
            self.window.close
        )

        self.close_button.setStyleSheet("""
            QPushButton {
                color: #65DFFF;
                background: transparent;
                border: none;
                font-size: 22px;
            }

            QPushButton:hover {
                background: #B00030;
                color: white;
            }
        """)

        self.max_button.setStyleSheet("""
            QPushButton {
                color: #65DFFF;
                background: transparent;
                border: none;
                font-size: 18px;
            }

            QPushButton:hover {
                background: #07394A;
            }
        """)

        self.min_button.setStyleSheet("""
            QPushButton {
                color: #65DFFF;
                background: transparent;
                border: none;
                font-size: 18px;
            }

            QPushButton:hover {
                background: #07394A;
            }
        """)

        layout.addWidget(
            self.min_button
        )

        layout.addWidget(
            self.max_button
        )

        layout.addWidget(
            self.close_button
        )

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            == Qt.LeftButton
        ):

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.window.frameGeometry().topLeft()
            )

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.drag_position
            and event.buttons()
            & Qt.LeftButton
        ):

            if not self.window.isMaximized():

                self.window.move(
                    event.globalPosition().toPoint()
                    - self.drag_position
                )

    def mouseDoubleClickEvent(
        self,
        event
    ):

        self.window.toggle_maximize()


# ============================================================
# SIDEBAR
# ============================================================

class Sidebar(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setFixedWidth(
            315
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            12,
            18,
            20
        )

        layout.setSpacing(
            14
        )

        # ------------------------------------------------
        # LOGO
        # ------------------------------------------------

        logo = QLabel(
            "TARS"
        )

        logo.setStyleSheet("""
            QLabel {
                color: #00DFFF;
                font-family: Consolas;
                font-size: 40px;
                font-weight: bold;
                letter-spacing: 7px;
            }
        """)

        layout.addWidget(
            logo
        )

        subtitle = QLabel(
            "TASK AUTOMATION &\n"
            "REASONING SYSTEM"
        )

        subtitle.setStyleSheet("""
            QLabel {
                color: #4C92A6;
                font-family: Consolas;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)

        layout.addWidget(
            subtitle
        )

        # ------------------------------------------------
        # DECORATIVE LINE
        # ------------------------------------------------

        line = QFrame()

        line.setFixedHeight(
            1
        )

        line.setStyleSheet(
            "background:#075064;"
        )

        layout.addWidget(
            line
        )

        # ------------------------------------------------
        # NEW CHAT
        # ------------------------------------------------

        new_chat = QPushButton(
            "+   NEW CONVERSATION"
        )

        new_chat.setFixedHeight(
            52
        )

        new_chat.setCursor(
            Qt.PointingHandCursor
        )

        new_chat.setStyleSheet("""
            QPushButton {
                color: #74E8FF;
                background: #041722;
                border: 1px solid #087C9A;
                border-radius: 7px;
                font-family: Consolas;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
                padding-left: 18px;
            }

            QPushButton:hover {
                background: #073043;
                border: 1px solid #00DFFF;
            }
        """)

        layout.addWidget(
            new_chat
        )

        # ------------------------------------------------
        # SYSTEM
        # ------------------------------------------------

        self.section(
            layout,
            "SYSTEM"
        )

        self.status(
            layout,
            "●  ONLINE",
            GREEN
        )

        self.status(
            layout,
            "VOICE READY",
            CYAN
        )

        # ------------------------------------------------
        # CAPABILITIES
        # ------------------------------------------------

        self.section(
            layout,
            "CAPABILITIES"
        )

        self.capability(
            layout,
            "◈   LOCAL AI"
        )

        self.capability(
            layout,
            "▣   COMPUTER CONTROL"
        )

        self.capability(
            layout,
            "</>  VS CODE AUTOMATION"
        )

        self.capability(
            layout,
            "♩   VOICE RECOGNITION"
        )

        self.capability(
            layout,
            "◎   LONG-TERM MEMORY"
        )

        layout.addStretch()

        # ------------------------------------------------
        # VERSION
        # ------------------------------------------------

        version = QLabel(
            "TARS v2.0\n"
            "LOCAL NEURAL INTERFACE\n"
            "Powered by Ollama"
        )

        version.setStyleSheet("""
            QLabel {
                color: #3F7281;
                font-family: Consolas;
                font-size: 10px;
                line-height: 150%;
            }
        """)

        layout.addWidget(
            version
        )

    def section(
        self,
        layout,
        text
    ):

        label = QLabel(
            text
        )

        label.setStyleSheet("""
            QLabel {
                color: #417C8C;
                font-family: Consolas;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 2px;
                margin-top: 12px;
            }
        """)

        layout.addWidget(
            label
        )

    def status(
        self,
        layout,
        text,
        color
    ):

        label = QLabel(
            text
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color: {color.name()};
                background: #04131C;
                border-left: 2px solid {color.name()};
                padding: 10px;
                font-family: Consolas;
                font-size: 11px;
                font-weight: bold;
            }}
            """
        )

        layout.addWidget(
            label
        )

    def capability(
        self,
        layout,
        text
    ):

        button = QPushButton(
            text
        )

        button.setFixedHeight(
            46
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        button.setStyleSheet("""
            QPushButton {
                color: #8CBAC7;
                background: #04131C;
                border: 1px solid #0A3342;
                border-radius: 6px;
                text-align: left;
                padding-left: 14px;
                font-family: Consolas;
                font-size: 11px;
            }

            QPushButton:hover {
                color: #00DFFF;
                border: 1px solid #0089A8;
                background: #06202B;
            }
        """)

        layout.addWidget(
            button
        )


# ============================================================
# MESSAGE CARD
# ============================================================

class MessageCard(QFrame):

    def __init__(
        self,
        speaker,
        message,
        is_user=False
    ):

        super().__init__()

        # Messenger-style bubble: the user's own messages get a
        # brighter cyan-tinted bubble, TARS gets the dark panel one.

        self.setMaximumWidth(
            520
        )

        if is_user:

            bubble_bg = "#0B3B4D"
            bubble_border = "#00A8D8"
            name_color = "#8FE9FF"

        else:

            bubble_bg = "#04111A"
            bubble_border = "#0A3848"
            name_color = "#00DFFF"

        self.setStyleSheet(
            f"""
            QFrame {{
                background: {bubble_bg};
                border: 1px solid {bubble_border};
                border-radius: 14px;
            }}
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            18,
            14,
            18,
            14
        )

        header = QHBoxLayout()

        name = QLabel(
            speaker
        )

        name.setStyleSheet(
            f"""
            QLabel {{
                color: {name_color};
                background: transparent;
                border: none;
                font-family: Consolas;
                font-size: 12px;
                font-weight: bold;
            }}
            """
        )

        timestamp = QLabel(
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        timestamp.setStyleSheet("""
            QLabel {
                color: #417888;
                background: transparent;
                border: none;
                font-family: Consolas;
                font-size: 10px;
            }
        """)

        header.addWidget(
            name
        )

        header.addStretch()

        header.addWidget(
            timestamp
        )

        layout.addLayout(
            header
        )

        text = QLabel(
            message
        )

        text.setWordWrap(
            True
        )

        text.setStyleSheet("""
            QLabel {
                color: #D8F8FF;
                background: transparent;
                border: none;
                font-family: Segoe UI;
                font-size: 14px;
                padding-top: 7px;
            }
        """)

        layout.addWidget(
            text
        )


# ============================================================
# CHAT AREA
# ============================================================

class ChatArea(QWidget):

    message_sent = Signal(str)

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            10
        )

        # ------------------------------------------------
        # HEADER
        # ------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "TARS"
        )

        title.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Segoe UI;
                font-size: 24px;
                font-weight: bold;
            }
        """)

        description = QLabel(
            "LOCAL INTELLIGENT DESKTOP ASSISTANT"
        )

        description.setStyleSheet("""
            QLabel {
                color: #477987;
                font-family: Consolas;
                font-size: 10px;
                letter-spacing: 1px;
            }
        """)

        header.addWidget(
            title
        )

        header.addSpacing(
            20
        )

        header.addWidget(
            description
        )

        header.addStretch()

        # READY

        ready = QLabel(
            "●  READY"
        )

        ready.setStyleSheet("""
            QLabel {
                color: #00FF91;
                background: #031C13;
                border: 1px solid #07583C;
                border-radius: 16px;
                padding: 9px 18px;
                font-family: Consolas;
                font-size: 11px;
                font-weight: bold;
            }
        """)

        header.addWidget(
            ready
        )

        layout.addLayout(
            header
        )

        # ------------------------------------------------
        # CONVERSATION PANEL
        # ------------------------------------------------

        conversation = GlowFrame(
            show_reactor=True
        )

        conversation_layout = QVBoxLayout(
            conversation
        )

        conversation_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        # Label

        label = QLabel(
            "CONVERSATION"
        )

        label.setStyleSheet("""
            QLabel {
                color: #00DFFF;
                font-family: Consolas;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)

        conversation_layout.addWidget(
            label
        )

        # Scroll area

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)

        self.scroll.viewport().setStyleSheet(
            "background: transparent;"
        )

        self.messages_widget = QWidget()

        self.messages_widget.setStyleSheet(
            "background: transparent;"
        )

        self.messages_layout = QVBoxLayout(
            self.messages_widget
        )

        self.messages_layout.setAlignment(
            Qt.AlignTop
        )

        self.messages_layout.setSpacing(
            10
        )

        self.scroll.setWidget(
            self.messages_widget
        )

        conversation_layout.addWidget(
            self.scroll
        )

        layout.addWidget(
            conversation,
            1
        )

        # ------------------------------------------------
        # REACTOR + CHAT
        # ------------------------------------------------

        self.add_message(
            "TARS",
            "New conversation started.\n"
            "What are we building?"
        )

        # ------------------------------------------------
        # INPUT
        # ------------------------------------------------

        input_frame = QFrame()

        input_frame.setStyleSheet("""
            QFrame {
                background: #04111A;
                border: 1px solid #08718C;
                border-radius: 9px;
            }
        """)

        input_layout = QHBoxLayout(
            input_frame
        )

        input_layout.setContentsMargins(
            15,
            8,
            10,
            8
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "MESSAGE TARS..."
        )

        self.input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #D8F8FF;
                font-family: Consolas;
                font-size: 14px;
                padding: 10px;
            }
        """)

        self.input.returnPressed.connect(
            self.send_message
        )

        input_layout.addWidget(
            self.input
        )

        self.voice_button = QPushButton(
            "◉"
        )

        self.voice_button.setFixedSize(
            50,
            50
        )

        self.voice_button.setStyleSheet("""
            QPushButton {
                color: #00DFFF;
                background: #061D2A;
                border: 1px solid #08718C;
                border-radius: 25px;
                font-size: 20px;
            }

            QPushButton:hover {
                background: #073B4C;
                border: 1px solid #00DFFF;
            }
        """)

        input_layout.addWidget(
            self.voice_button
        )

        self.send_button = QPushButton(
            "➤"
        )

        self.send_button.setFixedSize(
            58,
            50
        )

        self.send_button.setStyleSheet("""
            QPushButton {
                color: white;
                background: #00A8D8;
                border: none;
                border-radius: 25px;
                font-size: 24px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #00DFFF;
            }

            QPushButton:pressed {
                background: #08718C;
            }
        """)

        self.send_button.clicked.connect(
            self.send_message
        )

        input_layout.addWidget(
            self.send_button
        )

        layout.addWidget(
            input_frame
        )

        hint = QLabel(
            "ENTER  SEND     •     SPACE  VOICE"
        )

        hint.setAlignment(
            Qt.AlignCenter
        )

        hint.setStyleSheet("""
            QLabel {
                color: #315966;
                font-family: Consolas;
                font-size: 9px;
                letter-spacing: 1px;
            }
        """)

        layout.addWidget(
            hint
        )

    def add_message(
        self,
        speaker,
        message,
        is_user=False
    ):

        row = QWidget()

        row.setStyleSheet(
            "background: transparent;"
        )

        row_layout = QHBoxLayout(
            row
        )

        row_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        card = MessageCard(
            speaker,
            message,
            is_user
        )

        if is_user:

            # push the bubble to the right, like a sent message
            row_layout.addStretch()
            row_layout.addWidget(card)

        else:

            # keep the bubble on the left, like a received message
            row_layout.addWidget(card)
            row_layout.addStretch()

        self.messages_layout.addWidget(
            row
        )

        QTimer.singleShot(
            50,
            lambda:
            self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            )
        )

    def send_message(self):

        text = self.input.text().strip()

        if not text:
            return

        self.input.clear()

        self.add_message(
            "YOU",
            text,
            True
        )

        self.message_sent.emit(
            text
        )


# ============================================================
# MAIN WINDOW
# ============================================================

class TARSWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "TARS"
        )

        # IMPORTANT:
        # custom window = no duplicate Windows controls

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Window
        )

        self.resize(
            1500,
            900
        )

        self.setMinimumSize(
            1100,
            700
        )

        self.setStyleSheet("""
            QMainWindow {
                background: #02070D;
            }
        """)

        # ------------------------------------------------
        # CENTRAL
        # ------------------------------------------------

        root = QWidget()

        root.setStyleSheet("""
            QWidget {
                background: #02070D;
            }
        """)

        self.setCentralWidget(
            root
        )

        root_layout = QVBoxLayout(
            root
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ------------------------------------------------
        # TITLE BAR
        # ------------------------------------------------

        self.title_bar = TitleBar(
            self
        )

        root_layout.addWidget(
            self.title_bar
        )

        # ------------------------------------------------
        # MAIN CONTENT
        # ------------------------------------------------

        content = QHBoxLayout()

        content.setContentsMargins(
            15,
            0,
            15,
            15
        )

        content.setSpacing(
            18
        )

        # SIDEBAR

        sidebar = Sidebar()

        content.addWidget(
            sidebar
        )

        # MAIN

        self.chat = ChatArea()

        content.addWidget(
            self.chat,
            1
        )

        root_layout.addLayout(
            content,
            1
        )

        # ------------------------------------------------
        # BACKEND CONNECTION
        # ------------------------------------------------

        self.chat.message_sent.connect(
            self.process_message
        )

    # ========================================================
    # MAXIMIZE
    # ========================================================

    def toggle_maximize(self):

        if self.isMaximized():

            self.showNormal()

            self.title_bar.max_button.setText(
                "□"
            )

        else:

            self.showMaximized()

            self.title_bar.max_button.setText(
                "❐"
            )

    # ========================================================
    # TARS BACKEND
    # ========================================================

    def process_message(
        self,
        text
    ):

        # ----------------------------------------------------
        # TEMPORARY UI TEST
        # ----------------------------------------------------

        self.chat.add_message(
            "TARS",
            "Processing..."
        )

        # ----------------------------------------------------
        # CONNECT YOUR EXISTING TARS HERE
        # ----------------------------------------------------

        try:

            from tars_core import TARS

            if not hasattr(
                self,
                "tars"
            ):

                self.tars = TARS()

            response = self.tars.ask(
                text
            )

            # Remove "Processing..." card

            item = self.chat.messages_layout.takeAt(
                self.chat.messages_layout.count() - 1
            )

            if item:

                widget = item.widget()

                if widget:

                    widget.deleteLater()

            self.chat.add_message(
                "TARS",
                str(response)
            )

        except Exception as e:

            self.chat.add_message(
                "SYSTEM",
                f"Backend error: {e}"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "TARS"
    )

    window = TARSWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()
