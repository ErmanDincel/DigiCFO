import streamlit as st
import os

# ==========================================
# ENVIRONMENT VARIABLES (.env dosyası)
# ==========================================
# .env dosyasından environment variables'ları yükle
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    # .env dosyası yoksa environment variables'dan okumaya devam eder

# ==========================================
# DATABASE INITIALIZATION
# ==========================================
# Veritabanı bağlantısını başlat (eğer .env dosyasında DB_ENABLED=true ise)
try:
    from db.database import init_database, is_database_configured
    if is_database_configured():
        init_database()
        DB_AVAILABLE = True
    else:
        DB_AVAILABLE = False
except Exception as e:
    DB_AVAILABLE = False
    # Veritabanı bağlantısı başarısız olursa sessizce devam et

# ==========================================
# CONFIGURATION IMPORT
# ==========================================
# Güvenlik: Şifreler config dosyasından okunur
try:
    from config import DEMO_USERNAME, DEMO_PASSWORD
except ImportError:
    # Fallback: Eğer config.py yoksa (eski versiyon uyumluluğu)
    DEMO_USERNAME = "DigiCFO"
    DEMO_PASSWORD = "12547"
    st.warning("⚠️ config.py bulunamadı. Varsayılan değerler kullanılıyor. Güvenlik için config.py oluşturun!")

# ==========================================
# MAPPING WIZARD IMPORT
# ==========================================
# Veri okuma esnekliği için mapping wizard
try:
    from mapping_wizard import show_mapping_wizard, load_mapping, save_mapping
    MAPPING_WIZARD_AVAILABLE = True
except ImportError:
    MAPPING_WIZARD_AVAILABLE = False
    st.warning("⚠️ mapping_wizard.py bulunamadı. Veri okuma esnekliği özelliği devre dışı.")

# ==========================================
# GELİŞMİŞ EXCEL OKUYUCU IMPORT
# ==========================================
# Farklı muhasebe ve ERP sistemlerinden gelen Excel dosyalarını okumak için
try:
    from excel_reader import read_excel_smart, read_excel_multi_sheet, analyze_excel_structure
    ADVANCED_EXCEL_READER_AVAILABLE = True
except ImportError:
    ADVANCED_EXCEL_READER_AVAILABLE = False
    # Fallback: Standart pandas okuma kullanılacak

# ==========================================
# TMS/UFRS UYUMLULUK SİSTEMİ IMPORT
# ==========================================
# Excel'den okunan verilerin TMS/UFRS uyumluluğunu kontrol eder
try:
    from tms_ufrs_compliance import (
        TMS_UFRS_ESLESTIRME,
        tms_ufrs_hesap_kontrol,
        tablo_tms_ufrs_analiz,
        create_tms_ufrs_table,
        show_tms_ufrs_compliance_report
    )
    TMS_UFRS_COMPLIANCE_AVAILABLE = True
except ImportError:
    TMS_UFRS_COMPLIANCE_AVAILABLE = False
    st.warning("⚠️ tms_ufrs_compliance.py bulunamadı. TMS/UFRS uyumluluk kontrolü devre dışı.")

# ==========================================
# UTILS IMPORT
# ==========================================
# Yardımcı fonksiyonlar (formatlama, export, veri temizleme)
try:
    from utils import (
        to_excel,
        to_pdf,
        to_html,
        clean_turkish_float,
        clean_turkish_float_hizli,
        turkce_duzelt,
        pdf_to_dataframe,
        style_rasyo_df,
        scale_df
    )
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    st.warning("⚠️ utils.py bulunamadı. Bazı export fonksiyonları devre dışı.")

# ==========================================
# MAPPING IMPORT
# ==========================================
# Veri standardizasyonu için mapping fonksiyonları
try:
    from mapping import (
        get_standard_mapping,
        get_standard_mapping_hizli,
        apply_user_mapping_to_df
    )
    MAPPING_AVAILABLE = True
except ImportError:
    MAPPING_AVAILABLE = False
    st.warning("⚠️ mapping.py bulunamadı. Veri standardizasyonu fonksiyonları devre dışı.")

# ==========================================
# TRANSLATION IMPORT
# ==========================================
# Finansal tablo çeviri fonksiyonları (TFRS uyumlu Türkçe çeviri)
try:
    from translation import (
        TFRS_CEVIRI_SOZLUK,
        cevir_finansal_tablo_turkce
    )
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    st.warning("⚠️ translation.py bulunamadı. Finansal tablo çeviri fonksiyonları devre dışı.")

# ==========================================
# CONVERTERS IMPORT
# ==========================================
# Finansal tablo converter sınıfları (Gelir Tablosu, Bilanço)
try:
    from converters import (
        SEMA_GELIR_TABLOSU,
        SEMA_BILANCO,
        SEMA_NAKIT_AKIS,
        GelirTablosuConverter,
        BilancoConverter
    )
    CONVERTERS_AVAILABLE = True
except ImportError:
    CONVERTERS_AVAILABLE = False
    st.warning("⚠️ converters.py bulunamadı. Finansal tablo converter fonksiyonları devre dışı.")

# ==========================================
# BUYUK VERI ENGINE IMPORT
# ==========================================
# Büyük veri birleştirme ve istatistik hesaplama motoru
try:
    from buyuk_veri_engine import BuyukVeriMotoru
    BUYUK_VERI_ENGINE_AVAILABLE = True
except ImportError:
    BUYUK_VERI_ENGINE_AVAILABLE = False
    st.warning("⚠️ buyuk_veri_engine.py bulunamadı. Büyük veri motoru fonksiyonları devre dışı.")

# ==========================================
# DATA_LOADER IMPORT
# ==========================================
# Veri yükleme fonksiyonları (BIST, TCMB, TÜİK)
try:
    from data_loader import (
        get_tcmb_doviz_kurlari,
        get_tuik_tufe_yillik,
        get_tufe_endeks_serisi,
        get_bist_haftalik_veri,
        get_bist_endeks_haftalik,
        yukle_bist_sektor_verileri
    )
    DATA_LOADER_AVAILABLE = True
except ImportError:
    DATA_LOADER_AVAILABLE = False
    st.warning("⚠️ data_loader.py bulunamadı. Veri yükleme fonksiyonları devre dışı.")

# ==========================================
# SESSION MANAGER IMPORT
# ==========================================
# Merkezi session state yönetimi
try:
    from session_manager import (
        init_app_session_state,
        init_session_state_defaults,
        get_session_value,
        set_session_value,
        clear_session_keys,
        validate_session_state
    )
    SESSION_MANAGER_AVAILABLE = True
except ImportError:
    SESSION_MANAGER_AVAILABLE = False
    st.warning("⚠️ session_manager.py bulunamadı. Session state yönetimi devre dışı.")

# ==========================================
# AUTH IMPORT
# ==========================================
# Giriş/çıkış fonksiyonları
try:
    from auth import (
        KULLANICI_TURLERI,
        init_session_state,
        show_login_page,
        show_logout_button,
        is_authenticated,
        get_current_user
    )
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False
    st.warning("⚠️ auth.py bulunamadı. Giriş/çıkış fonksiyonları devre dışı.")

# ==========================================
# FINANCIAL_ANALYZER IMPORT
# ==========================================
# Finansal analiz ve rasyo hesaplamaları
try:
    from financial_analyzer import (
        HESAPLAMA_YONTEMLERI,
        RasyoAnalizi,
        hesapla_rasyolar_cached,
        hesaplama_yontemi_kontrol
    )
    FINANCIAL_ANALYZER_AVAILABLE = True
except ImportError:
    FINANCIAL_ANALYZER_AVAILABLE = False
    st.warning("⚠️ financial_analyzer.py bulunamadı. Rasyo hesaplamaları devre dışı.")

# ==========================================
# VIEWS IMPORT
# ==========================================
# UI bileşenleri (dosya yükleme, firma bilgileri, dashboard, raporlama)
# Views modüllerini import et
from views import (
    show_file_upload_section,
    show_company_info_form,
    show_main_dashboard,
    show_reports_section,
    get_tab_index
)
from views.ham_veri import show_ham_veri_section
from views.finansal_analiz_pro import show_finansal_analiz_pro_section
from views.sektor import show_sektor_section
from views.gelir_tablosu import show_gelir_tablosu_section
from views.bilanco import show_bilanco_section
from views.nakit_akis import show_nakit_akis_section
from views.buyuk_veri import show_buyuk_veri_section
from views.rasyo_oran import show_rasyo_oran_section
from views.veri_onay import show_veri_onay_section
from views.ileri_analiz import show_ileri_analiz_section
from views.veri_kontrol import show_veri_kontrol_section

# ==========================================
# PERFORMANS OPTİMİZASYONU - LAZY IMPORT
# ==========================================
# Ağır kütüphaneler sadece gerektiğinde yüklenir

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import io
import json

# Lazy import için fonksiyonlar
@st.cache_resource
def get_plotly():
    """Plotly'i sadece bir kez yükle"""
    import plotly.graph_objects as go
    return go

# FPDF - PDF oluşturma için
from fpdf import FPDF

# Requests ve XML her zaman lazım
import requests
import xml.etree.ElementTree as ET

# Yahoo Finance için yfinance kütüphanesi
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

# Global plotly referansı
go = get_plotly()

# ==========================================
# FİNANSAL ORAN HESAPLAMA YÖNTEMLERİ
# ==========================================
# HESAPLAMA_YONTEMLERI artık financial_analyzer.py'de
# Import edildi: from financial_analyzer import HESAPLAMA_YONTEMLERI

# ==========================================
# TMS/UFRS UYUMLULUK KONTROL FONKSİYONLARI
# ==========================================
# Bu fonksiyonlar tms_ufrs_compliance.py modülünden import ediliyor
# Import edildi: from tms_ufrs_compliance import tms_ufrs_hesap_kontrol, tablo_tms_ufrs_analiz

# hesaplama_yontemi_kontrol fonksiyonu artık financial_analyzer.py'de
# Import edildi: from financial_analyzer import hesaplama_yontemi_kontrol

# ==========================================
# TCMB & TÜİK & BIST VERİ ÇEKME FONKSİYONLARI
# ==========================================
# Bu fonksiyonlar artık data_loader.py modülünde
# Import edildi: from data_loader import get_tcmb_doviz_kurlari, get_tuik_tufe_yillik, ...

# ==========================================
# TFRS ÇEVİRİ FONKSİYONLARI
# ==========================================
# TFRS_CEVIRI_SOZLUK ve cevir_finansal_tablo_turkce fonksiyonları artık translation.py modülünde
# Import edildi: from translation import TFRS_CEVIRI_SOZLUK, cevir_finansal_tablo_turkce

# ==========================================
# HIZLI ANALİZ MODÜLÜ FONKSİYONLARI (appHi entegrasyonu)
# ==========================================

# clean_turkish_float_hizli fonksiyonu artık utils.py'de
# Import edildi: from utils import clean_turkish_float_hizli

# get_standard_mapping_hizli fonksiyonu artık mapping.py modülünde
# Import edildi: from mapping import get_standard_mapping_hizli

# ==========================================
# 1. KONFİGÜRASYON & GİRİŞ SİSTEMİ
# ==========================================

st.set_page_config(page_title="digiCFO - Akıllı Finans", page_icon="🤓", layout="wide")

# ==========================================
# KOYU LACİVERT TEMA CSS ENJEKSİYONU
# ==========================================
try:
    from theme_css import DARK_NAVY_THEME_CSS
    st.markdown(DARK_NAVY_THEME_CSS, unsafe_allow_html=True)
except ImportError:
    # Fallback: Tema dosyası yoksa varsayılan görünüm
    pass

