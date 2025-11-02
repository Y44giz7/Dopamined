# main.py (Düzeltilmiş Dopamined)
from kivy.config import Config
# genel config (en başta olmalı)
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'dpi', 'auto')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.image import Image 
Window.clearcolor = (0.07, 0.07, 0.08, 1)

# --- Veri / Ayarlar ---
LISLE_DB = [
    {"isim": "Kabataş Erkek Lisesi", "sehir": "İstanbul", "puan": 494.52},
    {"isim": "İstanbul Atatürk Fen Lisesi", "sehir": "İstanbul", "puan": 490.18},
    {"isim": "Beşiktaş Sakıp Sabancı Anadolu Lisesi", "sehir": "İstanbul", "puan": 486.22},
    {"isim": "Eskişehir Fatih Fen Lisesi", "sehir": "Eskişehir", "puan": 476.24},
    {"isim": "Samsun Fen Lisesi", "sehir": "Samsun", "puan": 472.50},
    {"isim": "Ankara Fen Lisesi", "sehir": "Ankara", "puan": 488.00},
    {"isim": "İzmir Fen Lisesi", "sehir": "İzmir", "puan": 485.30},
    {"isim": "Adana Fen Lisesi", "sehir": "Adana", "puan": 480.75},
]
YANLIS_BOL = {
    "turkce": 3,
    "mat": 3,
    "fen": 3,
    "inkilap": 4,
    "din": 4,
    "ing": 4
}

DERS_SORULAR = {
    "turkce": 20,
    "mat": 20,
    "fen": 20,
    "inkilap": 10,
    "din": 10,
    "ing": 10
}


# Kullanıcı tercih edebilsin diye: "mode1" = 3 yanlış = 1 doğru (default),
# "mode2" = her yanlış 1.25 net götür (alternatif).
penalty_mode = "mode1"  # "mode1" veya "mode2"

# ---------- Yardımcı popup fonksiyonu ----------
def show_popup(title, message, size=(0.8, 0.4)):
    popup = Popup(title=title, content=Label(text=message), size_hint=size)
    popup.open()

