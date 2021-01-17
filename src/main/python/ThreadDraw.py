# -*- coding: utf-8 -*-
import time
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class ThreadDraw(QThread):

    change_value_information_process_output = pyqtSignal(str)

    ins_username = ""
    ins_password = ""
    link = ""
    number_of_person_in_comment = ""
    max_number_of_comment = ""
    word_in_comment = ""
    comment_combinations = ""
    telegram_name = ""

    def run(self):
        self.instagramDraw()

    def telegram_send_message(self,msg):
        base_url = "https://api.telegram.org/bot1398914124:AAHG31zQXI3KVeFZ_8JeQN3Hn2w0QM777tU/sendMessage?chat_id=-1001252236490&text=" + str(msg)
        requests.get(base_url)

    def instagramDraw(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        while 1:
            browser.get(self.link)
            time.sleep(3)

            try:
                enter_button = browser.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                enter_button.click()
                time.sleep(3)
                self.change_value_information_process_output.emit("+ Giriş Sayfasına Gidildi.")
                break
            except:
                self.change_value_information_process_output.emit("- Giris sayfasina gidilemedi.")
                self.change_value_information_process_output.emit("* Sayfa Yenileniyor")

        while 1:
            try:
                username = browser.find_element_by_name("username")
                password = browser.find_element_by_name("password")

                username.send_keys(f"{self.ins_username}")  # kullanıcı adı
                password.send_keys(f"{self.ins_password}")  # sifresi
                password.send_keys(Keys.ENTER)
                break
            except:
                self.change_value_information_process_output.emit("- Kullanıcı ve şifre yazılamadı.")
                self.change_value_information_process_output.emit("* Sayfa Yenileniyor")
                browser.refresh()
                time.sleep(3)

        time.sleep(5)
        not_now_buton = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button")
        not_now_buton.click()
        time.sleep(5)

        # gonder_butonu = browser.find_element_by_xpath(
        #     "//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[3]/div/form/button")
        total_saniye = int((int(self.max_number_of_comment) * 66) + (int(self.max_number_of_comment) / 40 * 1500))
        ty_res = time.gmtime(total_saniye)
        proc_time = time.strftime("%H:%M:%S", ty_res)

        self.telegram_send_message(str(self.telegram_name + "\nBİSMİLLAHİRRAHMANİRRAHİM, ALLAHIM NASİP ET 🤲\nIntagram Bot Aktif Edildi.\nHedef Yorum Sayisi:"+self.max_number_of_comment+"\nTahmini Süre"+proc_time))

        sayac = 0
        for i in self.comment_combinations:
            if sayac != 0 and sayac % 40 == 0:
                self.telegram_mesaj_yolla(self.telegram_name + "\nAtılan yorum sayısı:" + sayac + "\n60 dk bekleyecek.")
                time.sleep(3600)
            browser.refresh()
            yorum = browser.find_element_by_class_name('Ypffh')
            yorum.click()
            time.sleep(5)
            yorum = browser.find_element_by_class_name('Ypffh')
            yorum.click()

            try:
                if self.number_of_person_in_comment == 1:
                    comment = self.word_in_comment
                    for x in range(self.number_of_person_in_comment):
                        comment =  comment +" "+i[x] + ' '
                    yorum.send_keys(comment)
                elif self.number_of_person_in_comment == 2:
                    comment = self.word_in_comment
                    for x in range(self.number_of_person_in_comment):
                        comment = comment + " " + i[x] + ' '
                    yorum.send_keys(comment)
                elif self.number_of_person_in_comment == 3:
                    comment = self.word_in_comment
                    for x in range(self.number_of_person_in_comment):
                        comment = comment + " " + i[x] + ' '
                    yorum.send_keys(comment)
                buton_salla = browser.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[3]/div/form/button")
                buton_salla.click()
            except:
                browser.refresh()
                time.sleep(5)
                pass

            sayac += 1
            self.change_value_information_process_output.emit("+Kişi:"+ str(sayac))
            print(f"Sayac : {sayac}")
            time.sleep(40)

            if sayac == int(self.max_number_of_comment):
                break

        self.telegram_send_message(self.telegram_name + "\n" + str(sayac) + " adet yorum yapıldı.\nİslemleriniz tamamlandi.\nALLAH NASİP EDER İNŞALLAH.🤲")
        self.change_value_information_process_output.emit("+Tum yorum islemleri yapildi ! ")
        self.change_value_information_process_output.emit("***🤲ALLAH NASİP EDER İNŞALLAH🤲***")