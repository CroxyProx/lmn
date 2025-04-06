import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QMovie


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.add_new_tab(QUrl('http://google.com'), 'Home Tab')
        self.showMaximized()

        # Loading spinner (Lumen Loader)
        self.loading_label = QLabel(self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("l.gif")
        self.loading_label.setMovie(self.movie)
        self.loading_label.hide()

        # Resize event to ensure loader covers the whole window
        self.resizeEvent = self.on_resize

        # Navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('◀', self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('▶', self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(' ⟳ ', self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction('⬢𝐋𝐔𝐌𝐄𝐍⬢', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.addSeparator()

        house_btn = QAction('ICONS: ', self)
        navbar.addAction(house_btn)

        drive_btn = QAction('📁', self)
        drive_btn.triggered.connect(self.navigate_drive)
        navbar.addAction(drive_btn)

        mail_btn = QAction('Mail', self)
        mail_btn.triggered.connect(self.navigate_mail)
        navbar.addAction(mail_btn)

        youtube_btn = QAction('𝗬𝗧', self)
        youtube_btn.triggered.connect(self.navigate_youtube)
        navbar.addAction(youtube_btn)

        chatgpt_btn = QAction('𝐂𝐡𝐚𝐭𝐆𝐏𝐓', self)
        chatgpt_btn.triggered.connect(self.navigate_chatgpt)
        navbar.addAction(chatgpt_btn)

        wiki_btn = QAction('𝕎', self)
        wiki_btn.triggered.connect(self.navigate_wiki)
        navbar.addAction(wiki_btn)

        weather_btn = QAction('Weather️', self)
        weather_btn.triggered.connect(self.navigate_weather)
        navbar.addAction(weather_btn)

        newyorktimes_btn = QAction('𝐍𝐞𝐰𝐘𝐨𝐫𝐤𝐓𝐢𝐦𝐞𝐬', self)
        newyorktimes_btn.triggered.connect(self.navigate_newyorktimes)
        navbar.addAction(newyorktimes_btn)

        download_btn = QAction('⬇ Download', self)
        download_btn.triggered.connect(self.trigger_download)
        navbar.addAction(download_btn)

        new_tab_btn = QAction('+CreateTab+', self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('http://google.com'), 'Lumen: New Tab'))
        navbar.addAction(new_tab_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.tabs.currentChanged.connect(self.update_url_bar)

    def add_new_tab(self, qurl=None, label='Lumen: NewTab'):
        if qurl is None:
            qurl = QUrl('http://google.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        self.tabs.addTab(browser, label)
        self.tabs.setCurrentWidget(browser)
        browser.urlChanged.connect(self.update_url_bar)

        # Connect load events
        browser.loadStarted.connect(self.show_loading)
        browser.loadFinished.connect(self.hide_loading)
        browser.page().profile().downloadRequested.connect(self.handle_download)

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_home(self):
        self.current_browser().setUrl(QUrl('http://google.com'))

    def navigate_mail(self):
        self.current_browser().setUrl(QUrl('http://gmail.com'))

    def navigate_drive(self):
        self.current_browser().setUrl(QUrl('http://drive.google.com'))

    def navigate_youtube(self):
        self.current_browser().setUrl(QUrl('http://youtube.com'))

    def navigate_chatgpt(self):
        self.current_browser().setUrl(QUrl('http://chat.openai.com'))

    def navigate_wiki(self):
        self.current_browser().setUrl(QUrl('https://en.wikipedia.org'))

    def navigate_weather(self):
        self.current_browser().setUrl(QUrl('https://weather.com/'))

    def navigate_newyorktimes(self):
        self.current_browser().setUrl(QUrl('https://www.nytimes.com/'))

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if "." in url and " " not in url:
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
        else:
            url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self):
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())

    def show_loading(self):
        self.loading_label.setGeometry(1, 1, self.width(), self.height())  # Cover the full window
        self.loading_label.raise_()  # Ensure it appears above all other widgets
        self.loading_label.show()
        self.movie.start()

    def hide_loading(self):
        QTimer.singleShot(500, lambda: self.loading_label.hide())  # Delay hiding so it's visible
        self.movie.stop()

    def handle_download(self, download):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.suggestedFileName(), "All Files (*.*)", options=options)
        if file_path:
            download.setPath(file_path)
            download.accept()

    def trigger_download(self):
        browser = self.current_browser()
        if browser:
            browser.page().profile().downloadRequested.connect(self.handle_download)

    def on_resize(self, event):
        """ Adjusts the loading screen size dynamically when resizing """
        self.loading_label.setGeometry(0, 0, self.width(), self.height())
        event.accept()


app = QApplication(sys.argv)
QApplication.setApplicationName('LumenBetaRelease')
window = MainWindow()
app.exec_()