# ---------- Giriş Ekranı ----------
class GirisEkrani(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        layout = FloatLayout()

        # Arka plan resmi
        bg = Image(source='arka_plan.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)  # en altta olacak şekilde önce ekleniyor

        # Başlık (üstüne diğer widget'lar ekleniyor)
        baslik = Label(
            text="Dopamined 😎",
            font_size='32sp',
            size_hint=(0.9, 0.12),
            pos_hint={"center_x": 0.5, "top": 0.95},
            color=(1, 0.9, 0.6, 1)
        )
        layout.add_widget(baslik)

        alt_yazi = Label(
            text="Motivasyon ve verimlilik için uygulaman",
            font_size='14sp',
            size_hint=(0.95, 0.06),
            pos_hint={"center_x": 0.5, "top": 0.86},
            color=(0.8,0.8,0.9,1)
        )
        layout.add_widget(alt_yazi)

        # Butonları dikey, responsive yap
        btn_h = 0.08
        gap = 0.12

        puan_btn = Button(
            text="LGS Puan Hesaplayıcı",
            size_hint=(0.8, btn_h),
            pos_hint={"center_x": 0.5, "top": 0.75},
            background_normal='',
            background_color=(0.15,0.6,0.9,1)
        )
        puan_btn.bind(on_release=lambda x: setattr(app.sm, "current", "puan"))
        layout.add_widget(puan_btn)

        hedef_btn = Button(
            text="Hedef Lise Seçimi",
            size_hint=(0.8, btn_h),
            pos_hint={"center_x": 0.5, "top": 0.75 - gap},
            background_normal='',
            background_color=(0.2,0.7,0.4,1)
        )
        hedef_btn.bind(on_release=lambda x: setattr(app.sm, "current", "hedef_lise"))
        layout.add_widget(hedef_btn)

        cizelge_btn = Button(
            text="Haftalık Çizelge",
            size_hint=(0.8, btn_h),
            pos_hint={"center_x": 0.5, "top": 0.75 - gap*2},
            background_normal='',
            background_color=(0.9,0.6,0.2,1)
        )
        cizelge_btn.bind(on_release=lambda x: setattr(app.sm, "current", "cizelge"))
        layout.add_widget(cizelge_btn)

        exit_btn = Button(
            text="X",
            size_hint=(0.11, 0.06),
            pos_hint={"right": 0.985, "top": 0.985},
            background_normal='',
            background_color=(0.9,0.2,0.2,1)
        )
        exit_btn.bind(on_release=lambda x: app.stop())
        layout.add_widget(exit_btn)

        self.add_widget(layout)

# ---------- Haftalık Çizelge ----------
class CizelgeEkrani(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        main_layout = BoxLayout(orientation='vertical', padding=6, spacing=6)

        header = BoxLayout(size_hint=(1, None), height=48, padding=6)
        back_btn = Button(text="< Geri", size_hint=(None,1), width=100)
        title = Label(text="📅 Haftalık Çizelge", size_hint=(1,1))
        exit_btn = Button(text="X", size_hint=(None,1), width=80)
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(exit_btn)
        back_btn.bind(on_release=lambda x: setattr(app.sm, "current", "giris"))
        exit_btn.bind(on_release=lambda x: app.stop())
        main_layout.add_widget(header)

        # Scrollable grid: saat sütununu düzenli responsive yapıyoruz
        scroll = ScrollView(size_hint=(1,1), do_scroll_x=True, do_scroll_y=True)
        satir_sayisi = 24
        sutun_sayisi = 8

        grid = GridLayout(cols=sutun_sayisi, rows=satir_sayisi+1, size_hint=(None,None), spacing=2, padding=2)
        grid.bind(minimum_height=grid.setter('height'), minimum_width=grid.setter('width'))

        # genişlik hesap: pencere genişliğinin bir parçasına göre, ama minimum genişlik ver
        col_w = max(100, int(Window.width * 0.12))
        grid.width = col_w * sutun_sayisi
        grid.height = 40 * (satir_sayisi + 1)

        # başlık
        grid.add_widget(Label(text="", size_hint=(None,None), width=col_w, height=40))
        gunler = ["Pzt","Sal","Çar","Per","Cum","Cts","Paz"]
        for gun in gunler:
            grid.add_widget(Label(text=gun, size_hint=(None,None), width=col_w, height=40))

        for i in range(1,25):
            saat = f"{i:02d}:00" if i != 24 else "00:00"
            ti_saat = TextInput(text=saat, size_hint=(None,None), width=col_w, height=40, multiline=False)
            grid.add_widget(ti_saat)
            for _ in range(7):
                ti = TextInput(size_hint=(None,None), width=col_w, height=40, multiline=False)
                grid.add_widget(ti)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

# ---------- LGS Puan Hesaplayıcı ----------
class PuanEkrani(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        main_layout = BoxLayout(orientation='vertical', padding=8, spacing=8)

        header = BoxLayout(size_hint=(1, None), height=48)
        back_btn = Button(text="< Geri", size_hint=(None,1), width=100)
        title = Label(text="LGS Puan Hesaplayıcı", size_hint=(1,1))
        header.add_widget(back_btn)
        header.add_widget(title)
        back_btn.bind(on_release=lambda x: setattr(app.sm, "current", "giris"))
        main_layout.add_widget(header)

        scroll = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation='vertical', spacing=10, padding=6, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        self.ids_dict = {}
        dersler = [
            ("Türkçe", "turkce"),
            ("Matematik", "mat"),
            ("Fen Bilimleri", "fen"),
            ("T.C. İnkılap Tarihi", "inkilap"),
            ("Din Kültürü", "din"),
            ("İngilizce", "ing")
        ]

        for ders_ad, ders_key in dersler:
            row = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=48)
            lbl = Label(text=ders_ad, size_hint_x=0.4)
            d_input = TextInput(hint_text="Doğru", input_filter='int', multiline=False, size_hint_x=0.3)
            y_input = TextInput(hint_text="Yanlış", input_filter='int', multiline=False, size_hint_x=0.3)
            row.add_widget(lbl)
            row.add_widget(d_input)
            row.add_widget(y_input)
            box.add_widget(row)
            self.ids_dict[f"{ders_key}_d"] = d_input
            self.ids_dict[f"{ders_key}_y"] = y_input

        scroll.add_widget(box)
        main_layout.add_widget(scroll)

        # Penalty mode göstergesi + buton seçme (switch yoksa basit buton)
        mode_row = BoxLayout(size_hint=(1, None), height=44, spacing=8)
        mode_label = Label(text="Puanlama modu:", size_hint_x=0.5, valign='middle')
        self.mode_btn = Button(text="3 yanlış = 1 doğru (aktif)" if penalty_mode == "mode1" else "her yanlış -1.25 net", size_hint_x=0.5)
        self.mode_btn.bind(on_release=self.toggle_mode)
        mode_row.add_widget(mode_label)
        mode_row.add_widget(self.mode_btn)
        main_layout.add_widget(mode_row)

        calc_btn = Button(text="PUANI HESAPLA", size_hint=(0.8, None), height=52, pos_hint={'center_x':0.5}, background_normal='', background_color=(0.2,0.5,0.9,1))
        calc_btn.bind(on_release=lambda x: app.hesapla())
        main_layout.add_widget(calc_btn)

        self.add_widget(main_layout)

    def toggle_mode(self, *args):
        global penalty_mode
        if penalty_mode == "mode1":
            penalty_mode = "mode2"
            self.mode_btn.text = "her yanlış -1.25 net (aktif)"
        else:
            penalty_mode = "mode1"
            self.mode_btn.text = "3 yanlış = 1 doğru (aktif)"

# ---------- Hedef Lise Ekranı ----------
class HedefLiseEkrani(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.secilen_liseler_list = []
        main_layout = BoxLayout(orientation='vertical', padding=6, spacing=6)

        header = BoxLayout(size_hint=(1, None), height=48)
        back_btn = Button(text="< Geri", size_hint=(None,1), width=100)
        title = Label(text="Hedef Liseler", size_hint=(1,1))
        header.add_widget(back_btn)
        header.add_widget(title)
        back_btn.bind(on_release=lambda x: setattr(app.sm, "current", "giris"))
        main_layout.add_widget(header)

        # Seçilen liseler alanı
        self.secilen_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=6, padding=4)
        self.secilen_box.bind(minimum_height=self.secilen_box.setter('height'))
        main_layout.add_widget(Label(text="Seçilen Liseler (max 5)", size_hint=(1,None), height=30))
        main_layout.add_widget(self.secilen_box)

        # Tüm liseler scroll
        scroll = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation='vertical', spacing=6, padding=6, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        self.lise_secim = {}

        for l in sorted(LISLE_DB, key=lambda x: x["puan"], reverse=True):
            if l["puan"] < 400:
                continue
            row = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=40)
            cb = CheckBox(size_hint=(None,None), size=(30,30))
            lbl = Label(text=f"{l['isim']} — {l['sehir']} — {l['puan']:.2f}")
            row.add_widget(cb)
            row.add_widget(lbl)
            box.add_widget(row)
            self.lise_secim[l['isim']] = (cb, l)

            def on_checkbox_active(checkbox, value, lise=l):
                if value:
                    if len(self.secilen_liseler_list) >= 5:
                        checkbox.active = False
                        show_popup("Uyarı", "En fazla 5 lise seçebilirsiniz!")
                        return
                    self.add_secilen_lise(lise)
                else:
                    self.remove_secilen_lise(lise)
            cb.bind(active=on_checkbox_active)

        scroll.add_widget(box)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def add_secilen_lise(self, lise):
        for child in self.secilen_box.children:
            if getattr(child, "lise_name", None) == lise['isim']:
                return
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=36)
        lbl = Label(text=f"{lise['isim']} — {lise['sehir']} — {lise['puan']:.2f}", size_hint_x=0.85, color=(0.9,0.9,0.9,1))
        del_btn = Button(text="Sil", size_hint_x=0.15)
        row.add_widget(lbl)
        row.add_widget(del_btn)
        row.lise_name = lise['isim']
        self.secilen_box.add_widget(row, index=0)
        self.secilen_liseler_list.append(lise)
        del_btn.bind(on_release=lambda x, l=lise: self.remove_secilen_lise(l))

    def remove_secilen_lise(self, lise):
        for child in list(self.secilen_box.children):
            if getattr(child, "lise_name", None) == lise['isim']:
                self.secilen_box.remove_widget(child)
        self.secilen_liseler_list = [l for l in self.secilen_liseler_list if l['isim'] != lise['isim']]
        cb, _ = self.lise_secim.get(lise['isim'], (None,None))
        if cb:
            cb.active = False

# ---------- App ----------
class DopaminedApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(GirisEkrani(app=self, name="giris"))
        self.sm.add_widget(PuanEkrani(app=self, name="puan"))
        self.sm.add_widget(HedefLiseEkrani(app=self, name="hedef_lise"))
        self.sm.add_widget(CizelgeEkrani(app=self, name="cizelge"))
        return self.sm

    def hesapla(self):
        try:
            screen = self.sm.get_screen("puan")
            toplam_net = 0.0
            dersler = ["turkce", "mat", "fen", "inkilap", "din", "ing"]

            for key in dersler:
                max_soru = DERS_SORULAR[key]
                d_text = screen.ids_dict.get(f"{key}_d")
                y_text = screen.ids_dict.get(f"{key}_y")

                if not d_text or not y_text:
                    continue

                try:
                    d = int(d_text.text.strip() or 0)
                    y = int(y_text.text.strip() or 0)
                except ValueError:
                    popup = Popup(
                        title="Hata",
                        content=Label(text=f"{key.upper()} dersinde geçersiz sayı!"),
                        size_hint=(0.7, 0.4)
                    )
                    popup.open()
                    return

                if d < 0 or y < 0:
                    popup = Popup(
                        title="Hata",
                        content=Label(text=f"{key.upper()} dersinde negatif sayı olamaz!"),
                        size_hint=(0.7,0.4)
                    )
                    popup.open()
                    return

                if d + y > max_soru:
                    popup = Popup(
                        title="Hata",
                        content=Label(text=f"{key.upper()} dersinde toplam doğru+yanlış {max_soru}'u geçemez!"),
                        size_hint=(0.7,0.4)
                    )
                    popup.open()
                    return

                net = d - (y / 3)
                if net < 0:
                    net = 0
                toplam_net += net

            toplam_puan = toplam_net * 4 + 100
            if toplam_puan > 500:
                toplam_puan = 500

            popup = Popup(
                title="Tahmini Puan",
                content=Label(text=f"Tahmini Puan: {toplam_puan:.2f}"),
                size_hint=(0.8,0.5)
            )
            popup.open()

        except Exception as e:
            popup = Popup(
                title="Hata",
                content=Label(text=f"Beklenmedik bir hata oluştu: {e}"),
                size_hint=(0.8,0.5)
            )
            popup.open()




if __name__ == "__main__":
    DopaminedApp().run()