# ==========================================
# ÖZEL SELECTBOX RENK STİLLERİ - AÇIK MAVİ
# ==========================================
st.markdown("""
<style>
    /* Genel selectbox stilleri - Açık mavi için hazırlık */
    .selectbox-light-blue [data-baseweb="select"] > div {
        background-color: #e3f2fd !important;
        color: #1565c0 !important;
        border: 1px solid #90caf9 !important;
    }
    
    .selectbox-light-blue [data-baseweb="selectValue"] {
        color: #1565c0 !important;
    }
</style>
<script>
    function applyLightBlueToSelectboxes() {
        // Grup Seçiniz selectbox'ını bul ve açık mavi yap
        const labels = document.querySelectorAll('label, p');
        labels.forEach(function(label) {
            if (label.textContent && label.textContent.includes('Grup Seçiniz')) {
                let selectbox = label.closest('[data-testid="stSelectbox"]');
                if (!selectbox) {
                    // Label'ın yanındaki selectbox'ı bul
                    let parent = label.parentElement;
                    while (parent && !parent.querySelector('[data-baseweb="select"]')) {
                        parent = parent.parentElement;
                    }
                    if (parent) {
                        selectbox = parent.querySelector('[data-testid="stSelectbox"]') || parent;
                    }
                }
                if (selectbox) {
                    const selectDiv = selectbox.querySelector('[data-baseweb="select"] > div');
                    if (selectDiv) {
                        selectDiv.style.backgroundColor = '#e3f2fd';
                        selectDiv.style.color = '#1565c0';
                        selectDiv.style.border = '1px solid #90caf9';
                    }
                    const selectValue = selectbox.querySelector('[data-baseweb="selectValue"]');
                    if (selectValue) {
                        selectValue.style.color = '#1565c0';
                    }
                }
            }
            
            // BIST'ten Firma Seçin selectbox'ını bul ve açık mavi yap
            if (label.textContent && label.textContent.includes("BIST'ten Firma Seçin")) {
                let selectbox = label.closest('[data-testid="stSelectbox"]');
                if (!selectbox) {
                    let parent = label.parentElement;
                    while (parent && !parent.querySelector('[data-baseweb="select"]')) {
                        parent = parent.parentElement;
                    }
                    if (parent) {
                        selectbox = parent.querySelector('[data-testid="stSelectbox"]') || parent;
                    }
                }
                if (selectbox) {
                    const selectDiv = selectbox.querySelector('[data-baseweb="select"] > div');
                    if (selectDiv) {
                        selectDiv.style.backgroundColor = '#e3f2fd';
                        selectDiv.style.color = '#1565c0';
                        selectDiv.style.border = '1px solid #90caf9';
                    }
                    const selectValue = selectbox.querySelector('[data-baseweb="selectValue"]');
                    if (selectValue) {
                        selectValue.style.color = '#1565c0';
                    }
                }
            }
        });
    }
    
    // Sayfa yüklendiğinde ve her render'da çalıştır
    setTimeout(applyLightBlueToSelectboxes, 100);
    setTimeout(applyLightBlueToSelectboxes, 500);
    setTimeout(applyLightBlueToSelectboxes, 1000);
    
    // Streamlit'in rerun'larını dinle
    if (window.MutationObserver) {
        var observer = new MutationObserver(function(mutations) {
            applyLightBlueToSelectboxes();
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }
</script>
""", unsafe_allow_html=True)

# --- AUTHENTICATION (GİRİŞ) KONTROLÜ ---
# Kullanıcı türleri ve session state yönetimi artık auth.py'de
if AUTH_AVAILABLE:
    init_session_state()
    KULLANICI_TURLERI = KULLANICI_TURLERI  # Import edilen değişken
else:
    # Fallback: Eğer auth.py yoksa eski sistem
    KULLANICI_TURLERI = {
        "Bireysel Kullanıcı": {
            "tipler": ["Demo Kullanıcısı"],
            "icon": "👤",
            "renk": "#3498DB"
        },
        "Kurumsal Kullanıcı": {
            "tipler": ["Demo Kullanıcısı"],
            "icon": "🏢",
            "renk": "#9B59B6"
        }
    }
    if SESSION_MANAGER_AVAILABLE:
        init_session_state_defaults({
            'authenticated': False,
            'kullanici_turu': None,
            'kullanici_tipi': None,
            'kullanici_adi': None
        })
    else:
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'kullanici_turu' not in st.session_state:
            st.session_state['kullanici_turu'] = None
        if 'kullanici_tipi' not in st.session_state:
            st.session_state['kullanici_tipi'] = None
        if 'kullanici_adi' not in st.session_state:
            st.session_state['kullanici_adi'] = None

# --- UYGULAMA SESSION STATE BAŞLATMA ---
# Merkezi session state yönetimi
if SESSION_MANAGER_AVAILABLE:
    init_app_session_state()
else:
    # Fallback: Manuel session state başlatma
    if 'veri_onaylandi' not in st.session_state:
        st.session_state['veri_onaylandi'] = False
    if 'veri_onay_zamani' not in st.session_state:
        st.session_state['veri_onay_zamani'] = None
    if 'gelir_tablosu_onay' not in st.session_state:
        st.session_state['gelir_tablosu_onay'] = False
    if 'bilanco_onay' not in st.session_state:
        st.session_state['bilanco_onay'] = False
    if 'nakit_akis_onay' not in st.session_state:
        st.session_state['nakit_akis_onay'] = False
    if 'ekran_durumu' not in st.session_state:
        st.session_state['ekran_durumu'] = 'veri_merkezi'

# --- AUTHENTICATION KONTROLÜ ---
if not st.session_state.get('authenticated', False):
    # Login sayfasını göster (auth.py'den)
    if AUTH_AVAILABLE:
        show_login_page()
        st.stop()
    else:
        # Fallback: Eski login sistemi (auth.py yoksa)
        st.error("⚠️ auth.py modülü bulunamadı. Lütfen auth.py dosyasını kontrol edin.")
        st.stop()

# ==========================================
# GİRİŞ SONRASI - appHi.py ARAYÜZÜ
# ==========================================

# --- Sidebar Kullanıcı Bilgisi ---
# Logout butonu (auth.py'den) - Sadece menu ekranı DIŞINDA gösterilir
# Menu ekranında show_main_dashboard fonksiyonu sidebar'ı yönetir
if st.session_state.get('ekran_durumu') != 'menu':
    with st.sidebar:
        if AUTH_AVAILABLE:
            show_logout_button()
        else:
            # Fallback: Eski logout sistemi
            kullanici_adi = st.session_state.get('kullanici_adi', 'Kullanıcı')
            kullanici_turu_goster = st.session_state.get('kullanici_turu', '')
            kullanici_tipi_goster = st.session_state.get('kullanici_tipi', '')
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <p style="color: #00d4ff; margin: 0; font-size: 12px;">🟢 Aktif Oturum</p>
                <p style="color: white; margin: 5px 0; font-weight: bold;">{kullanici_adi}</p>
                <p style="color: #888; margin: 0; font-size: 11px;">{kullanici_tipi_goster}</p>
                <p style="color: #666; margin: 0; font-size: 10px;">{kullanici_turu_goster}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Çıkış Yap", use_container_width=True):
                st.session_state['authenticated'] = False
                st.session_state['kullanici_turu'] = None
                st.session_state['kullanici_tipi'] = None
                st.session_state['kullanici_adi'] = None
                st.rerun()
        

# ==========================================
# appHi.py - YARDIMCI FONKSİYONLAR
# ==========================================

# clean_turkish_float fonksiyonu artık utils.py'de
# Import edildi: from utils import clean_turkish_float

# ==========================================
# MAPPING ENTEGRASYON FONKSİYONLARI
# ==========================================
# apply_user_mapping_to_df, get_standard_mapping ve get_standard_mapping_hizli 
# fonksiyonları artık mapping.py modülünde
# Import edildi: from mapping import apply_user_mapping_to_df, get_standard_mapping, get_standard_mapping_hizli

# ==========================================
# appHi.py - ANA UYGULAMA AKIŞI
# ==========================================

import plotly.express as px

# Ekran durumu kontrolü
if 'ekran_durumu' not in st.session_state:
    st.session_state['ekran_durumu'] = 'veri_merkezi'  # veri_merkezi -> firma_bilgileri -> menu

