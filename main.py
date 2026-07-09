import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from plyer import notification

class MoliyachiApp(App):
    def build(self):
        # Ma'lumotlar bazasini sozlash
        self.conn = sqlite3.connect('obodonchilik.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ish_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sana TEXT,
                soat REAL,
                yoqilgi REAL
            )
        ''')
        self.conn.commit()

        # Asosiy oyna dizayni
        uzun_oyna = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Sarlavha
        uzun_oyna.add_widget(Label(text="MOLIYACHI AI OBODON\nIsh va Yoqilg'i Hisobi", font_size=20, bold=True, size_hint_y=None, height=50, halign="center"))

        # Ma'lumot kiritish joylari
        self.sana_input = TextInput(hint_text="Sana (Yil-Oy-Kun)", multiline=False, size_hint_y=None, height=40)
        self.soat_input = TextInput(hint_text="Ish soati (Masalan: 8)", multiline=False, input_filter='float', size_hint_y=None, height=40)
        self.yoqilgi_input = TextInput(hint_text="Sarflangan yoqilg'i (Litr)", multiline=False, input_filter='float', size_hint_y=None, height=40)

        uzun_oyna.add_widget(self.sana_input)
        uzun_oyna.add_widget(self.soat_input)
        uzun_oyna.add_widget(self.yoqilgi_input)

        # Saqlash tugmasi
        saqlash_btn = Button(text="Ma'lumotni Saqlash", background_color=[0.1, 0.6, 0.3, 1], size_hint_y=None, height=50, font_size=18)
        saqlash_btn.bind(on_press=self.malumot_saqlash)
        uzun_oyna.add_widget(saqlash_btn)

        # Tarix ro'yxati (Skroll bo'ladigan joy)
        uzun_oyna.add_widget(Label(text="Kiritilgan Ma'lumotlar Tarixi:", font_size=16, bold=True, size_hint_y=None, height=30))
        
        self.tarix_scroll = ScrollView()
        self.tarix_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.tarix_grid.bind(minimum_height=self.tarix_grid.setter('height'))
        self.tarix_scroll.add_widget(self.tarix_grid)
        
        uzun_oyna.add_widget(self.tarix_scroll)

        # Tarixni yangilab ko'rsatish
        self.tarixni_yangila()

        return uzun_oyna

    def malumot_saqlash(self, instance):
        sana = self.sana_input.text.strip()
        soat = self.soat_input.text.strip()
        yoqilgi = self.yoqilgi_input.text.strip()

        if sana and soat and yoqilgi:
            try:
                self.cursor.execute("INSERT INTO ish_log (sana, soat, yoqilgi) VALUES (?, ?, ?)", (sana, float(soat), float(yoqilgi)))
                self.conn.commit()
                
                # Tozalash
                self.sana_input.text = ""
                self.soat_input.text = ""
                self.yoqilgi_input.text = ""
                
                self.tarixni_yangila()
                
                # Telefonga bildirishnoma yuborish
                notification.notify(title="Muvaffaqiyatli", message="Ma'lumotlar bazaga saqlandi!")
            except Exception as e:
                print(e)
        else:
            notification.notify(title="Xatolik", message="Iltimos, hamma joyni to'ldiring!")

    def tarixni_yangila(self):
        self.tarix_grid.clear_widgets()
        self.cursor.execute("SELECT sana, soat, yoqilgi FROM ish_log ORDER BY id DESC")
        rows = self.cursor.fetchall()
        
        for row in rows:
            matn = f"Sana: {row[0]}  |  Soat: {row[1]} m/soat  |  Yoqilg'i: {row[2]} L"
            self.tarix_grid.add_widget(Label(text=matn, size_hint_y=None, height=35, font_size=14, halign="left"))

    def on_stop(self):
        self.conn.close()

if __name__ == '__main__':
    MoliyachiApp().run()
