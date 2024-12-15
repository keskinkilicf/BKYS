import streamlit as st
from datetime import datetime
import pandas as pd
import google.generativeai as genai

# API Anahtarı
GEMINI_ANAHTARI = "AIzaSyD1e1jL3tJ8tyihXLNtbWLFSf-xOJ8Nc_w"

# Gemini API'yi yapılandırma
genai.configure(api_key=GEMINI_ANAHTARI)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_activity_recommendations(unit, activity_name, description, date):
    prompt = f"""
    Kalite yönetim sistemine yönelik faaliyet planlaması ve kanıt oluşturma konusunda bir uzman gibi davran ve aşağıdaki bilgilere göre önerilerde bulun:
    Birim: {unit}
    Faaliyet Adı: {activity_name}
    Açıklama: {description}
    Tarih: {date}

    Lütfen şunları sağla:
    1. Faaliyetin iyileştirilmesi için öneriler
    2. Faaliyetle ilgili olası riskler ve önlemler
    3. Gerekli kaynaklar ve verimlilik artırıcı öneriler
    """
    response = model.generate_content(prompt)
    return response.text

# Başlık ve tanıtım
st.title("BKYS")
st.title("📋 Bütünleşik Kalite Yönetim Sistemi Kanıt Giriş Formu")
st.write("Bu form, kalite yönetim sistemi gerçekleştirme kanıtlarını kayıt altına almanızı sağlar.")

# Form alanları
st.subheader("Birim Bilgileri")

birim = st.text_input("Birim Adı", placeholder="Örneğin: Uzaktan Eğitim Araştırma ve Uygulama Merkezi")
alt_birim = st.text_input("Alt Birim", placeholder="Alt birimi belirtiniz (isteğe bağlı)")

donem = st.text_input("Dönem", placeholder="Örneğin: 2024 Yaz")

gerceklesme_tarihi = st.date_input("Gerçekleşme Tarihi", value=datetime.now())

st.subheader("Faaliyet Bilgileri")

faaliyet_adi = st.text_area("Gerçekleştirilen Faaliyet Adı", placeholder="Faaliyetin adını yazınız")

gerceklesmeyen_gerekce = st.text_area("Gerçekleştirilemeyen Faaliyetler İçin Gerekçe", placeholder="Eğer bir faaliyet gerçekleştirilemediyse, gerekçesini yazınız (isteğe bağlı)")

faaliyet_aciklama = st.text_area("Faaliyet Gerçekleştirme Açıklaması", placeholder="Faaliyetin gerçekleştirilme sürecini açıklayınız")

faaliyet_kanit_gorseli = st.file_uploader("Faaliyet Gerçekleştirme Kanıt Görseli", type=["jpg", "jpeg", "png", "pdf"])

değerlendirme = st.text_area("Değerlendirme", placeholder="Faaliyetle ilgili değerlendirme açıklaması")

# Öneri butonu
if st.button("Yapay Zeka Önerilerini Al"):
    if birim and faaliyet_adi and faaliyet_aciklama:
        with st.spinner("Öneriler oluşturuluyor..."):
            öneriler = get_activity_recommendations(birim, faaliyet_adi, faaliyet_aciklama, gerceklesme_tarihi.strftime("%Y-%m-%d"))
            st.markdown(öneriler)
    else:
        st.warning("Lütfen birim, faaliyet adı ve açıklama alanlarını doldurun!")

# Kaydetme butonu
if st.button("Kaydet"):
    if birim and donem and gerceklesme_tarihi and faaliyet_adi and faaliyet_aciklama and değerlendirme:
        # Verileri bir tabloya kaydetme
        data = {
            "Birim": [birim],
            "Alt Birim": [alt_birim],
            "Dönem": [donem],
            "Gerçekleşme Tarihi": [gerceklesme_tarihi.strftime("%Y-%m-%d")],
            "Gerçekleştirilen Faaliyet Adı": [faaliyet_adi],
            "Gerçekleştirilemeyen Gerekçe": [gerceklesmeyen_gerekce],
            "Faaliyet Açıklaması": [faaliyet_aciklama],
            "Değerlendirme": [değerlendirme],
            "Kanıt Görseli": [faaliyet_kanit_gorseli.name if faaliyet_kanit_gorseli else "Yok"]
        }
        df = pd.DataFrame(data)

        # CSV'ye kaydetme
        try:
            df.to_csv("kanit_girisleri.csv", mode='a', header=False, index=False)
            st.success("Kanıt başarıyla kaydedildi!")
        except Exception as e:
            st.error(f"Kaydetme sırasında bir hata oluştu: {e}")
    else:
        st.warning("Lütfen tüm zorunlu alanları doldurun!")
