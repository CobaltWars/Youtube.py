import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://youtube.com/"))
        self.setCentralWidget(self.browser)
        
        self.setWindowTitle("Youtube")
        self.setWindowIcon(QIcon("logo_app.ico"))  # Ajout de l'icône

        # Créer une variable pour stocker l'état de maximisation de la fenêtre
        self.is_maximized = False

        # Créer une variable pour stocker la taille de l'écran entier
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry()
        self.default_size = screen_geometry.size()

        # Afficher en mode fenêtre maximisée par défaut
        self.showMaximized()
        self.is_maximized = True

        # Créer une fenêtre de démarrage avec une icône
        self.splash = QSplashScreen(QPixmap("logo.png"), Qt.WindowStaysOnTopHint)
        self.splash.show()

        # Connecter le signal de chargement complet à une fonction qui masque la fenêtre de démarrage
        self.browser.loadFinished.connect(self.fade_out_splash)
        
        # Supporter mode plein écran
        self.browser.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True
        )
        
        self.browser.page().fullScreenRequested.connect(
            lambda request: self.handle_fullscreen_requested(request)
        )
        
    def fade_out_splash(self):
        # Effectuer l'effet de fondu enchaîné
        self.fade_animation = QPropertyAnimation(self.splash, b"windowOpacity")
        self.fade_animation.setDuration(1000)  # Durée de l'animation en millisecondes
        self.fade_animation.setStartValue(0.8)  # Opacité initiale (plus proche de 1.0 pour commencer plus tard)
        self.fade_animation.setEndValue(0.0)  # Opacité finale
        self.fade_animation.finished.connect(self.splash.hide)  # Cacher la fenêtre de démarrage à la fin de l'animation
        self.fade_animation.start()

    def handle_fullscreen_requested(self, request):
        request.accept()

        if request.toggleOn():
            # Sauvegarder l'état de maximisation de la fenêtre avant de passer en mode plein écran
            self.is_maximized = self.isMaximized()
            self.showFullScreen()
            self.statusBar().hide()
            self.browser.page().settings().setAttribute(
                QWebEngineSettings.ShowScrollBars, False
            )
        else:
            # Restaurer l'état de maximisation de la fenêtre avant le mode plein écran
            if self.is_maximized:
                self.showMaximized()
            else:
                self.showNormal()
            self.statusBar().show()
            self.browser.page().settings().setAttribute(
                QWebEngineSettings.ShowScrollBars, True
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()  # Afficher la fenêtre principale
    sys.exit(app.exec_())