# ==========================================
# EKRAN 1: FİNANSAL VERİ MERKEZİ
# ==========================================
if st.session_state['ekran_durumu'] == 'veri_merkezi':
    
    st.title("📊 Finansal Veri Merkezi & Analiz")
    st.markdown("---")

    # --- Sidebar Veri Yükleme ---
    st.sidebar.header("📁 Veri Yükleme")
    
    # Veri kaynağı seçimi
    data_source = st.sidebar.radio(
        "Veri Kaynağı Seçin:",
        ["📊 Veritabanından Seç", "📁 Manuel Dosya Yükle"],
        key="data_source_selector"
    )
    
    df = None
    data_loaded = False
    
    # ==========================================
    # VERİTABANI SEÇENEĞİ
    # ==========================================
    if data_source == "📊 Veritabanından Seç":
        if DB_AVAILABLE:
            try:
                from dal.demo_dal import get_companies, get_company_by_id
                from dal.data_loader_db import load_company_data_from_db, get_company_financial_summary
                
                companies = get_companies()
                
                if companies:
                    # Firma seçimi - Sadece firma adı göster (temizlenmiş)
                    # Firma adlarını temizle ve sadece adı göster
                    company_options = {}
                    for c in companies:
                        firma_adi = str(c['firma_adi']).strip() if c.get('firma_adi') else ''
                        # Sadece firma adını al (varsa ek bilgileri temizle)
                        if firma_adi:
                            company_options[firma_adi] = c['id']
                    
                    if company_options:
                        selected_company_name = st.sidebar.selectbox(
                            "Firma Seçin:",
                            options=list(company_options.keys()),
                            key="company_selector_db"
                        )
                    else:
                        st.sidebar.warning("⚠️ Veritabanında firma bulunamadı.")
                        selected_company_name = None
                    
                    if selected_company_name:
                        selected_company_id = company_options[selected_company_name]
                        
                        # Özet bilgileri göster
                        summary = get_company_financial_summary(selected_company_id)
                        if summary:
                            st.sidebar.info(f"""
                            **Firma Özeti:**
                            - 📊 {summary.get('account_count', 0)} Hesap
                            - 📅 {summary.get('period_count', 0)} Dönem
                            - 📝 {summary.get('total_records', 0)} Kayıt
                            - 🗓️ Son Dönem: {summary.get('latest_period', 'N/A')}
                            """)
                        
                        # Verileri yükle butonu
                        if st.sidebar.button("🔄 Verileri Yükle", type="primary", key="load_from_db_btn"):
                            with st.spinner("📊 Veritabanından veriler yükleniyor..."):
                                df = load_company_data_from_db(selected_company_id)
                                
                                if df is not None and not df.empty:
                                    # Firma bilgilerini session state'e kaydet
                                    company_info = get_company_by_id(selected_company_id)
                                    if company_info:
                                        st.session_state['firma_bilgi'] = {
                                            'Firma Adı': company_info['firma_adi'],
                                            'Borsa Kodu': company_info['borsa_kodu'],
                                            'Sektör': company_info['sektor']
                                        }
                                    
                                    # ==========================================
                                    # VERİ İŞLEME (Manuel yükleme ile aynı)
                                    # ==========================================
                                    # Orijinal veriyi kaydet
                                    st.session_state['df_orijinal_yuklenen'] = df.copy()
                                    
                                    # Veritabanından gelen veri: account_name, period1, period2, ...
                                    # Manuel yükleme formatına uyarla: Kalem -> account_name
                                    if 'account_name' in df.columns:
                                        df = df.rename(columns={'account_name': 'Kalem'})
                                    
                                    # Sayısal sütunları temizle
                                    numeric_cols = [col for col in df.columns if col != 'Kalem']
                                    item_col = 'Kalem' if 'Kalem' in df.columns else df.columns[0]
                                    
                                    # Sayısal sütunları temizle
                                    for col in numeric_cols:
                                        if col in df.columns:
                                            if not pd.api.types.is_numeric_dtype(df[col]):
                                                df[col] = df[col].apply(clean_turkish_float)
                                    
                                    # Standartlaştırma - Mapping entegrasyonu
                                    user_mapping = st.session_state.get('user_mapping', {})
                                    df = apply_user_mapping_to_df(df, item_col, user_mapping)
                                    
                                    # Session state'e kaydet
                                    st.session_state['df_ham'] = df.copy()
                                    st.session_state['data_source'] = 'database'
                                    st.session_state['selected_company_id'] = selected_company_id
                                    
                                    # ==========================================
                                    # FİNANSAL TABLOLARI OLUŞTUR (MENU İÇİN)
                                    # ==========================================
                                    # Tarih sütunlarını ve banka durumunu belirle
                                    st.session_state['date_cols'] = numeric_cols
                                    st.session_state['is_banka'] = False
                                    
                                    # Ham veriyi doğrudan kullan (manuel yükleme ile aynı)
                                    st.session_state['df_gelir_raw'] = df.copy()
                                    st.session_state['df_bilanco_raw'] = df.copy()
                                    st.session_state['df_nakit_raw'] = df.copy()
                                    
                                    # Alternatif anahtarlar (bazı modüller bunları kullanıyor)
                                    st.session_state['df_gelir_ham_veri'] = df.copy()
                                    st.session_state['df_bilanco_ham_veri'] = df.copy()
                                    st.session_state['df_nakit_ham_veri'] = df.copy()
                                    
                                    # Veri Merkezi için de kaydet
                                    st.session_state['df_veri_merkezi'] = df.copy()
                                    st.session_state['numeric_cols_vm'] = numeric_cols
                                    
                                    st.success(f"✅ {company_info['firma_adi']} verileri başarıyla yüklendi ve işlendi!")
                                    data_loaded = True
                                    st.rerun()
                                else:
                                    st.error("❌ Veritabanından veri yüklenemedi.")
                else:
                    st.sidebar.warning("⚠️ Veritabanında firma bulunamadı.")
            except Exception as e:
                st.sidebar.error(f"❌ Veritabanı hatası: {str(e)}")
        else:
            st.sidebar.warning("⚠️ Veritabanı bağlantısı yapılandırılmamış. Manuel dosya yükleme kullanın.")
        
        st.sidebar.markdown("---")
        
        # Veritabanı Yönetimi (Sidebar'ın en altında)
        try:
            from db_management import show_db_management_section
            show_db_management_section()
        except ImportError:
            pass
    
    # ==========================================
    # MANUEL DOSYA YÜKLEME SEÇENEĞİ
    # ==========================================
    elif data_source == "📁 Manuel Dosya Yükle":
        uploaded_file = st.sidebar.file_uploader("Excel veya CSV Dosyası Yükleyin", type=["xlsx", "xls", "csv"], key="manual_file_uploader")
        
        if uploaded_file is not None:
            try:
                # Dosyayı Oku
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # ==========================================
                # ORİJİNAL VERİYİ KAYDET (İşlenmeden önce!)
                # ==========================================
                # Orijinal veriyi session_state'e kaydet (Veri Kontrol için)
                st.session_state['df_orijinal_yuklenen'] = df.copy()
                st.session_state['df_ham'] = df.copy()
                st.session_state['data_source'] = 'manual'
                
                # Eğer session state'de company_id varsa temizle
                if 'selected_company_id' in st.session_state:
                    del st.session_state['selected_company_id']

                st.success("✅ Dosya başarıyla yüklendi!")
                data_loaded = True
                
                # Ham veriyi göster
                with st.expander("Ham Veriyi Görüntüle"):
                    st.dataframe(df.head())

                # --- Veri İşleme ---
                # Sayısal sütunları temizle
                numeric_cols = df.columns[1:] # İlk sütun hariç diğerleri
                item_col = df.columns[0]      # İlk sütun (Kalem Adı)

                for col in numeric_cols:
                    df[col] = df[col].apply(clean_turkish_float)

                # Standartlaştırma - Mapping entegrasyonu
                user_mapping = st.session_state.get('user_mapping', {})
                df = apply_user_mapping_to_df(df, item_col, user_mapping)
                
                # Session state'e kaydet
                st.session_state['df_ham'] = df.copy()
            except Exception as e:
                st.error(f"❌ Dosya okunurken hata: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
        
        st.sidebar.markdown("---")
        
        # Veritabanı Yönetimi (Sidebar'ın en altında)
        try:
            from db_management import show_db_management_section
            show_db_management_section()
        except ImportError:
            pass
    
    # ==========================================
    # VERİ İŞLEME VE GÖSTERİM (Her iki kaynak için)
    # ==========================================
    if 'df_ham' in st.session_state and st.session_state['df_ham'] is not None:
        df = st.session_state['df_ham'].copy()
        
        if not df.empty:
            # Veri işleme (eğer daha önce işlenmemişse)
            if 'Grup' not in df.columns or 'Standart_Kalem' not in df.columns:
                # Sayısal sütunları temizle
                numeric_cols = df.columns[1:] # İlk sütun hariç diğerleri
                item_col = df.columns[0]      # İlk sütun (Kalem Adı)

                for col in numeric_cols:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        continue  # Zaten sayısal
                    df[col] = df[col].apply(clean_turkish_float)

                # Standartlaştırma - Mapping entegrasyonu
                user_mapping = st.session_state.get('user_mapping', {})
                df = apply_user_mapping_to_df(df, item_col, user_mapping)
                
                # Session state'e kaydet
                st.session_state['df_ham'] = df.copy()
            else:
                # Zaten işlenmiş, sadece sütunları al
                numeric_cols = [col for col in df.columns if col not in ['Grup', 'Standart_Kalem', df.columns[0]]]
                item_col = df.columns[0]

            # --- Analiz Sekmeleri ---
            tab1, tab2 = st.tabs(["📋 Özet Tablo", "📈 Grafikler"])

            with tab1:
                st.subheader("Standartlaştırılmış Veri")
                # Gruplara göre filtreleme
                if 'Grup' in df.columns:
                    selected_group = st.selectbox("Grup Seçiniz:", ["Tümü"] + list(df['Grup'].unique()), key="grup_sec_finansal_veri_merkezi")
                else:
                    selected_group = "Tümü"
                
                if selected_group != "Tümü":
                    display_df = df[df['Grup'] == selected_group]
                else:
                    display_df = df
                
                st.dataframe(display_df, use_container_width=True)

            with tab2:
                st.subheader("Trend Analizi")
                
                if len(numeric_cols) > 0:
                    # 1. Grafikleri Oluştur ve 2'li Izgara (Grid) Halinde Göster
                    # Standart_Kalem yoksa account_name kullan
                    item_col_name = 'Standart_Kalem' if 'Standart_Kalem' in display_df.columns else display_df.columns[0]
                    unique_items = display_df[item_col_name].unique()
                    all_figures = [] # PDF çıktısı için grafikleri sakla

                    # Her 2 grafikte bir yeni satır
                    for i in range(0, len(unique_items), 2):
                        cols = st.columns(2)
                        
                        # --- Grafik 1 ---
                        item1 = unique_items[i]
                        row1 = display_df[display_df[item_col_name] == item1]
                        if not row1.empty:
                            df_melt1 = row1.melt(id_vars=[item_col_name], value_vars=numeric_cols, var_name='Dönem', value_name='Değer')
                            fig1 = px.bar(
                                df_melt1, 
                                x='Dönem', 
                                y='Değer', 
                                color='Standart_Kalem', 
                                title=item1
                            )
                            cols[0].plotly_chart(fig1, use_container_width=True)
                            all_figures.append(fig1)

                        # --- Grafik 2 (Varsa) ---
                        if i + 1 < len(unique_items):
                            item2 = unique_items[i+1]
                            row2 = display_df[display_df[item_col_name] == item2]
                            if not row2.empty:
                                df_melt2 = row2.melt(id_vars=[item_col_name], value_vars=numeric_cols, var_name='Dönem', value_name='Değer')
                                fig2 = px.bar(
                                    df_melt2, 
                                    x='Dönem', 
                                    y='Değer', 
                                    color='Standart_Kalem', 
                                    title=item2
                                )
                                cols[1].plotly_chart(fig2, use_container_width=True)
                                all_figures.append(fig2)

                    st.markdown("---")
                    
                    # 2. Rapor Çıktısı (PDF/HTML)
                    st.write("### 📥 Rapor Çıktısı")
                    st.info("Aşağıdaki butona tıklayarak grafikleri içeren raporu indirebilir, açılan sayfada **'Yazdır' (Ctrl+P)** diyerek **PDF olarak kaydedebilirsiniz.**")

                    # HTML İçeriği Hazırla
                    html_string = f"""
                    <html>
                    <head>
                        <title>Finansal Analiz Raporu - {selected_group}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 40px; }}
                            .chart-container {{ page-break-inside: avoid; margin-bottom: 50px; text-align: center; }}
                            h1 {{ text-align: center; color: #333; }}
                            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                            th {{ background-color: #f2f2f2; }}
                            @media print {{
                                .no-print {{ display: none; }}
                            }}
                        </style>
                    </head>
                    <body>
                        <h1>Finansal Analiz Raporu</h1>
                        <h3>Grup: {selected_group}</h3>
                        <p>Rapor Tarihi: {pd.Timestamp.now().strftime('%d-%m-%Y %H:%M')}</p>
                        <hr>
                        <h4>Veri Tablosu</h4>
                        {display_df.to_html(index=False)}
                        <hr>
                        <h4>Grafikler</h4>
                    """

                    # Grafikleri HTML'e ekle
                    for fig in all_figures:
                        fig_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
                        html_string += f"<div class='chart-container'>{fig_html}</div>"

                    html_string += """
                    </body>
                    </html>
                    """

                    st.download_button(
                        label="📄 Tüm Grafikleri Rapor Olarak İndir (PDF İçin)",
                        data=html_string,
                        file_name=f"Finansal_Rapor_{selected_group}.html",
                        mime="text/html"
                    )

                else:
                    st.warning("Grafik çizmek için yeterli sayısal sütun bulunamadı.")

            # Veriyi session_state'e kaydet
            st.session_state['df_veri_merkezi'] = df
            st.session_state['numeric_cols_vm'] = list(numeric_cols)
            st.session_state['df_ham'] = df.copy()
            
            # ==========================================
            # FİNANSAL TABLOLARI OLUŞTUR (MENU İÇİN)
            # ==========================================
            # Tarih sütunlarını ve banka durumunu belirle
            st.session_state['date_cols'] = list(numeric_cols)
            st.session_state['is_banka'] = False
            
            # Ham veriyi doğrudan kullan
            st.session_state['df_gelir_raw'] = df.copy()
            st.session_state['df_bilanco_raw'] = df.copy()
            st.session_state['df_nakit_raw'] = df.copy()
            
            # Alternatif anahtarlar (bazı modüller bunları kullanıyor)
            st.session_state['df_gelir_ham_veri'] = df.copy()
            st.session_state['df_bilanco_ham_veri'] = df.copy()
            st.session_state['df_nakit_ham_veri'] = df.copy()
            
            st.success("✅ Veriler başarıyla yüklendi!")
            
            # Sonraki Adım Butonu
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("➡️ Firma Sektör Bilgileri Tanımlama", type="primary", use_container_width=True):
                    st.session_state['ekran_durumu'] = 'firma_bilgileri'
                    st.rerun()
    else:
        st.info("Lütfen sol menüden bir dosya yükleyerek başlayın.")
    
    st.stop()  # Veri merkezi ekranını burada durdur

# ==========================================
# EKRAN 2: FİRMA BİLGİLERİ VE SEKTÖR SEÇİMİ
# ==========================================
elif st.session_state['ekran_durumu'] == 'firma_bilgileri':
    
    st.title("🏢 Firma Bilgileri & Sektör Seçimi")
    st.markdown("---")
    
    # Geri butonu sidebar'da
    with st.sidebar:
        if st.button("⬅️ Veri Merkezine Dön", use_container_width=True):
            st.session_state['ekran_durumu'] = 'veri_merkezi'
            st.rerun()
    
    st.info("👋 Analize başlamadan önce firma hakkında birkaç temel bilgi eklemek ister misiniz?")
    st.markdown("Bu bilgiler **Büyük Veri** tablosunu zenginleştirmek ve çalışan başına verimlilik analizleri için kullanılacaktır.")
    
    # BIST Sektör verilerini merkezi fonksiyondan al (cache'li - sadece 1 kez yüklenir)
    bist_data = yukle_bist_sektor_verileri()
    df_bist = bist_data["df_bist"]
    df_sektor_ort = bist_data["df_sektor_ort"]
    bist_kodlari = bist_data["bist_kodlari"]
    sektor_listesi = bist_data["sektor_listesi"]
    bist_verisi_var = bist_data["bist_verisi_var"]
    
    # Firma seçimi (form dışında - dinamik güncelleme için)
    st.markdown("### 🔍 Firma Seçimi")
    
    # BIST verisi yoksa uyarı göster
    if not bist_verisi_var:
        st.warning("⚠️ BIST sektör verileri bulunamadı. Otomatik firma seçimi için 'BistTumSektorHissesort.xlsx' dosyasını uygulama ile aynı klasöre kopyalayın.")
    
    col_sec1, col_sec2 = st.columns([1, 1])
    
    with col_sec1:
        secilen_kod = st.selectbox(
            "BIST'ten Firma Seçin (Borsa Kodu):",
            options=bist_kodlari,
            key="bist_firma_sec",
            help="Listeden bir firma seçerseniz bilgiler otomatik doldurulur",
            disabled=not bist_verisi_var
        )
    
    # Seçilen firmaya göre varsayılan değerleri belirle
    default_vals = {
        "ad": "", "sektor": "", "sermaye": 0.0, "hisse": 0, "halka_aciklik": 0.0,
        "fiyat": 0.0, "fk": 0.0, "fd_favok": 0.0, "fd_satis": 0.0, "pd_dd": 0.0,
        "piyasa_degeri": 0.0, "piyasa_degeri_usd": 0.0, "ozkaynaklar": 0.0, "dd_hisse": 0.0
    }
    sektor_ort_vals = {"fk": 0.0, "fd_favok": 0.0, "fd_satis": 0.0, "pd_dd": 0.0}
    
    if secilen_kod != "-- Manuel Giriş --" and df_bist is not None:
        firma_row = df_bist[df_bist['Borsa Kodu'] == secilen_kod]
        if not firma_row.empty:
            row = firma_row.iloc[0]
            default_vals["ad"] = str(row.get('Hisse Adı', ''))
            default_vals["sektor"] = str(row.get('Sektör', ''))
            # Sermaye mn TL olarak geliyor, 1.000.000 ile çarp (TL'ye çevir)
            default_vals["sermaye"] = float(row.get('Sermaye(mn TL)', 0) or 0) * 1000000
            default_vals["halka_aciklik"] = float(row.get('Halka AçıklıkOranı (%)', 0) or 0)
            default_vals["fiyat"] = float(row.get('Kapanış(TL)', 0) or 0)
            # Piyasa değeri mn TL olarak geliyor, 1.000.000 ile çarp (TL'ye çevir)
            default_vals["piyasa_degeri"] = float(row.get('Piyasa Değeri(mn TL)', 0) or 0) * 1000000
            # Piyasa değeri $ (mn $ olarak geliyor)
            default_vals["piyasa_degeri_usd"] = float(row.get('Piyasa Değeri(mn $)', 0) or 0) * 1000000
            # Hisse sayısını hesapla: Piyasa Değeri / Fiyat
            if default_vals["fiyat"] > 0:
                default_vals["hisse"] = int(default_vals["piyasa_degeri"] / default_vals["fiyat"])
            
            # F/K, FD/FAVÖK vb. değerleri al
            for key, col in [("fk", "F/K"), ("fd_favok", "FD/FAVÖK"), ("fd_satis", "FD/Satışlar"), ("pd_dd", "PD/DD")]:
                val = row.get(col, 0)
                if val != 'A/D' and pd.notna(val):
                    try:
                        default_vals[key] = float(val)
                    except:
                        default_vals[key] = 0.0
            
            # DD (Defter Değeri / Özkaynaklar) hesapla: DD = PD / (PD/DD)
            if default_vals["piyasa_degeri"] > 0 and default_vals["pd_dd"] > 0:
                default_vals["ozkaynaklar"] = default_vals["piyasa_degeri"] / default_vals["pd_dd"]
            else:
                default_vals["ozkaynaklar"] = 0.0
            
            # DD per share (Hisse başına defter değeri) = Özkaynaklar / Hisse Sayısı
            if default_vals["ozkaynaklar"] > 0 and default_vals["hisse"] > 0:
                default_vals["dd_hisse"] = default_vals["ozkaynaklar"] / default_vals["hisse"]
            else:
                default_vals["dd_hisse"] = 0.0
            
            # Sektör ortalamalarını al
            if df_sektor_ort is not None and default_vals["sektor"]:
                sektor_row = df_sektor_ort[df_sektor_ort['Sektör'] == default_vals["sektor"]]
                if not sektor_row.empty:
                    s_row = sektor_row.iloc[0]
                    sektor_ort_vals["fk"] = float(s_row.get('F/K', 0) or 0) if pd.notna(s_row.get('F/K', 0)) else 0.0
                    sektor_ort_vals["fd_favok"] = float(s_row.get('FD/FAVÖK', 0) or 0) if pd.notna(s_row.get('FD/FAVÖK', 0)) else 0.0
                    sektor_ort_vals["fd_satis"] = float(s_row.get('FD/Satışlar', 0) or 0) if pd.notna(s_row.get('FD/Satışlar', 0)) else 0.0
                    sektor_ort_vals["pd_dd"] = float(s_row.get('PD/DD', 0) or 0) if pd.notna(s_row.get('PD/DD', 0)) else 0.0
    
    with col_sec2:
        if secilen_kod != "-- Manuel Giriş --":
            st.success(f"✅ Seçilen: **{default_vals['ad']}** ({secilen_kod})")
            st.caption(f"Sektör: {default_vals['sektor']}")
        else:
            # Manuel giriş için sektör seçimi (HALKA AÇIK OLMAYAN ŞİRKETLER İÇİN)
            st.info("📝 **Halka Açık Olmayan Şirket** - Tüm bilgileri manuel girebilir ve karşılaştırma için sektör seçebilirsiniz.")
            if sektor_listesi:
                secilen_sektor_manuel = st.selectbox(
                    "🏭 Sektör Seçin (Mukayese için):",
                    options=["-- Sektör Seçiniz --"] + sektor_listesi,
                    key="manuel_sektor_sec",
                    help="Sektör seçtiğinizde o sektörün ortalama çarpanları görünecek"
                )
                if secilen_sektor_manuel != "-- Sektör Seçiniz --" and df_sektor_ort is not None:
                    default_vals["sektor"] = secilen_sektor_manuel
                    sektor_row = df_sektor_ort[df_sektor_ort['Sektör'] == secilen_sektor_manuel]
                    if not sektor_row.empty:
                        s_row = sektor_row.iloc[0]
                        sektor_ort_vals["fk"] = float(s_row.get('F/K', 0) or 0) if pd.notna(s_row.get('F/K', 0)) else 0.0
                        sektor_ort_vals["fd_favok"] = float(s_row.get('FD/FAVÖK', 0) or 0) if pd.notna(s_row.get('FD/FAVÖK', 0)) else 0.0
                        sektor_ort_vals["fd_satis"] = float(s_row.get('FD/Satışlar', 0) or 0) if pd.notna(s_row.get('FD/Satışlar', 0)) else 0.0
                        sektor_ort_vals["pd_dd"] = float(s_row.get('PD/DD', 0) or 0) if pd.notna(s_row.get('PD/DD', 0)) else 0.0
                        st.success(f"✅ Sektör seçildi: **{secilen_sektor_manuel}**")
            else:
                st.warning("⚠️ Sektör listesi yüklenemedi. Excel dosyasının aynı klasörde olduğundan emin olun.")
    
    # Sektör Ortalamaları Bilgi Kutusu
    if any(v > 0 for v in sektor_ort_vals.values()):
        st.markdown("---")
        st.markdown(f"### 📊 Sektör Ortalamaları ({default_vals['sektor']})")
        col_ort1, col_ort2, col_ort3, col_ort4 = st.columns(4)
        with col_ort1:
            st.metric("Sektör Ort. F/K", f"{sektor_ort_vals['fk']:.2f}" if sektor_ort_vals['fk'] > 0 else "-")
        with col_ort2:
            st.metric("Sektör Ort. FD/FAVÖK", f"{sektor_ort_vals['fd_favok']:.2f}" if sektor_ort_vals['fd_favok'] > 0 else "-")
        with col_ort3:
            st.metric("Sektör Ort. FD/Satışlar", f"{sektor_ort_vals['fd_satis']:.2f}" if sektor_ort_vals['fd_satis'] > 0 else "-")
        with col_ort4:
            st.metric("Sektör Ort. PD/DD", f"{sektor_ort_vals['pd_dd']:.2f}" if sektor_ort_vals['pd_dd'] > 0 else "-")
        
        # Sektördeki Tüm BIST Firmalarının Listesi
        if df_bist is not None and default_vals['sektor']:
            with st.expander(f"📋 {default_vals['sektor']} Sektöründeki BIST Firmaları", expanded=False):
                # Seçilen sektördeki firmaları filtrele
                df_sektor_firmalar = df_bist[df_bist['Sektör'] == default_vals['sektor']].copy()
                
                if not df_sektor_firmalar.empty:
                    # Gösterilecek sütunları seç
                    gosterilecek_sutunlar = ['Borsa Kodu', 'Hisse Adı', 'Kapanış(TL)', 'Piyasa Değeri(mn TL)', 'F/K', 'FD/FAVÖK', 'FD/Satışlar', 'PD/DD']
                    mevcut_sutunlar = [col for col in gosterilecek_sutunlar if col in df_sektor_firmalar.columns]
                    
                    df_sektor_goster = df_sektor_firmalar[mevcut_sutunlar].copy()
                    
                    # Sayısal sütunları dönüştür (A/D değerlerini - olarak göster)
                    for col in ['F/K', 'FD/FAVÖK', 'FD/Satışlar', 'PD/DD']:
                        if col in df_sektor_goster.columns:
                            df_sektor_goster[col] = df_sektor_goster[col].replace('A/D', '-').astype(str)
                    
                    # Tüm sütunları Arrow uyumlu yap
                    for col in df_sektor_goster.columns:
                        df_sektor_goster[col] = df_sektor_goster[col].fillna('-').astype(str)
                    
                    st.markdown(f"**Toplam {len(df_sektor_goster)} firma** bu sektörde BIST'te işlem görmektedir.")
                    
                    # Tablo gösterimi
                    st.dataframe(
                        df_sektor_goster,
                        use_container_width=True,
                        height=min(400, len(df_sektor_goster) * 35 + 40)
                    )
                else:
                    st.warning("Bu sektörde BIST'te işlem gören firma bulunamadı.")
    
    st.markdown("---")
    
    with st.form("firma_bilgi_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            # Temel Firma Bilgileri
            st.markdown("### 🏢 Temel Firma Bilgileri")
            f_ad = st.text_input("Firma Adı", value=default_vals["ad"], placeholder="Örn: ABC A.Ş.")
            f_sektor = st.text_input("Sektör", value=default_vals["sektor"], disabled=True if secilen_kod != "-- Manuel Giriş --" else False)
            f_od_sermaye = st.number_input("Ödenmiş Sermaye (TL)", min_value=0.0, step=1000000.0, value=default_vals["sermaye"], format="%.0f")
            f_hisse_sayisi = st.number_input("Pay / Hisse Sayısı (Tüm)", min_value=0, step=1000000, value=default_vals["hisse"])
            f_halka_aciklik = st.number_input("Halka Açıklık Oranı (%)", min_value=0.0, max_value=100.0, step=0.1, value=default_vals["halka_aciklik"])
            f_calisan = st.number_input("Çalışan Sayısı", min_value=0, step=1)
            f_endeksler = st.text_input("Bulunduğu Endeksler", placeholder="BIST 100, BIST Sınai vb.")

        with c2:
            # Piyasa Verileri
            st.markdown("### 📈 Piyasa Verileri")
            f_islem_tarihi = st.date_input("İşlem Tarihi")
            f_borsa_fiyat = st.number_input("Borsa Fiyatı (TL)", min_value=0.0, step=0.01, value=default_vals["fiyat"])
            f_piyasa_degeri = st.number_input("Piyasa Değeri (TL)", min_value=0.0, step=1000000.0, value=default_vals["piyasa_degeri"], format="%.0f")
            st.markdown("---")
            st.markdown("#### 💱 Döviz Kurları (TCMB Alış)")
            
            # TCMB'den otomatik kur çek
            tcmb_kurlar = get_tcmb_doviz_kurlari()
            default_usd = tcmb_kurlar["USD"] if tcmb_kurlar["USD"] else 0.0
            default_eur = tcmb_kurlar["EUR"] if tcmb_kurlar["EUR"] else 0.0
            
            if tcmb_kurlar["tarih"]:
                st.caption(f"📅 TCMB Kur Tarihi: {tcmb_kurlar['tarih']}")
            
            f_usd_kur = st.number_input("Dolar (USD)", min_value=0.0, step=0.0001, format="%.4f", value=default_usd)
            f_eur_kur = st.number_input("Euro (EUR)", min_value=0.0, step=0.0001, format="%.4f", value=default_eur)
            
            st.markdown("---")
            st.markdown("#### 📈 TÜFE Oranı (Yıllık %)")
            
            # TÜİK'ten otomatik TÜFE çek
            tufe_data = get_tuik_tufe_yillik()
            default_tufe = tufe_data["tufe_yillik"] if tufe_data["tufe_yillik"] else 0.0
            
            if tufe_data["donem"]:
                st.caption(f"📅 TÜFE Dönemi: {tufe_data['donem']}")
            
            f_tufe_yillik = st.number_input("Yıllık TÜFE (%)", min_value=0.0, step=0.1, format="%.2f", value=default_tufe)

        with c3:
            # Ekonomik Göstergeler
            st.markdown("### 📊 Firma Çarpanları")
            f_fk = st.number_input("F/K (Fiyat/Kazanç)", min_value=0.0, step=0.1, value=default_vals["fk"])
            f_fd_favok = st.number_input("FD/FAVÖK", min_value=0.0, step=0.1, value=default_vals["fd_favok"])
            f_fd_satis = st.number_input("FD/Satışlar", min_value=0.0, step=0.1, value=default_vals["fd_satis"])
            f_pd_dd = st.number_input("PD/DD", min_value=0.0, step=0.1, value=default_vals["pd_dd"])
            
            st.markdown("---")
            st.markdown("#### Faiz Oranları (Yıllık %)")
            f_politika_faiz = st.number_input("Politika Faizi (TCMB)", min_value=0.0, step=0.25)
            f_mevduat_faiz = st.number_input("1 Yıllık Mevduat Faizi", min_value=0.0, step=0.01)

        
        col_submit, col_skip = st.columns([1,1])
        with col_submit:
            submit_btn = st.form_submit_button("✅ Verileri Kaydet ve Devam Et", type="primary")
        with col_skip:
            skip_btn = st.form_submit_button("⏩ Veri Girmeden Devam Et")
        
        if submit_btn:
            st.session_state['firma_bilgi'] = {
                "Firma Adı": f_ad,
                "Borsa Kodu": secilen_kod if secilen_kod != "-- Manuel Giriş --" else "",
                "Sektör": f_sektor if f_sektor else default_vals["sektor"],
                "Tarih": datetime.now().strftime('%Y-%m-%d'),
                "Ödenmiş Sermaye": f_od_sermaye,
                "İşlem Tarihi": str(f_islem_tarihi),
                "Pay / Hisse Sayısı tüm": f_hisse_sayisi,
                "Halka Açıklık Oranı": f_halka_aciklik,
                "Çalışan Sayısı": f_calisan,
                "Bulundugu Endeksler": f_endeksler,
                "Borsa Fiyatı (Önceki iş gunu günü kapanış)": f_borsa_fiyat,
                "Piyasa Değeri (TL)": f_piyasa_degeri,
                "Piyasa Değeri ($)": default_vals.get("piyasa_degeri_usd", 0),
                "Özkaynaklar (DD)": default_vals.get("ozkaynaklar", 0),
                "DD Hisse Başına": default_vals.get("dd_hisse", 0),
                "TCMB Dolar Döviz Alış Kuru": f_usd_kur,
                "TCMB Euru Döviz Alış Kuru": f_eur_kur,
                "Yıllık TÜFE (%)": f_tufe_yillik,
                "F/K": f_fk,
                "FD/FAVÖK": f_fd_favok,
                "FD/Satışlar": f_fd_satis,
                "PD/DD": f_pd_dd,
                "Politika Faizi (TCMB Haftalık Repo)": f_politika_faiz,
                "1 Yıllık Mevduat Faizi": f_mevduat_faiz,
                # Sektör Ortalamaları (karşılaştırma için)
                "Sektör Ort. F/K": sektor_ort_vals["fk"],
                "Sektör Ort. FD/FAVÖK": sektor_ort_vals["fd_favok"],
                "Sektör Ort. FD/Satışlar": sektor_ort_vals["fd_satis"],
                "Sektör Ort. PD/DD": sektor_ort_vals["pd_dd"]
            }
            st.session_state['form_submitted'] = True
            st.session_state['firma_onaylandi'] = True
            
            # Veri Merkezi'nden gelen verileri kontrol et ve finansal tabloları oluştur
            if 'df_veri_merkezi' in st.session_state and not st.session_state['df_veri_merkezi'].empty:
                df_vm = st.session_state['df_veri_merkezi'].copy()
                st.session_state['df_ham'] = df_vm
                
                # Finansal tabloları oluştur (ham veriyi kullan)
                if 'df_gelir_raw' not in st.session_state or st.session_state.get('df_gelir_raw', pd.DataFrame()).empty:
                    st.session_state['date_cols'] = list(df_vm.select_dtypes(include=[np.number]).columns)
                    st.session_state['is_banka'] = False
                    st.session_state['df_gelir_raw'] = df_vm.copy()
                    st.session_state['df_bilanco_raw'] = df_vm.copy()
                    st.session_state['df_nakit_raw'] = df_vm.copy()
            
            st.session_state['ekran_durumu'] = 'menu'
            st.rerun()
        
        if skip_btn:
            st.session_state['firma_bilgi'] = {}
            st.session_state['form_submitted'] = True
            st.session_state['firma_onaylandi'] = True
            
            # Veri Merkezi'nden gelen verileri kontrol et ve finansal tabloları oluştur
            if 'df_veri_merkezi' in st.session_state and not st.session_state['df_veri_merkezi'].empty:
                df_vm = st.session_state['df_veri_merkezi'].copy()
                st.session_state['df_ham'] = df_vm
                
                # Finansal tabloları oluştur (ham veriyi kullan)
                if 'df_gelir_raw' not in st.session_state or st.session_state.get('df_gelir_raw', pd.DataFrame()).empty:
                    st.session_state['date_cols'] = list(df_vm.select_dtypes(include=[np.number]).columns)
                    st.session_state['is_banka'] = False
                    st.session_state['df_gelir_raw'] = df_vm.copy()
                    st.session_state['df_bilanco_raw'] = df_vm.copy()
                    st.session_state['df_nakit_raw'] = df_vm.copy()
            
            st.session_state['ekran_durumu'] = 'menu'
            st.rerun()
    
    st.stop()

# ==========================================
# EKRAN 3: ANA MENÜ (ESKİ SİSTEM İLE ENTEGRE)
# ==========================================
elif st.session_state['ekran_durumu'] == 'menu':
    try:
        # Sidebar'da firma bilgisi özeti ve kontroller
        with st.sidebar:
            firma_bilgi = st.session_state.get('firma_bilgi', {})
            if firma_bilgi:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <p style="color: #00d4ff; margin: 0; font-size: 12px;">🏢 Firma</p>
                    <p style="color: white; margin: 5px 0; font-weight: bold;">{firma_bilgi.get('Firma Adı', 'Belirtilmedi')}</p>
                    <p style="color: #888; margin: 0; font-size: 11px;">📍 {firma_bilgi.get('Sektör', '')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("⬅️ Firma Bilgilerine Dön", use_container_width=True):
                st.session_state['ekran_durumu'] = 'firma_bilgileri'
                st.rerun()
            
            st.markdown("---")
            
        # Rakam ölçeği seçimi artık dashboard.py'de sidebar'da gösteriliyor
        # scale_option dashboard.py'de session state'e kaydediliyor
        
        # Veri kontrolü ve hazırlık
        veri_yuklu = 'df_gelir_raw' in st.session_state and not st.session_state.get('df_gelir_raw', pd.DataFrame()).empty
        
        if not veri_yuklu:
            st.warning("⚠️ Henüz finansal veri yüklenmemiş. Bazı sekmeler boş görünecektir.")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📂 Veri Merkezine Git", type="primary"):
                    st.session_state['ekran_durumu'] = 'veri_merkezi'
                    st.rerun()
            with col_btn2:
                if st.button("↻ Sayfayı Yenile"):
                    st.rerun()
        
        # Verileri al
        date_cols = st.session_state.get('date_cols', [])
        is_banka = st.session_state.get('is_banka', False)
        df_gelir_raw = st.session_state.get('df_gelir_raw', pd.DataFrame())
        df_bilanco_raw = st.session_state.get('df_bilanco_raw', pd.DataFrame())
        df_nakit_raw = st.session_state.get('df_nakit_raw', pd.DataFrame())
        firma_bilgi = st.session_state.get('firma_bilgi', {})
        
        # Ölçek ayarı - dashboard.py'de sidebar'da seçilen değer
        scale = st.session_state.get('scale', 1)  # Varsayılan: TL (Tam)

        df_gelir_view = scale_df(df_gelir_raw, scale, date_cols)
        df_bilanco_view = scale_df(df_bilanco_raw, scale, date_cols)
        df_nakit_view = scale_df(df_nakit_raw, scale, date_cols)
        
        df_full_raw = pd.concat([df_gelir_raw, df_bilanco_raw, df_nakit_raw], ignore_index=True)
        dates_asc = date_cols

        def get_asc(k, use_scale=True): 
            df_source = scale_df(df_full_raw, scale, date_cols) if use_scale else df_full_raw
            row = df_source[df_source['Kalem'] == k]
            vals = row[date_cols].values[0] if not row.empty else [0]*len(date_cols)
            return [v if pd.notnull(v) else 0 for v in vals]
        
        # ==========================================
        # UPLOADED_FILE DEĞİŞKENİ - ESKİ SİSTEM UYUMLULUĞU
        # ==========================================
        # Eski sistemden gelen kodlar uploaded_file kullanıyor
        # Yeni sistemde df_veri_merkezi kullanılıyor
        uploaded_file = st.session_state.get('uploaded_file_obj', None)
        
        # ==========================================
        # SIDEBAR MENÜ SİSTEMİ - VIEW MODÜLÜ KULLANIMI
        # ==========================================
        # show_main_dashboard fonksiyonu sidebar menüyü oluşturur ve seçilen menüyü döndürür
        selected_menu, tab_names_aktif, tab_names_kapali, tab_names_ileri_analiz, tab_names_stratejik_analiz, tab_names_urunler, tab_names_coaching, tab_names_ai_analiz, tab_names_model_robotlar = show_main_dashboard(is_banka=is_banka)
        
        # ==========================================
        # SEÇİLEN MENÜYE GÖRE İÇERİK GÖSTERİMİ
        # ==========================================
        
        # ANA BÖLÜM SEKMELERİ
        if selected_menu == "📄 Ham Veri":
            show_ham_veri_section()
        
        elif selected_menu == "💼 Finansal Analiz Pro":
            show_finansal_analiz_pro_section()
        
        elif selected_menu == "📊 Sektör":
            show_sektor_section()
        
        elif selected_menu == "✅ Veri Kontrol":
            show_veri_kontrol_section()
        
        elif selected_menu == "📊 Gelir Tablosu":
            show_gelir_tablosu_section()
        
        elif selected_menu == "📊 Bilanço":
            show_bilanco_section()
        
        elif selected_menu == "💰 Nakit Akış Tablosu":
            show_nakit_akis_section()
        
        elif selected_menu == "🗃️ Büyük Veri":
            show_buyuk_veri_section()
        
        elif selected_menu == "📊 Rasyo/Oran":
            show_rasyo_oran_section()
        
        elif selected_menu == "📥 Rapor":
            show_reports_section()
        
        elif selected_menu == "✅ Veri Onayı":
            show_veri_onay_section()
        
        elif selected_menu == "🚀 İleri Finansal Analiz":
            show_ileri_analiz_section()
        
        elif selected_menu == "🎯 Stratejik Analiz":
            try:
                from views.stratejik_analiz_menu import show_stratejik_analiz_menu_section
                show_stratejik_analiz_menu_section()
            except ImportError:
                st.info("📋 Stratejik Analiz modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Stratejik Analiz yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "🤖 AI CEO/CFO Coaching":
            try:
                from views.ceo_cfo_coaching import show_ceo_cfo_coaching_section
                show_ceo_cfo_coaching_section()
            except ImportError:
                st.info("📋 AI CEO/CFO Coaching modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ AI CEO/CFO Coaching yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "🤖 AI Analiz ve Rapor":
            try:
                from views.ai_raporlar import show_ai_analiz_rapor_menu_section
                show_ai_analiz_rapor_menu_section()
            except ImportError:
                st.info("📋 AI Analiz ve Rapor modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ AI Analiz ve Rapor yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "🤖 AI Model Danışman Robotlar":
            try:
                from views.ai_model_robotlar import show_ai_model_robotlar_menu_section
                show_ai_model_robotlar_menu_section()
            except ImportError:
                st.info("📋 AI Model Danışman Robotlar modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ AI Model Danışman Robotlar yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "🤖 AI CFO Danışman Robotlar":
            # Alt menü seçimi yapılmamışsa varsayılan olarak ilk alt menüyü göster
            default_submenu = st.session_state.get('selected_ai_cfo_submenu', '1. Stratejik AI CFO')
            try:
                from views.ai_cfo_robots import show_ai_cfo_section
                show_ai_cfo_section(default_submenu)
            except ImportError as e:
                st.error(f"❌ AI CFO Robotlar modülü yüklenemedi: {str(e)}")
                import traceback
                with st.expander("🔍 Hata Detayları"):
                    st.code(traceback.format_exc())
            except Exception as e:
                st.error(f"❌ AI CFO Robotlar yüklenirken hata oluştu: {str(e)}")
                import traceback
                with st.expander("🔍 Hata Detayları"):
                    st.code(traceback.format_exc())
        
        elif selected_menu == "1. Stratejik AI CFO":
            try:
                from views.ai_cfo_robots import show_ai_cfo_section
                show_ai_cfo_section("1. Stratejik AI CFO")
            except ImportError as e:
                st.error(f"❌ AI CFO Robotlar modülü yüklenemedi: {str(e)}")
                import traceback
                with st.expander("🔍 Hata Detayları"):
                    st.code(traceback.format_exc())
            except Exception as e:
                st.error(f"❌ AI CFO Robotlar yüklenirken hata oluştu: {str(e)}")
                import traceback
                with st.expander("🔍 Hata Detayları"):
                    st.code(traceback.format_exc())
        
        elif selected_menu == "2. Teknik ve Operasyonel AI CFO":
            try:
                from views.ai_cfo_robots import show_ai_cfo_section
                show_ai_cfo_section("2. Teknik ve Operasyonel AI CFO")
            except ImportError as e:
                st.error(f"❌ AI CFO Robotlar modülü yüklenemedi: {str(e)}")
                import traceback
                with st.expander("🔍 Hata Detayları"):
                    st.code(traceback.format_exc())
            except Exception as e:
                st.error(f"❌ AI CFO Robotlar yüklenirken hata oluştu: {str(e)}")
                import traceback
                with st.expander("🔍 Hata Detayları"):
                    st.code(traceback.format_exc())
        
        elif selected_menu == "Dashboard Grafik":
            try:
                from views.dashboard_grafik import show_dashboard_grafik_section
                show_dashboard_grafik_section()
            except ImportError:
                st.info("📋 Dashboard Grafik modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Dashboard Grafik yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Sankey":
            try:
                from views.sankey_grafik import show_sankey_grafik_section
                show_sankey_grafik_section()
            except ImportError:
                st.info("📋 Sankey Grafik modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Sankey Grafik yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Rasyo":
            try:
                from views.rasyo_analiz import show_rasyo_analiz_section
                show_rasyo_analiz_section()
            except ImportError:
                st.info("📋 Rasyo Analiz modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Rasyo Analiz yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Yatırımcı":
            try:
                from views.yatirimci_analiz import show_yatirimci_analiz_section
                show_yatirimci_analiz_section()
            except ImportError:
                st.info("📋 Yatırımcı Analiz modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Yatırımcı Analiz yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Dikey":
            try:
                from views.dikey_analiz import show_dikey_analiz_section
                show_dikey_analiz_section()
            except ImportError:
                st.info("📋 Dikey Analiz modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Dikey Analiz yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "DuPont":
            try:
                from views.dupont_analiz import show_dupont_analiz_section
                show_dupont_analiz_section()
            except ImportError:
                st.info("📋 DuPont Analizi modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ DuPont Analizi yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Senaryo":
            try:
                from views.senaryo_analiz import show_senaryo_analiz_section
                show_senaryo_analiz_section()
            except ImportError:
                st.info("📋 Senaryo Analizi modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Senaryo Analizi yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Sektör Bilgi":
            try:
                from views.sektor_bilgi import show_sektor_bilgi_section
                show_sektor_bilgi_section()
            except ImportError:
                st.info("📋 Sektör Bilgi modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Sektör Bilgi yüklenirken hata oluştu: {str(e)}")
        
        elif selected_menu == "Borsa":
            try:
                from views.borsa_analiz import show_borsa_analiz_section
                show_borsa_analiz_section()
            except ImportError:
                st.info("📋 Borsa Analizi modülü yüklenemedi.")
            except Exception as e:
                st.error(f"❌ Borsa Analizi yüklenirken hata oluştu: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ **Beklenmeyen Bir Hata Oluştu**\n\n"
                f"Hata Detayı: `{str(e)}`\n\n"
                f"💡 **Çözüm Önerileri:**\n"
                f"- Sayfayı yenileyin (F5 veya ↻ butonu)\n"
                f"- Verilerin doğru formatta olduğundan emin olun\n"
                f"- Hata devam ederse, lütfen sistem yöneticinize başvurun")
        import traceback
        with st.expander("🔍 Teknik Detaylar (Geliştiriciler İçin)", expanded=False):
            st.code(traceback.format_exc())

# ==========================================
# ŞEMALAR VE DÖNÜŞTÜRÜCÜ SINIFLAR
# ==========================================
# SEMA_GELIR_TABLOSU, SEMA_BILANCO, SEMA_NAKIT_AKIS şemaları ve
# GelirTablosuConverter, BilancoConverter sınıfları artık converters.py modülünde
# Import edildi: from converters import SEMA_GELIR_TABLOSU, SEMA_BILANCO, SEMA_NAKIT_AKIS, GelirTablosuConverter, BilancoConverter
# HESAPLAMA_YONTEMLERI artık financial_analyzer.py'de
# Import edildi: from financial_analyzer import HESAPLAMA_YONTEMLERI

# --- BANKA ŞEMALARI ---
SEMA_BANKA_GELIR = {
    "Faiz Gelirleri": ["faiz gelirleri", "interest income", "kredilerden alınan faizler"],
    "Faiz Giderleri (-)": ["faiz giderleri", "interest expenses", "mevduata verilen faizler"],
    "Net Faiz Geliri": ["net faiz geliri", "net interest income", "net faiz gelir/gideri"],
    "Net Ücret ve Komisyon": ["net ücret ve komisyon", "net fee and commission", "ücret ve komisyon gelirleri"],
    "Ticari Kar/Zarar": ["ticari kar", "ticari zarar", "ticari kar/zarar (net)", "sermaye piyasası işlemleri karı"],
    "Diğer Faaliyet Gelirleri": ["diğer faaliyet gelirleri", "other operating income"],
    "Faaliyet Giderleri (-)": ["faaliyet giderleri", "personel giderleri", "genel yönetim giderleri", "diğer faaliyet giderleri"],
    "Kredi Karşılık Giderleri (-)": ["kredi karşılık", "beklenen kredi zarar", "provision for loan losses", "karşılık giderleri"],
    "Vergi Öncesi Kar": ["vergi öncesi kar", "profit before tax", "sürdürülen faaliyetler vergi öncesi"],
    "Vergi (-)": ["vergi", "tax", "vergi karşılığı"],
    "Net Kar/Zarar": ["net dönem karı", "net kar/zarar", "net income", "dönem net karı", "dönem karı"]
}

SEMA_BANKA_BILANCO = {
    "Nakit Değerler ve MB": ["nakit değerler", "merkez bankası", "kasa", "cash and central bank"],
    "Gerçeğe Uygun Değer Farkı FV": ["gerçeğe uygun değer", "finansal varlıklar", "alım satım amaçlı"],
    "Bankalar": ["bankalar", "banks"],
    "Krediler (Net)": ["krediler", "loans", "canlı krediler", "takipteki krediler"],
    "Menkul Değerler": ["menkul değerler", "yatırım amaçlı menkul kıymetler", "gerçeğe uygun değeri kar/zarara"],
    "Maddi Duran Varlıklar": ["maddi duran varlıklar", "sabit kıymetler", "demirbaşlar"],
    "Toplam Varlıklar": ["toplam varlıklar", "toplam aktifler", "aktif toplamı", "total assets"],
    
    "Mevduat": ["mevduat", "deposits", "toplam mevduat", "müşteri mevduatı"],
    "Alınan Krediler": ["alınan krediler", "funds borrowed", "kredi kuruluşlarına borçlar"],
    "İhraç Edilen Menkul Kıymetler": ["ihraç edilen menkul", "issued securities"],
    "Muhtelif Borçlar": ["muhtelif borçlar", "other liabilities"],
    "Toplam Yükümlülükler": ["toplam yükümlülükler", "toplam borçlar", "toplam pasifler"],
    
    "Ödenmiş Sermaye": ["ödenmiş sermaye", "sermaye", "share capital"],
    "Yedekler": ["yedekler", "kar yedekleri", "yasal yedekler"],
    "Geçmiş Yıl Karları": ["geçmiş yıl kar", "retained earnings"],
    "Dönem Net Karı": ["dönem net karı", "net profit for the period"],
    "Özkaynaklar": ["özkaynaklar", "toplam özkaynaklar", "shareholders equity"]
}

# ==========================================
# TMS / UFRS (IFRS) UYUMLULUK SİSTEMİ
# ==========================================
# TMS: Türkiye Muhasebe Standartları
# UFRS: Uluslararası Finansal Raporlama Standartları (IFRS)
# Her hesap için TMS adı, UFRS/IFRS adı ve ilgili standart numarası

TMS_UFRS_ESLESTIRME = {
    # ==========================================
    # GELİR TABLOSU HESAPLARI
    # ==========================================
    "gelir_tablosu": {
        "Satış Gelirleri": {
            "tms_adi": "Hasılat",
            "ufrs_adi": "Revenue",
            "tms_standart": "TMS 18 / TFRS 15",
            "ufrs_standart": "IAS 18 / IFRS 15",
            "aciklama": "Hasılatın muhasebeleştirilmesi (Müşteri Sözleşmelerinden Hasılat)",
            "hesaplama": "Brüt satışlar - Satış iadeleri - Satış iskontoları",
            "alternatif_isimler": ["satış gelirleri", "hasılat", "net satışlar", "revenue", "sales", "net sales", "turnover"]
        },
        "Satışların Maliyeti (-)": {
            "tms_adi": "Satışların Maliyeti",
            "ufrs_adi": "Cost of Sales / Cost of Goods Sold",
            "tms_standart": "TMS 2",
            "ufrs_standart": "IAS 2",
            "aciklama": "Stoklar standardına göre maliyet hesaplama",
            "hesaplama": "Dönem başı stok + Dönem içi alımlar - Dönem sonu stok",
            "alternatif_isimler": ["satışların maliyeti", "satış maliyeti", "cogs", "cost of goods sold", "cost of sales"]
        },
        "Brüt Kar/Zarar": {
            "tms_adi": "Brüt Kar/Zarar",
            "ufrs_adi": "Gross Profit/Loss",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Finansal Tabloların Sunuluşu",
            "hesaplama": "Hasılat - Satışların Maliyeti",
            "alternatif_isimler": ["brüt kar", "brüt kar/zarar", "brüt satış karı", "gross profit", "gross margin"]
        },
        "Faaliyet Giderleri (-)": {
            "tms_adi": "Faaliyet Giderleri",
            "ufrs_adi": "Operating Expenses",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Genel Yönetim + Pazarlama Satış + Ar-Ge Giderleri",
            "hesaplama": "Genel Yönetim Giderleri + Pazarlama Satış Dağıtım Giderleri + Ar-Ge Giderleri",
            "alternatif_isimler": ["faaliyet giderleri", "operating expenses", "opex", "işletme giderleri"]
        },
        "Faaliyet Karı/Zararı": {
            "tms_adi": "Esas Faaliyet Karı/Zararı",
            "ufrs_adi": "Operating Profit/Loss",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Esas faaliyetlerden elde edilen kar veya zarar",
            "hesaplama": "Brüt Kar - Faaliyet Giderleri + Esas Faaliyetlerden Diğer Gelirler - Esas Faaliyetlerden Diğer Giderler",
            "alternatif_isimler": ["esas faaliyet karı", "faaliyet karı", "faaliyet karı/zararı", "operating income", "operating profit", "ebit"]
        },
        "Amortisman ve İtfa": {
            "tms_adi": "Amortisman ve İtfa Giderleri",
            "ufrs_adi": "Depreciation and Amortization",
            "tms_standart": "TMS 16 / TMS 38",
            "ufrs_standart": "IAS 16 / IAS 38",
            "aciklama": "Maddi ve Maddi Olmayan Duran Varlıkların amortismanı",
            "hesaplama": "Maddi Duran Varlık Amortismanı + Maddi Olmayan Duran Varlık İtfası + Kullanım Hakkı Varlık İtfası",
            "alternatif_isimler": ["amortisman", "itfa", "depreciation", "amortization", "d&a"]
        },
        "FAVÖK (EBITDA)": {
            "tms_adi": "Faiz, Amortisman ve Vergi Öncesi Kar",
            "ufrs_adi": "Earnings Before Interest, Taxes, Depreciation and Amortization",
            "tms_standart": "Standart Dışı (Yönetim Raporlaması)",
            "ufrs_standart": "Non-GAAP Measure",
            "aciklama": "Yönetim performans ölçütü - standart dışı",
            "hesaplama": "Esas Faaliyet Karı + Amortisman + İtfa Giderleri",
            "alternatif_isimler": ["favök", "ebitda", "faiz amortisman vergi öncesi kar"]
        },
        "Finansman Gelir/Gider (Net)": {
            "tms_adi": "Finansman Geliri/Gideri (Net)",
            "ufrs_adi": "Finance Income/Costs (Net)",
            "tms_standart": "TMS 23 / TFRS 9",
            "ufrs_standart": "IAS 23 / IFRS 9",
            "aciklama": "Borçlanma maliyetleri ve finansal araçlar",
            "hesaplama": "Finansman Gelirleri - Finansman Giderleri",
            "alternatif_isimler": ["finansman gideri", "finansman geliri", "finance costs", "interest expense", "interest income"]
        },
        "Vergi Öncesi Kar": {
            "tms_adi": "Sürdürülen Faaliyetler Vergi Öncesi Karı/Zararı",
            "ufrs_adi": "Profit/Loss Before Tax from Continuing Operations",
            "tms_standart": "TMS 1 / TMS 12",
            "ufrs_standart": "IAS 1 / IAS 12",
            "aciklama": "Vergi öncesi dönem karı",
            "hesaplama": "Esas Faaliyet Karı + Finansman Gelirleri - Finansman Giderleri + Diğer Gelirler - Diğer Giderler",
            "alternatif_isimler": ["vergi öncesi kar", "pretax income", "profit before tax", "ebt"]
        },
        "Vergi (-)": {
            "tms_adi": "Dönem Vergi Gideri/Geliri",
            "ufrs_adi": "Income Tax Expense/Income",
            "tms_standart": "TMS 12",
            "ufrs_standart": "IAS 12",
            "aciklama": "Gelir Vergileri standardı",
            "hesaplama": "Cari Dönem Vergi Gideri + Ertelenmiş Vergi Gideri/Geliri",
            "alternatif_isimler": ["vergi", "tax", "income tax", "kurumlar vergisi", "dönem vergi gideri"]
        },
        "Net Kar/Zarar": {
            "tms_adi": "Dönem Karı/Zararı",
            "ufrs_adi": "Profit/Loss for the Period",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Net dönem sonucu (pozitif = kar, negatif = zarar)",
            "hesaplama": "Vergi Öncesi Kar - Vergi Gideri",
            "alternatif_isimler": ["net kar", "net kar/zarar", "net dönem karı", "dönem karı", "net income", "net profit", "profit for the period"]
        }
    },
    
    # ==========================================
    # BİLANÇO - VARLIKLAR
    # ==========================================
    "bilanco_varliklar": {
        "Dönen Varlıklar": {
            "tms_adi": "Dönen Varlıklar",
            "ufrs_adi": "Current Assets",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "12 ay içinde nakde çevrilmesi beklenen varlıklar",
            "hesaplama": "Nakit + Alacaklar + Stoklar + Diğer Dönen Varlıklar",
            "alternatif_isimler": ["dönen varlıklar", "current assets", "cari varlıklar"]
        },
        "Nakit ve Benzerleri": {
            "tms_adi": "Nakit ve Nakit Benzerleri",
            "ufrs_adi": "Cash and Cash Equivalents",
            "tms_standart": "TMS 7",
            "ufrs_standart": "IAS 7",
            "aciklama": "Nakit Akış Tablosu standardı",
            "hesaplama": "Kasa + Banka + Vadesiz Mevduat + 3 aya kadar vadeli araçlar",
            "alternatif_isimler": ["nakit", "cash", "nakit ve nakit benzerleri", "hazır değerler"]
        },
        "Ticari Alacaklar": {
            "tms_adi": "Ticari Alacaklar",
            "ufrs_adi": "Trade Receivables",
            "tms_standart": "TFRS 9 / TFRS 15",
            "ufrs_standart": "IFRS 9 / IFRS 15",
            "aciklama": "Finansal Araçlar ve Hasılat standartları",
            "hesaplama": "Alıcılar + Alacak Senetleri - Şüpheli Alacak Karşılığı",
            "alternatif_isimler": ["ticari alacaklar", "alacaklar", "trade receivables", "accounts receivable"]
        },
        "Stoklar": {
            "tms_adi": "Stoklar",
            "ufrs_adi": "Inventories",
            "tms_standart": "TMS 2",
            "ufrs_standart": "IAS 2",
            "aciklama": "Stoklar standardı (Maliyet veya net gerçekleşebilir değerin düşük olanı)",
            "hesaplama": "İlk Madde + Yarı Mamul + Mamul + Ticari Mal - Stok Değer Düşüklüğü Karşılığı",
            "alternatif_isimler": ["stoklar", "inventories", "inventory", "envanter"]
        },
        "Duran Varlıklar": {
            "tms_adi": "Duran Varlıklar",
            "ufrs_adi": "Non-Current Assets",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "12 aydan uzun vadeli varlıklar",
            "hesaplama": "Maddi DV + Maddi Olmayan DV + Finansal Yatırımlar + Diğer Duran Varlıklar",
            "alternatif_isimler": ["duran varlıklar", "non-current assets", "fixed assets", "uzun vadeli varlıklar"]
        },
        "Maddi Duran Varlıklar": {
            "tms_adi": "Maddi Duran Varlıklar",
            "ufrs_adi": "Property, Plant and Equipment",
            "tms_standart": "TMS 16",
            "ufrs_standart": "IAS 16",
            "aciklama": "Maddi Duran Varlıklar standardı",
            "hesaplama": "Maliyet Bedeli - Birikmiş Amortisman - Değer Düşüklüğü",
            "alternatif_isimler": ["maddi duran varlıklar", "ppe", "property plant equipment", "sabit kıymetler"]
        },
        "Kullanım Hakkı Varlıkları": {
            "tms_adi": "Kullanım Hakkı Varlıkları",
            "ufrs_adi": "Right-of-Use Assets",
            "tms_standart": "TFRS 16",
            "ufrs_standart": "IFRS 16",
            "aciklama": "Kiralamalar standardı",
            "hesaplama": "Kiralama başlangıcındaki değer - Birikmiş İtfa - Değer Düşüklüğü",
            "alternatif_isimler": ["kullanım hakkı varlıkları", "right of use assets", "rou assets", "kiralama varlıkları"]
        },
        "Maddi Olmayan Duran Varlıklar": {
            "tms_adi": "Maddi Olmayan Duran Varlıklar",
            "ufrs_adi": "Intangible Assets",
            "tms_standart": "TMS 38",
            "ufrs_standart": "IAS 38",
            "aciklama": "Maddi Olmayan Duran Varlıklar standardı",
            "hesaplama": "Şerefiye + Haklar + Lisanslar + Geliştirme Maliyetleri - Birikmiş İtfa",
            "alternatif_isimler": ["maddi olmayan duran varlıklar", "intangible assets", "intangibles", "gayri maddi varlıklar"]
        },
        "Şerefiye": {
            "tms_adi": "Şerefiye",
            "ufrs_adi": "Goodwill",
            "tms_standart": "TFRS 3",
            "ufrs_standart": "IFRS 3",
            "aciklama": "İşletme Birleşmeleri standardı",
            "hesaplama": "Ödenen bedel - Edinilen net varlıkların gerçeğe uygun değeri",
            "alternatif_isimler": ["şerefiye", "goodwill", "peştamallık"]
        },
        "Toplam Varlıklar": {
            "tms_adi": "Toplam Varlıklar",
            "ufrs_adi": "Total Assets",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Bilançonun aktif tarafı toplamı",
            "hesaplama": "Dönen Varlıklar + Duran Varlıklar",
            "alternatif_isimler": ["toplam varlıklar", "total assets", "aktif toplamı", "toplam aktifler"]
        }
    },
    
    # ==========================================
    # BİLANÇO - KAYNAKLAR
    # ==========================================
    "bilanco_kaynaklar": {
        "Kısa Vadeli Yükümlülükler": {
            "tms_adi": "Kısa Vadeli Yükümlülükler",
            "ufrs_adi": "Current Liabilities",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "12 ay içinde ödenmesi gereken yükümlülükler",
            "hesaplama": "Finansal Borçlar (KV) + Ticari Borçlar + Diğer KV Yükümlülükler",
            "alternatif_isimler": ["kısa vadeli yükümlülükler", "current liabilities", "kısa vadeli borçlar"]
        },
        "Finansal Borçlar (KV)": {
            "tms_adi": "Kısa Vadeli Borçlanmalar",
            "ufrs_adi": "Short-term Borrowings",
            "tms_standart": "TFRS 9 / TMS 32",
            "ufrs_standart": "IFRS 9 / IAS 32",
            "aciklama": "Finansal Araçlar standartları",
            "hesaplama": "Banka Kredileri (KV) + Çıkarılmış Tahviller (KV kısmı) + Kiralama Yükümlülükleri (KV)",
            "alternatif_isimler": ["finansal borçlar", "banka kredileri", "short-term borrowings", "bank loans"]
        },
        "Ticari Borçlar": {
            "tms_adi": "Ticari Borçlar",
            "ufrs_adi": "Trade Payables",
            "tms_standart": "TFRS 9",
            "ufrs_standart": "IFRS 9",
            "aciklama": "Ticari faaliyetlerden kaynaklanan borçlar",
            "hesaplama": "Satıcılar + Borç Senetleri + Alınan Avanslar",
            "alternatif_isimler": ["ticari borçlar", "satıcılar", "trade payables", "accounts payable"]
        },
        "Uzun Vadeli Yükümlülükler": {
            "tms_adi": "Uzun Vadeli Yükümlülükler",
            "ufrs_adi": "Non-Current Liabilities",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "12 aydan uzun vadeli yükümlülükler",
            "hesaplama": "Finansal Borçlar (UV) + Kiralama Yükümlülükleri (UV) + Kıdem Tazminatı + Ertelenmiş Vergi",
            "alternatif_isimler": ["uzun vadeli yükümlülükler", "non-current liabilities", "uzun vadeli borçlar"]
        },
        "Finansal Borçlar (UV)": {
            "tms_adi": "Uzun Vadeli Borçlanmalar",
            "ufrs_adi": "Long-term Borrowings",
            "tms_standart": "TFRS 9 / TMS 32",
            "ufrs_standart": "IFRS 9 / IAS 32",
            "aciklama": "Uzun vadeli finansal borçlar",
            "hesaplama": "Banka Kredileri (UV) + Çıkarılmış Tahviller + Kiralama Yükümlülükleri (UV)",
            "alternatif_isimler": ["uzun vadeli finansal borçlar", "long-term borrowings", "long-term debt"]
        },
        "Kıdem Tazminatı Karşılığı": {
            "tms_adi": "Çalışanlara Sağlanan Faydalara İlişkin Karşılıklar",
            "ufrs_adi": "Employee Benefit Obligations",
            "tms_standart": "TMS 19",
            "ufrs_standart": "IAS 19",
            "aciklama": "Çalışanlara Sağlanan Faydalar standardı",
            "hesaplama": "Aktüeryal hesaplama ile belirlenen bugünkü değer",
            "alternatif_isimler": ["kıdem tazminatı", "employee benefits", "pension obligations", "çalışan faydaları"]
        },
        "Ertelenmiş Vergi Yükümlülüğü": {
            "tms_adi": "Ertelenmiş Vergi Yükümlülüğü",
            "ufrs_adi": "Deferred Tax Liability",
            "tms_standart": "TMS 12",
            "ufrs_standart": "IAS 12",
            "aciklama": "Gelir Vergileri standardı - Geçici farklar",
            "hesaplama": "Vergiye tabi geçici farklar x Vergi oranı",
            "alternatif_isimler": ["ertelenmiş vergi yükümlülüğü", "deferred tax liability", "dtl"]
        },
        "Özkaynaklar": {
            "tms_adi": "Özkaynaklar",
            "ufrs_adi": "Equity",
            "tms_standart": "TMS 1 / TMS 32",
            "ufrs_standart": "IAS 1 / IAS 32",
            "aciklama": "Toplam varlıklar - Toplam yükümlülükler",
            "hesaplama": "Ödenmiş Sermaye + Sermaye Yedekleri + Kar Yedekleri + Geçmiş Yıl Karları + Dönem Karı",
            "alternatif_isimler": ["özkaynaklar", "equity", "shareholders equity", "net varlıklar"]
        },
        "Ödenmiş Sermaye": {
            "tms_adi": "Ödenmiş Sermaye",
            "ufrs_adi": "Issued Capital / Share Capital",
            "tms_standart": "TMS 32",
            "ufrs_standart": "IAS 32",
            "aciklama": "Çıkarılmış ve ödenmiş pay sermayesi",
            "hesaplama": "Çıkarılmış pay sayısı x Pay başına nominal değer",
            "alternatif_isimler": ["ödenmiş sermaye", "sermaye", "share capital", "issued capital"]
        },
        "Geçmiş Yıl Karları": {
            "tms_adi": "Geçmiş Yıllar Karları/Zararları",
            "ufrs_adi": "Retained Earnings",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Birikmiş karlar ve zararlar",
            "hesaplama": "Önceki dönem birikmiş kar/zarar + Dönem karı - Dağıtılan temettü",
            "alternatif_isimler": ["geçmiş yıl karları", "retained earnings", "birikmiş karlar"]
        },
        "Toplam Kaynaklar": {
            "tms_adi": "Toplam Kaynaklar (Yükümlülükler ve Özkaynaklar)",
            "ufrs_adi": "Total Equity and Liabilities",
            "tms_standart": "TMS 1",
            "ufrs_standart": "IAS 1",
            "aciklama": "Bilançonun pasif tarafı toplamı = Aktif toplamı",
            "hesaplama": "Kısa Vadeli Yük. + Uzun Vadeli Yük. + Özkaynaklar",
            "alternatif_isimler": ["toplam kaynaklar", "total liabilities and equity", "pasif toplamı"]
        }
    },
    
    # ==========================================
    # NAKİT AKIŞ TABLOSU
    # ==========================================
    "nakit_akis": {
        "İşletme Faaliyetlerinden Nakit": {
            "tms_adi": "İşletme Faaliyetlerinden Kaynaklanan Nakit Akışları",
            "ufrs_adi": "Cash Flows from Operating Activities",
            "tms_standart": "TMS 7",
            "ufrs_standart": "IAS 7",
            "aciklama": "Nakit Akış Tabloları standardı - Doğrudan veya dolaylı yöntem",
            "hesaplama": "Dönem Karı + Nakit Çıkışı Gerektirmeyen Giderler - İşletme Sermayesi Değişimi",
            "alternatif_isimler": ["işletme nakit akışı", "operating cash flow", "ocf", "faaliyetlerden nakit"]
        },
        "Yatırım Faaliyetlerinden Nakit": {
            "tms_adi": "Yatırım Faaliyetlerinden Kaynaklanan Nakit Akışları",
            "ufrs_adi": "Cash Flows from Investing Activities",
            "tms_standart": "TMS 7",
            "ufrs_standart": "IAS 7",
            "aciklama": "Uzun vadeli varlık alım/satımından kaynaklanan akışlar",
            "hesaplama": "Maddi DV Alımları + Maddi Olmayan DV Alımları - Satışlar + Yatırım Gelirleri",
            "alternatif_isimler": ["yatırım nakit akışı", "investing cash flow", "icf", "yatırımlardan nakit"]
        },
        "Finansman Faaliyetlerinden Nakit": {
            "tms_adi": "Finansman Faaliyetlerinden Kaynaklanan Nakit Akışları",
            "ufrs_adi": "Cash Flows from Financing Activities",
            "tms_standart": "TMS 7",
            "ufrs_standart": "IAS 7",
            "aciklama": "Özkaynaklar ve borçlanmalardaki değişimler",
            "hesaplama": "Kredi Kullanımları - Kredi Geri Ödemeleri - Temettü Ödemeleri - Faiz Ödemeleri",
            "alternatif_isimler": ["finansman nakit akışı", "financing cash flow", "fcf", "finansmandan nakit"]
        },
        "Serbest Nakit Akışı": {
            "tms_adi": "Serbest Nakit Akışı",
            "ufrs_adi": "Free Cash Flow",
            "tms_standart": "Standart Dışı (Yönetim Raporlaması)",
            "ufrs_standart": "Non-GAAP Measure",
            "aciklama": "İşletmenin serbest kullanabileceği nakit",
            "hesaplama": "İşletme Faaliyetlerinden Nakit - CAPEX (Sermaye Harcamaları)",
            "alternatif_isimler": ["serbest nakit akışı", "free cash flow", "fcf"]
        }
    }
}

# TMS/UFRS Kontrol fonksiyonları dosyanın başında tanımlandı (satır 144-240)

# ==========================================
# 2. VERİ İŞLEME MOTORU
# ==========================================
# HESAPLAMA_YONTEMLERI artık financial_analyzer.py'de
# Import edildi: from financial_analyzer import HESAPLAMA_YONTEMLERI

# pdf_to_dataframe fonksiyonu artık utils.py'de
# Import edildi: from utils import pdf_to_dataframe

# ==========================================
# 3. RASYO MOTORU
# ==========================================
# RasyoAnalizi sınıfı ve hesapla_rasyolar_cached fonksiyonu artık financial_analyzer.py'de
# Import edildi: from financial_analyzer import RasyoAnalizi, hesapla_rasyolar_cached

# ==========================================
# YENİ: BÜYÜK VERİ MOTORU (MASTER TABLE)
# ==========================================

# ==========================================
# 3. BÜYÜK VERİ MOTORU
# ==========================================
# BuyukVeriMotoru sınıfı artık buyuk_veri_engine.py modülünde
# Import edildi: from buyuk_veri_engine import BuyukVeriMotoru

# ==========================================
# 4. RAPORLAMA (PDF & EXCEL)
# ==========================================

# Export ve formatlama fonksiyonları artık utils.py'de
# Import edildi: from utils import to_excel, to_pdf, to_html, turkce_duzelt, style_rasyo_df

# ==========================================
# DOSYA YÜKLEME - VIEW MODÜLÜ KULLANIMI
# ==========================================
# Menu ekranında sidebar'da zaten dosya yükleme bölümü var, bu yüzden menu ekranında gösterilmiyor
if st.session_state.get('ekran_durumu') != 'menu':
    # Mapping modülü varsa get_standard_mapping'i kullan, yoksa None gönder
    mapping_func = get_standard_mapping if MAPPING_AVAILABLE else None
    show_file_upload_section(get_standard_mapping_func=mapping_func)

# ==========================================
# FİRMA BİLGİ FORMU - VIEW MODÜLÜ KULLANIMI
# ==========================================
# Menu ekranında sidebar'da zaten firma bilgileri bölümü var, bu yüzden menu ekranında gösterilmiyor
if st.session_state.get('ekran_durumu') != 'menu':
    show_company_info_form()

# Veri yüklenmemişse
if st.session_state.get('ekran_durumu') != 'menu':
    if 'df_gelir_raw' not in st.session_state:
        st.warning("Lütfen analize başlamak için sol menüden veya yukarıdan bir Excel/CSV dosyası yükleyin.")
        
        if st.session_state.get('authenticated', False):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.info("**Hızlı Başlangıç**")
                st.markdown("""
            1. Sol menüden **Dosya Yükle** butonuna basın.
            2. Gelen ekranda **Firma Bilgilerini** girin veya atlayın.
            3. Sistemin analizi tamamlamasını bekleyin.
            """)
        with col2:
            st.success("**Özellikler**")
            st.markdown("""
            * **Otomatik Sektör Tespiti:** Banka ve Reel sektör ayrımı.
            * **Hibrit Rasyo Analizi:** Sektöre özel finansal oranlar.
            * **Büyük Veri Motoru:** Tüm verilerin tek havuzda toplanması.
            * **Sankey Diyagramı:** Gelir akışını görselleştirin.
            """)