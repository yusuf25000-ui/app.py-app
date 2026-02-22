import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="مكتب أبو محمد للتخليص", layout="wide")

# الرابط المباشر للصورة
LOGO_URL = "https://raw.githubusercontent.com/yusuf23000-ui/app.py-app/main/7569.jpg"

# رابط جدول جوجل الخاص بك (للقراءة)
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- وظيفة جلب البيانات للتعبئة الآلية ---
def load_data():
    try:
        df = pd.read_csv(csv_url)
        # تنظيف الأسماء من المسافات الزائدة
        df['السائق'] = df['السائق'].astype(str).str.strip()
        return df
    except:
        return pd.DataFrame()

df_history = load_data()

# --- واجهة البرنامج ---
st.image(LOGO_URL, width=150)
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ نظام مكتب أبو محمد للتخليص</h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["📄 إصدار فاتورة ذكية", "📊 التقارير اليومية"])

with tab1:
    st.subheader("📝 إدخال بيانات المعاملة")
    
    # ميزة التعبئة الآلية
    all_drivers = ["جديد"]
    if not df_history.empty:
        all_drivers += sorted(df_history['السائق'].unique().tolist())
    
    selected_driver = st.selectbox("اختر سائقاً مسجلاً لتعبئة بياناته آلياً:", all_drivers)
    
    # تحديد القيم الافتراضية
    init_plate = ""
    init_chassis = ""
    if selected_driver != "جديد":
        # جلب آخر سجل لهذا السائق
        last_info = df_history[df_history['السائق'] == selected_driver].iloc[-1]
        init_plate = last_info['اللوحة']
        init_chassis = last_info['القعادة']

    with st.form("invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_val = st.date_input("التاريخ", datetime.now())
            manifest_no = st.text_input("رقم البيان")
            importer = st.text_input("اسم المستورد")
            driver_name = st.text_input("اسم السائق", value="" if selected_driver == "جديد" else selected_driver)
        with col2:
            plate = st.text_input("رقم اللوحة", value=init_plate)
            chassis = st.text_input("رقم القعادة", value=init_chassis)
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("الرسوم (ريال)", min_value=0.0)
        
        submit = st.form_submit_button("✨ توليد الفاتورة")

    if submit:
        # تصميم الفاتورة الاحترافي
        st.markdown(f"""
        <div style="direction: rtl; border: 4px solid #1E3A8A; padding: 25px; border-radius: 15px; background-color: white; color: black; font-family: 'Arial';">
            <div style="text-align: center;">
                <img src="{LOGO_URL}" width="180">
                <h2 style="color: #1E3A8A; margin-top: 10px;">فاتورة تخليص جمركي</h2>
            </div>
            <hr>
            <table style="width: 100%; font-size: 18px; border-spacing: 10px;">
                <tr><td><b>التاريخ:</b> {date_val}</td><td><b>رقم البيان:</b> {manifest_no}</td></tr>
                <tr><td><b>المستورد:</b> {importer}</td><td><b>السائق:</b> {driver_name}</td></tr>
                <tr><td><b>اللوحة:</b> {plate}</td><td><b>القعادة:</b> {chassis}</td></tr>
                <tr style="background-color: #f1f5f9;"><td colspan="2" style="text-align:center; padding:10px;"><b>الكمية:</b> {bags:,} كيس</td></tr>
            </table>
            <div style="margin-top: 20px; padding: 15px; background-color: #1E3A8A; color: white; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0;">إجمالي الرسوم: {fees:,.2f} ريال</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # سطر البيانات للنسخ
        st.write("---")
        st.info("💡 انسخ السطر التالي وضعه في جدول جوجل شيت:")
        row_to_add = f"{date_val}, {manifest_no}, {importer}, {driver_name}, {plate}, {chassis}, {bags}, {fees}"
        st.code(row_to_add, language="text")

with tab2:
    st.subheader("📊 ملخص العمليات")
    if st.button("🔄 تحديث التقارير"):
        df = pd.read_csv(csv_url)
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("عدد القواطر", len(df))
            c2.metric("إجمالي الأكياس", f"{pd.to_numeric(df['الأكياس'], errors='coerce').sum():,.0f}")
            c3.metric("إجمالي المبالغ", f"{pd.to_numeric(df['الرسوم'], errors='coerce').sum():,.2f}")
            st.dataframe(df, use_container_width=True)
