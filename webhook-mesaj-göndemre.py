import sys
import requests
import re
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QPushButton, QTextEdit, QComboBox,
                             QLabel, QLineEdit, QColorDialog, QMessageBox,
                             QGroupBox, QFrame, QScrollArea, QCheckBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QSettings 

class SafWebhookStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Saf Discord Webhook Studio v20 (Kusursuz Rehber & Ultimate Önizleme)")
        self.resize(1450, 850) 
        
        self.hafiza = QSettings("DiscordStudio", "WebhookUygulamam")
        
        self.setStyleSheet("""
            QMainWindow { background-color: #313338; } 
            QWidget#appPanel { background-color: #313338; }
            QWidget#previewPanel { background-color: #313338; border-left: 1px solid #1E1F22; }
            
            QScrollArea { border: none; background-color: #313338; }
            QScrollArea#guideScroll { background-color: #2B2D31; border-right: 1px solid #1E1F22; }
            QWidget#guidePanel { background-color: #2B2D31; }
            
            QScrollBar:vertical { background: #2B2D31; width: 14px; margin: 0px; border-left: 1px solid #1E1F22;}
            QScrollBar::handle:vertical { background: #1A1B1E; min-height: 20px; border-radius: 7px; margin: 3px; }
            QScrollBar::handle:vertical:hover { background: #4E5058; }
            
            QPushButton { background-color: #5865F2; border-radius: 4px; color: white; padding: 10px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background-color: #4752C4; }
            QPushButton#btnGri { background-color: #4E5058; color: #DCDDDE; font-size: 13px;}
            QPushButton#btnGri:hover { background-color: #6D6F78; }
            QPushButton#btnKirmizi { background-color: #DA373C; font-size: 14px; padding: 5px; }
            QPushButton#btnKirmizi:hover { background-color: #A12828; }
            
            QPushButton#btnSembol { 
                background-color: #1E1F22; color: #23A559; font-weight: bold; font-size: 14px; 
                padding: 5px; border-radius: 4px; border: 1px solid #111214;
            }
            QPushButton#btnSembol:hover { background-color: #3F4147; color: #FFFFFF; }
            
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1E1F22; border: 1px solid #111214; border-radius: 4px;
                color: #DBDEE1; padding: 10px; font-size: 13px;
            }
            QLabel { color: #F2F3F5; font-size: 14px; font-weight: bold; }
            QLabel#RehberBaslik { color: #FFFFFF; font-size: 16px; font-weight: 900; margin-bottom: 5px; }
            QLabel#RehberMetin { color: #B5BAC1; font-size: 12px; font-weight: normal; line-height: 1.4; }
            QLabel#RehberVurgu { color: #23A559; font-size: 13px; font-weight: bold; font-family: Consolas, monospace; }
            QLabel#RehberOrnek { color: #80848E; font-size: 11px; font-style: italic; margin-bottom: 6px; }
            
            QGroupBox { border: 1px solid #1E1F22; border-radius: 6px; margin-top: 15px; padding-top: 15px; color: #B5BAC1; font-weight: bold; font-size: 13px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
            QStatusBar { background-color: #1E1F22; color: #DBDEE1; font-weight: bold; }
            
            QCheckBox { color: #DBDEE1; font-size: 14px; font-weight: bold; }
            QWebEngineView { background-color: #313338; border: none; }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SOL PANEL (KAYDIRILABİLİR REHBER - RESTORE EDİLDİ) =================
        self.guide_scroll = QScrollArea()
        self.guide_scroll.setObjectName("guideScroll")
        self.guide_scroll.setWidgetResizable(True)
        self.guide_scroll.setFixedWidth(320)

        guide_panel = QWidget()
        guide_panel.setObjectName("guidePanel")
        guide_layout = QVBoxLayout(guide_panel)
        guide_layout.setContentsMargins(15, 20, 15, 20)
        
        lbl_rb_baslik = QLabel("📚 Hızlı Rehber"); lbl_rb_baslik.setObjectName("RehberBaslik")
        guide_layout.addWidget(lbl_rb_baslik)

        # 1. BÖLÜM: Detaylı ID Alma Rehberi
        rehber_adimlar = (
            "Webhook'lar sunucu verilerini otomatik "
            "okuyamaz. Bu yüzden etiketleme yapmak "
            "için Discord Ayarlarından <b>Gelişmiş -> Geliştirici Modu</b>'nu "
            "açıp ID kopyalaman gerekir.<br><br>"
            "📌 <b>Nasıl Yapılır?</b><br>"
            "<b>1.</b> Kişi, rol veya kanala sağ tıklayın.<br>"
            "<b>2.</b> <b>ID'yi Kopyala</b> seçeneğine tıklayın.<br>"
            "<b>3.</b> Kopyalanan ID'yi şablonlara yapıştırın."
        )
        lbl_adimlar = QLabel(rehber_adimlar); lbl_adimlar.setObjectName("RehberMetin")
        lbl_adimlar.setTextFormat(Qt.RichText); lbl_adimlar.setWordWrap(True)
        guide_layout.addWidget(lbl_adimlar)

        line1 = QFrame(); line1.setFrameShape(QFrame.HLine); line1.setStyleSheet("background-color: #1E1F22; margin-top: 5px; margin-bottom: 5px;")
        guide_layout.addWidget(line1)

        # 2. BÖLÜM: Şablonlar ve Görsel Örnekler (Örn: kısmı geri geldi)
        def rehber_sekmesi_ekle(baslik, sablon, ornek):
            guide_layout.addWidget(QLabel(baslik))
            lbl_sablon = QLabel(sablon); lbl_sablon.setObjectName("RehberVurgu"); lbl_sablon.setTextInteractionFlags(Qt.TextSelectableByMouse)
            guide_layout.addWidget(lbl_sablon)
            lbl_ornek = QLabel(f"Örn: {ornek}"); lbl_ornek.setObjectName("RehberOrnek")
            guide_layout.addWidget(lbl_ornek)

        rehber_sekmesi_ekle("👤 Kişi Etiketleme:", "<@ID_Buraya>", "<@72314569874521>")
        rehber_sekmesi_ekle("🎭 Rol Etiketleme:", "<@&ID_Buraya>", "<@&98765432101234>")
        rehber_sekmesi_ekle("💬 Kanal Etiketleme:", "<#ID_Buraya>", "<#11223344556677>")
        rehber_sekmesi_ekle("✨ Emoji Gönderme:", "<:isim:ID_Buraya>", "<:pepe:1234567890>")

        line2 = QFrame(); line2.setFrameShape(QFrame.HLine); line2.setStyleSheet("background-color: #1E1F22; margin-top: 5px; margin-bottom: 5px;")
        guide_layout.addWidget(line2)

        # 3. BÖLÜM: Resim Linkleri Kuralı (Geri Getirildi)
        guide_layout.addWidget(QLabel("🖼️ Resim Linkleri Kuralı"))
        lbl_resim_kural = QLabel(
            "Resim linkleri mutlaka <b>.png, .jpg, .gif</b> uzantısı ile bitmelidir. Normal web siteleri çalışmaz!<br>"
            "<b>✅ Taktik:</b> Resmi Discord'a rastgele yükleyip <b>'Bağlantıyı Kopyala'</b> diyerek sorunsuz kullanabilirsiniz."
        )
        lbl_resim_kural.setObjectName("RehberMetin"); lbl_resim_kural.setWordWrap(True)
        lbl_resim_kural.setTextFormat(Qt.RichText)
        guide_layout.addWidget(lbl_resim_kural)
        
        rehber_sekmesi_ekle("🔗 Yazıya Link Ekleme:", "[Yazı](https://link.com)", "[Tıkla](https://google.com)")

        line3 = QFrame(); line3.setFrameShape(QFrame.HLine); line3.setStyleSheet("background-color: #1E1F22; margin-top: 5px; margin-bottom: 5px;")
        guide_layout.addWidget(line3)

        # 4. BÖLÜM: Metin Biçimlendirme
        guide_layout.addWidget(QLabel("✍️ Metin Biçimlendirme"))
        rehber_sekmesi_ekle("Kalın (Bold):", "**Yazı**", "**Merhaba**")
        rehber_sekmesi_ekle("Eğik (Italic):", "*Yazı*", "*Merhaba*")
        rehber_sekmesi_ekle("Altı Çizili:", "__Yazı__", "__Merhaba__")

        guide_layout.addStretch()

        # 5. BÖLÜM: Hızlı Sembol Kopyalama
        guide_layout.addWidget(QLabel("⚡ Semboller (Tıkla Kopyala)"))
        sembol_layout = QHBoxLayout()
        for s in ["<", ">", "&", "@", "#", "\\", "[", "]"]: 
            btn = QPushButton(s); btn.setObjectName("btnSembol")
            btn.clicked.connect(lambda checked, text=s: self.sembol_kopyala(text))
            sembol_layout.addWidget(btn)
        guide_layout.addLayout(sembol_layout)
        
        self.guide_scroll.setWidget(guide_panel)
        main_layout.addWidget(self.guide_scroll)

        # ================= ORTA PANEL (KAYDIRILABİLİR EDİTÖR) =================
        self.app_scroll = QScrollArea()
        self.app_scroll.setWidgetResizable(True)
        
        app_panel = QWidget()
        app_panel.setObjectName("appPanel")
        app_layout = QVBoxLayout(app_panel)
        app_layout.setContentsMargins(20, 20, 20, 20)
        app_layout.setSpacing(10)

        wh_grup = QGroupBox("1. Webhook Bağlantı & Kimlik")
        wh_layout = QVBoxLayout(wh_grup)
        self.inp_webhook_url = QLineEdit(); self.inp_webhook_url.setPlaceholderText("Webhook URL'sini Buraya Yapıştırın (Zorunlu)")
        wh_layout.addWidget(self.inp_webhook_url)

        wh_kimlik_layout = QHBoxLayout()
        self.inp_wh_name = QLineEdit(); self.inp_wh_name.setPlaceholderText("İsim (Örn: Duyuru Botu)")
        self.inp_wh_avatar = QLineEdit(); self.inp_wh_avatar.setPlaceholderText("Avatar URL (https:// ile başlamalı)")
        wh_kimlik_layout.addWidget(self.inp_wh_name)
        wh_kimlik_layout.addWidget(self.inp_wh_avatar)
        wh_layout.addLayout(wh_kimlik_layout)
        app_layout.addWidget(wh_grup)

        ayarlar_layout = QHBoxLayout()
        self.combo_tip = QComboBox()
        self.combo_tip.addItems(["Düz Mesaj", "Embed (Kart) Mesaj"])
        ayarlar_layout.addWidget(QLabel("Tip:")); ayarlar_layout.addWidget(self.combo_tip, stretch=2)
        
        ayarlar_layout.addWidget(QLabel("Ping:")); 
        self.chk_everyone = QCheckBox("@everyone")
        self.chk_here = QCheckBox("@here")
        self.chk_spoiler = QCheckBox("Spoiler ||Gizle||")
        ayarlar_layout.addWidget(self.chk_everyone)
        ayarlar_layout.addWidget(self.chk_here)
        ayarlar_layout.addWidget(self.chk_spoiler)
        app_layout.addLayout(ayarlar_layout)

        self.duz_mesaj_grup = QGroupBox("İçerik: Düz Mesaj")
        duz_layout = QVBoxLayout(self.duz_mesaj_grup)
        self.txt_mesaj = QTextEdit(); self.txt_mesaj.setPlaceholderText("Mesajınızı yazın... (Markdown ve kanal etiketleri kullanabilirsiniz)")
        self.txt_mesaj.setMaximumHeight(150)
        duz_layout.addWidget(self.txt_mesaj)
        app_layout.addWidget(self.duz_mesaj_grup)

        self.embed_grup = QGroupBox("İçerik: Profesyonel Embed Tasarımı")
        embed_layout = QVBoxLayout(self.embed_grup)

        author_layout = QHBoxLayout()
        self.inp_author_name = QLineEdit(); self.inp_author_name.setPlaceholderText("Yazar Adı (Kartın En Üstü)")
        self.inp_author_icon = QLineEdit(); self.inp_author_icon.setPlaceholderText("Yazar İkonu URL")
        author_layout.addWidget(self.inp_author_name, stretch=2); author_layout.addWidget(self.inp_author_icon, stretch=2)
        embed_layout.addLayout(author_layout)

        self.inp_title = QLineEdit(); self.inp_title.setPlaceholderText("Ana Başlık")
        self.inp_desc = QTextEdit(); self.inp_desc.setPlaceholderText("Embed Açıklaması...")
        self.inp_desc.setMinimumHeight(100)
        embed_layout.addWidget(self.inp_title); embed_layout.addWidget(self.inp_desc)

        self.fields_layout = QVBoxLayout()
        embed_layout.addLayout(self.fields_layout)
        self.embed_fields_data = [] 
        
        self.btn_alan_ekle = QPushButton("+ Yeni Alt Sütun (Field) Ekle")
        self.btn_alan_ekle.setObjectName("btnGri")
        self.btn_alan_ekle.clicked.connect(self.alan_ekle)
        embed_layout.addWidget(self.btn_alan_ekle)

        resim_layout = QHBoxLayout()
        self.inp_image = QLineEdit(); self.inp_image.setPlaceholderText("Büyük Alt Resim URL")
        self.inp_thumb = QLineEdit(); self.inp_thumb.setPlaceholderText("Sağ Üst Küçük Resim (Thumbnail) URL")
        resim_layout.addWidget(self.inp_image); resim_layout.addWidget(self.inp_thumb)
        embed_layout.addLayout(resim_layout)

        footer_layout = QHBoxLayout()
        self.inp_footer_text = QLineEdit(); self.inp_footer_text.setPlaceholderText("En Alt Bilgi (Footer) Yazısı")
        self.inp_footer_icon = QLineEdit(); self.inp_footer_icon.setPlaceholderText("Alt Bilgi İkonu URL")
        footer_layout.addWidget(self.inp_footer_text, stretch=2); footer_layout.addWidget(self.inp_footer_icon, stretch=1)
        embed_layout.addLayout(footer_layout)

        alt_ayar_layout = QHBoxLayout()
        self.inp_color = QLineEdit(); self.inp_color.setPlaceholderText("Renk (#FFC4E8)")
        btn_renk = QPushButton("🎨"); btn_renk.setObjectName("btnGri"); btn_renk.setFixedWidth(40)
        btn_renk.clicked.connect(self.renk_secici_ac)
        
        self.chk_timestamp = QCheckBox("Güncel Saati Ekle")
        self.chk_timestamp.setChecked(False)
        self.chk_timestamp.stateChanged.connect(self.onizlemeyi_ciz)
        
        alt_ayar_layout.addWidget(self.inp_color); alt_ayar_layout.addWidget(btn_renk)
        alt_ayar_layout.addWidget(self.chk_timestamp)
        alt_ayar_layout.addStretch()
        embed_layout.addLayout(alt_ayar_layout)

        app_layout.addWidget(self.embed_grup)

        app_layout.addStretch()
        self.btn_gonder = QPushButton("WEBHOOK İLE MESAJI GÖNDER 🚀")
        self.btn_gonder.setMinimumHeight(60)
        self.btn_gonder.clicked.connect(self.webhook_ile_gonder)
        app_layout.addWidget(self.btn_gonder)
        
        self.app_scroll.setWidget(app_panel)
        main_layout.addWidget(self.app_scroll, stretch=5)

        # ================= SAĞ PANEL (CANLI ÖNİZLEME) =================
        preview_panel = QWidget()
        preview_panel.setObjectName("previewPanel")
        preview_panel.setMinimumWidth(480)
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(15, 20, 15, 20)

        lbl_prv_baslik = QLabel("👁️ Canlı Önizleme"); lbl_prv_baslik.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 900; margin-bottom: 5px;")
        preview_layout.addWidget(lbl_prv_baslik)

        self.browser_onizleme = QWebEngineView()
        self.browser_onizleme.page().setBackgroundColor(Qt.transparent)
        preview_layout.addWidget(self.browser_onizleme)
        
        main_layout.addWidget(preview_panel, stretch=4)

        # CANLI GÜNCELLEME SİNYALLERİ
        self.combo_tip.currentIndexChanged.connect(self.arayuz_guncelle)
        
        self.chk_everyone.stateChanged.connect(self.onizlemeyi_ciz)
        self.chk_here.stateChanged.connect(self.onizlemeyi_ciz)
        self.chk_spoiler.stateChanged.connect(self.onizlemeyi_ciz)

        self.inp_wh_name.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_wh_avatar.textChanged.connect(self.onizlemeyi_ciz)
        self.txt_mesaj.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_author_name.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_author_icon.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_title.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_desc.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_color.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_image.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_thumb.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_footer_text.textChanged.connect(self.onizlemeyi_ciz)
        self.inp_footer_icon.textChanged.connect(self.onizlemeyi_ciz)

        self.onceki_verileri_yukle()
        self.arayuz_guncelle()
        self.onizlemeyi_ciz() 

    # --- ÖZELLİKLER VE FONKSİYONLAR ---
    
    def alan_ekle(self):
        if len(self.embed_fields_data) >= 10: return QMessageBox.warning(self, "Sınır", "En fazla 10 alan ekleyebilirsiniz.")
        alan_widget = QWidget()
        alan_layout = QHBoxLayout(alan_widget)
        alan_layout.setContentsMargins(0, 0, 0, 0)
        
        isim = QLineEdit(); isim.setPlaceholderText("Alt Başlık")
        deger = QLineEdit(); deger.setPlaceholderText("Değer")
        inline = QCheckBox("Yan Yana")
        inline.setChecked(True)
        btn_sil = QPushButton("X"); btn_sil.setObjectName("btnKirmizi"); btn_sil.setFixedWidth(30)
        
        alan_layout.addWidget(isim, stretch=2)
        alan_layout.addWidget(deger, stretch=3)
        alan_layout.addWidget(inline)
        alan_layout.addWidget(btn_sil)
        self.fields_layout.addWidget(alan_widget)
        
        alan_verisi = {"widget": alan_widget, "name": isim, "value": deger, "inline": inline}
        self.embed_fields_data.append(alan_verisi)
        
        isim.textChanged.connect(self.onizlemeyi_ciz)
        deger.textChanged.connect(self.onizlemeyi_ciz)
        inline.stateChanged.connect(self.onizlemeyi_ciz)
        btn_sil.clicked.connect(lambda: self.alan_sil(alan_verisi))
        self.onizlemeyi_ciz()

    def alan_sil(self, alan_verisi):
        self.fields_layout.removeWidget(alan_verisi["widget"])
        alan_verisi["widget"].deleteLater()
        if alan_verisi in self.embed_fields_data:
            self.embed_fields_data.remove(alan_verisi)
        self.onizlemeyi_ciz()

    def markdown_cevir(self, metin):
        if not metin: return ""
        metin = metin.replace("\n", "<br>")
        metin = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', metin) 
        metin = re.sub(r'\*(.*?)\*', r'<i>\1</i>', metin)     
        metin = re.sub(r'__(.*?)__', r'<u>\1</u>', metin)     
        metin = re.sub(r'~~(.*?)~~', r'<s>\1</s>', metin)
        metin = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color: #00A8FC; text-decoration: none;">\1</a>', metin)
        metin = re.sub(r'<#(\d+)>', r'<span class="ping">#kanal</span>', metin)
        return metin

    def onizlemeyi_ciz(self):
        isim = self.inp_wh_name.text().strip() or "Spidey Bot"
        avatar = self.inp_wh_avatar.text().strip() or "https://cdn.discordapp.com/embed/avatars/0.png"
        
        ping_list = []
        if self.chk_everyone.isChecked(): ping_list.append("@everyone")
        if self.chk_here.isChecked(): ping_list.append("@here")
        
        ping_metni = ""
        if ping_list:
            birlestirilmis = " ".join(ping_list)
            if self.chk_spoiler.isChecked():
                ping_metni = f"<span class='spoiler'><span class='ping'>{birlestirilmis}</span></span><br><br>"
            else:
                ping_metni = f"<span class='ping'>{birlestirilmis}</span><br><br>"
        
        tip = self.combo_tip.currentText()
        mesaj = self.markdown_cevir(self.txt_mesaj.toPlainText().strip())
        
        embed_author_name = self.markdown_cevir(self.inp_author_name.text().strip())
        embed_author_icon = self.inp_author_icon.text().strip()
        embed_baslik = self.markdown_cevir(self.inp_title.text().strip())
        embed_aciklama = self.markdown_cevir(self.inp_desc.toPlainText().strip())
        embed_renk = self.inp_color.text().strip() or "#1E1F22"
        embed_resim = self.inp_image.text().strip()
        embed_thumb = self.inp_thumb.text().strip()
        embed_footer_text = self.inp_footer_text.text().strip()
        embed_footer_icon = self.inp_footer_icon.text().strip()
        
        html = f"""
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; }}
                body {{ font-family: 'gg sans', 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #313338; color: #DBDEE1; font-size: 16px; margin: 0; padding: 16px 20px; overflow-x: hidden; }}
                ::-webkit-scrollbar {{ width: 14px; height: 14px; }}
                ::-webkit-scrollbar-track {{ background: #2B2D31; border-radius: 8px; border: 3px solid #313338; }}
                ::-webkit-scrollbar-thumb {{ background: #1A1B1E; border-radius: 8px; border: 3px solid #313338; }}
                ::-webkit-scrollbar-thumb:hover {{ background: #4E5058; }}

                .msg-container {{ display: flex; align-items: flex-start; gap: 16px; padding-left: 12px; }}
                .avatar {{ width: 40px; height: 40px; border-radius: 50%; object-fit: cover; flex-shrink: 0; margin-top: -2px; margin-left: -16px; }}
                .header {{ display: flex; align-items: center; gap: 6px; margin-bottom: 4px; line-height: 1.2; }}
                .username {{ color: #F2F3F5; font-size: 16px; font-weight: 500; }}
                .bot-tag {{ background-color: #5865F2; color: white; font-size: 10px; padding: 2px 4px; border-radius: 3px; font-weight: bold; display: flex; align-items: center; }}
                .timestamp {{ color: #80848E; font-size: 12px; }}
                .ping {{ background-color: rgba(88, 101, 242, 0.3); color: #C9CDD0; font-weight: 500; padding: 2px 4px; border-radius: 3px; display: inline-block; }}
                
                .spoiler {{ background-color: #202225; border-radius: 4px; padding: 0 4px; display: inline-block; cursor: pointer; }}
                .spoiler .ping {{ opacity: 0.2; transition: 0.2s; background-color: transparent; }}
                .spoiler:hover .ping {{ opacity: 1; }}

                .embed {{ background-color: #2B2D31; border-left: 4px solid {embed_renk}; border-radius: 4px; padding: 12px 16px 16px 16px; margin-top: 4px; max-width: 500px; display: flex; flex-direction: column; gap: 8px; }}
                .embed-content-wrapper {{ display: flex; flex-direction: row; gap: 16px; justify-content: space-between; }}
                .embed-main-content {{ flex: 1; min-width: 0; }}
                
                .embed-author {{ display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }}
                .embed-author-icon {{ width: 24px; height: 24px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }}
                .embed-author-name {{ color: #FFFFFF; font-weight: 600; font-size: 14px; line-height: 1; }}
                
                .embed-title {{ color: #FFFFFF; font-weight: 600; font-size: 16px; line-height: 1.2; margin-top: 2px; margin-bottom: 4px;}}
                .embed-description {{ color: #DBDEE1; font-size: 14px; line-height: 1.4; word-wrap: break-word; }}
                
                .embed-thumbnail {{ width: 80px; height: 80px; border-radius: 4px; object-fit: cover; flex-shrink: 0; }}
                .embed-image {{ margin-top: 8px; max-width: 100%; border-radius: 4px; object-fit: contain; }}
                
                .embed-fields {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 8px; }}
                .field {{ min-width: 0; word-wrap: break-word; }}
                .field-name {{ color: #FFFFFF; font-weight: 600; font-size: 14px; margin-bottom: 2px; }}
                .field-value {{ color: #DBDEE1; font-size: 14px; line-height: 1.4; }}
                
                .embed-footer {{ display: flex; align-items: center; gap: 8px; margin-top: 8px; }}
                .footer-icon {{ width: 20px; height: 20px; border-radius: 50%; object-fit: cover; }}
                .footer-text {{ color: #DBDEE1; font-size: 12px; font-weight: 500; }}
            </style>
        </head>
        <body>
            <div class="msg-container">
                <img src="{avatar}" class="avatar" onerror="this.src='https://cdn.discordapp.com/embed/avatars/0.png'">
                <div>
                    <div class="header">
                        <span class="username">{isim}</span>
                        <span class="bot-tag">APP</span>
                        <span class="timestamp">Bugün saat 12:00</span>
                    </div>
        """

        if tip == "Embed (Kart) Mesaj":
            if ping_metni: html += f"<div style='margin-bottom: 8px; line-height: 1.4;'>{ping_metni}</div>"
            
            html += "<div class='embed'><div class='embed-content-wrapper'><div class='embed-main-content'>"
            
            if embed_author_name:
                html += "<div class='embed-author'>"
                if embed_author_icon: html += f"<img src='{embed_author_icon}' class='embed-author-icon' onerror=\"this.style.display='none'\">"
                html += f"<span class='embed-author-name'>{embed_author_name}</span></div>"
                
            if embed_baslik: html += f"<div class='embed-title'>{embed_baslik}</div>"
            if embed_aciklama: html += f"<div class='embed-description'>{embed_aciklama}</div>"
            
            fields_html = ""
            for f in self.embed_fields_data:
                f_isim = self.markdown_cevir(f["name"].text().strip())
                f_deger = self.markdown_cevir(f["value"].text().strip())
                inl = f["inline"].isChecked()
                if f_isim and f_deger:
                    span_style = "" if inl else "grid-column: 1 / -1;"
                    fields_html += f"<div class='field' style='{span_style}'><div class='field-name'>{f_isim}</div><div class='field-value'>{f_deger}</div></div>"
            
            if fields_html: html += f"<div class='embed-fields'>{fields_html}</div>"

            html += "</div>" 
            
            if embed_thumb: html += f"<img src='{embed_thumb}' class='embed-thumbnail' onerror=\"this.style.display='none'\">"
            html += "</div>" 
            
            if embed_resim: html += f"<img src='{embed_resim}' class='embed-image' onerror=\"this.style.display='none'\">"
            
            if embed_footer_text or embed_footer_icon or self.chk_timestamp.isChecked():
                html += "<div class='embed-footer'>"
                if embed_footer_icon: html += f"<img src='{embed_footer_icon}' class='footer-icon' onerror=\"this.style.display='none'\">"
                
                f_yazi = embed_footer_text
                if self.chk_timestamp.isChecked():
                    f_yazi = f"{f_yazi} • Bugün saat 12:00" if f_yazi else "Bugün saat 12:00"
                    
                html += f"<span class='footer-text'>{f_yazi}</span></div>"
            
            html += "</div>" 
        else: 
            if mesaj or ping_metni: html += f"<div style='line-height: 1.4; margin-top: 4px;'>{ping_metni}{mesaj}</div>"

        html += "</div></div></body></html>"
        self.browser_onizleme.setHtml(html)

    def onceki_verileri_yukle(self):
        self.inp_webhook_url.setText(str(self.hafiza.value("url", "")))
        self.inp_wh_name.setText(str(self.hafiza.value("wh_name", "")))
        self.inp_wh_avatar.setText(str(self.hafiza.value("wh_avatar", "")))
        
        tip = str(self.hafiza.value("combo_tip", "Düz Mesaj"))
        if self.combo_tip.findText(tip) >= 0: self.combo_tip.setCurrentText(tip)
        
        if str(self.hafiza.value("chk_everyone", "false")).lower() == "true": self.chk_everyone.setChecked(True)
        if str(self.hafiza.value("chk_here", "false")).lower() == "true": self.chk_here.setChecked(True)
        if str(self.hafiza.value("chk_spoiler", "false")).lower() == "true": self.chk_spoiler.setChecked(True)
        
        self.txt_mesaj.setText(str(self.hafiza.value("txt_mesaj", "")))
        self.inp_author_name.setText(str(self.hafiza.value("author_name", "")))
        self.inp_author_icon.setText(str(self.hafiza.value("author_icon", "")))
        self.inp_title.setText(str(self.hafiza.value("title", "")))
        self.inp_desc.setText(str(self.hafiza.value("desc", "")))
        self.inp_thumb.setText(str(self.hafiza.value("thumb", "")))
        self.inp_footer_text.setText(str(self.hafiza.value("f_text", "")))
        self.inp_footer_icon.setText(str(self.hafiza.value("f_icon", "")))
        
        if str(self.hafiza.value("timestamp", "false")).lower() == "true": self.chk_timestamp.setChecked(True)
        
        renk = str(self.hafiza.value("color", "#FFC4E8"))
        self.inp_color.setText(renk if renk else "#FFC4E8")
        self.inp_image.setText(str(self.hafiza.value("image", "")))

    def verileri_hafizaya_kaydet(self):
        self.hafiza.setValue("url", self.inp_webhook_url.text().strip())
        self.hafiza.setValue("wh_name", self.inp_wh_name.text().strip())
        self.hafiza.setValue("wh_avatar", self.inp_wh_avatar.text().strip())
        self.hafiza.setValue("combo_tip", self.combo_tip.currentText())
        
        self.hafiza.setValue("chk_everyone", self.chk_everyone.isChecked())
        self.hafiza.setValue("chk_here", self.chk_here.isChecked())
        self.hafiza.setValue("chk_spoiler", self.chk_spoiler.isChecked())
        
        self.hafiza.setValue("txt_mesaj", self.txt_mesaj.toPlainText().strip())
        self.hafiza.setValue("author_name", self.inp_author_name.text().strip())
        self.hafiza.setValue("author_icon", self.inp_author_icon.text().strip())
        self.hafiza.setValue("title", self.inp_title.text().strip())
        self.hafiza.setValue("desc", self.inp_desc.toPlainText().strip())
        self.hafiza.setValue("thumb", self.inp_thumb.text().strip())
        self.hafiza.setValue("f_text", self.inp_footer_text.text().strip())
        self.hafiza.setValue("f_icon", self.inp_footer_icon.text().strip())
        self.hafiza.setValue("timestamp", self.chk_timestamp.isChecked())
        self.hafiza.setValue("color", self.inp_color.text().strip())
        self.hafiza.setValue("image", self.inp_image.text().strip())

    def closeEvent(self, event):
        self.verileri_hafizaya_kaydet()
        event.accept()

    def sembol_kopyala(self, sembol):
        cb = QApplication.clipboard()
        cb.setText(sembol)
        self.statusBar().showMessage(f"✅ Panoya Kopyalandı: {sembol}", 3000)

    def arayuz_guncelle(self):
        secim = self.combo_tip.currentText()
        if secim == "Embed (Kart) Mesaj":
            self.embed_grup.show()
            self.duz_mesaj_grup.hide()
        else:
            self.embed_grup.hide()
            self.duz_mesaj_grup.show()
        self.onizlemeyi_ciz()

    def renk_secici_ac(self):
        renk = QColorDialog.getColor(parent=self, title="Embed Rengini Seç")
        if renk.isValid():
            self.inp_color.setText(renk.name().upper())

    def webhook_ile_gonder(self):
        url = self.inp_webhook_url.text().strip()
        if not url: return QMessageBox.critical(self, "Hata", "Lütfen URL girin!")
        self.verileri_hafizaya_kaydet()

        veri = {}
        if self.inp_wh_name.text().strip(): veri["username"] = self.inp_wh_name.text().strip()
        if self.inp_wh_avatar.text().strip(): veri["avatar_url"] = self.inp_wh_avatar.text().strip()

        ping_listesi = []
        if self.chk_everyone.isChecked(): ping_listesi.append("@everyone")
        if self.chk_here.isChecked(): ping_listesi.append("@here")
        
        ping_metni = ""
        if ping_listesi:
            ping_metni = " ".join(ping_listesi)
            if self.chk_spoiler.isChecked():
                ping_metni = f"||{ping_metni}||"
            ping_metni += "\n" 

        if self.combo_tip.currentText() == "Embed (Kart) Mesaj":
            if ping_metni: veri["content"] = ping_metni
            embed = {}
            
            if self.inp_author_name.text().strip():
                embed["author"] = {"name": self.inp_author_name.text().strip()}
                if self.inp_author_icon.text().strip(): embed["author"]["icon_url"] = self.inp_author_icon.text().strip()
                    
            if self.inp_title.text().strip(): embed["title"] = self.inp_title.text().strip()
            if self.inp_desc.toPlainText().strip(): embed["description"] = self.inp_desc.toPlainText().strip()
            if self.inp_image.text().strip(): embed["image"] = {"url": self.inp_image.text().strip()}
            if self.inp_thumb.text().strip(): embed["thumbnail"] = {"url": self.inp_thumb.text().strip()}
            
            # YENİ ZAMAN DAMGASI KODU (HATASIZ)
            if self.chk_timestamp.isChecked(): 
                embed["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
            footer = {}
            if self.inp_footer_text.text().strip(): footer["text"] = self.inp_footer_text.text().strip()
            if self.inp_footer_icon.text().strip(): footer["icon_url"] = self.inp_footer_icon.text().strip()
            if footer: embed["footer"] = footer
            
            fields = []
            for f in self.embed_fields_data:
                f_isim = f["name"].text().strip()
                f_deger = f["value"].text().strip()
                if f_isim and f_deger:
                    fields.append({"name": f_isim, "value": f_deger, "inline": f["inline"].isChecked()})
            if fields: embed["fields"] = fields
            
            renk = self.inp_color.text().strip()
            if renk:
                try: embed["color"] = int(renk.replace("#", ""), 16)
                except: pass
                
            if embed: veri["embeds"] = [embed]
            else: return QMessageBox.warning(self, "Uyarı", "Embed içeriği girmelisiniz.")
        else: 
            mesaj = self.txt_mesaj.toPlainText().strip()
            if not mesaj and not ping_metni: return QMessageBox.warning(self, "Uyarı", "Mesaj yazmalısınız.")
            veri["content"] = ping_metni + mesaj

        try:
            cevap = requests.post(url, json=veri)
            if cevap.status_code in [200, 204]: self.statusBar().showMessage("✅ Webhook mesajı başarıyla hedefe ulaştı!")
            else: QMessageBox.critical(self, "Hata", f"Hata Kodu: {cevap.status_code}\nDetay: {cevap.text}")
        except Exception as e: QMessageBox.critical(self, "Bağlantı Hatası", f"İstek atılamadı.\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafWebhookStudio()
    window.show()
    sys.exit(app.exec_())