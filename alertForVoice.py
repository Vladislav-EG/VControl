from win10toast import ToastNotifier
from threading import Thread

def main():
    my_notification = ToastNotifier()
    my_notification.show_toast(
        "Голосовой Ввод", 
        "Укажите текстовым курсором куда будет вводиться текст",
        threaded = True,
    )





