import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="مكتب أبو محمد للتخلص", layout="wide")

# رابط الصورة المباشر (تأكد من استخدام الرابط الذي ينتهي بـ .jpg أو .png)
LOGO_URL = "https://raw.githubusercontent.com/yusuf23000-ui/app.py-app/main/7569.jpg"

# رابط الجدول الخاص بك
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- واجهة البرنامج ---
# عرض الصورة في أعلى التطبيق للتأكد من أنها تعمل
st.image(LOGO_URL, width=200)
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ نظام مكتب أبو محمد للتخليص</h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["📄 إصدار فاتورة ذكية", "📊 التقارير"])

with tab1:
    with st.form("invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver_name = st.text_input("اسم السائق")
            plate = st.text_input("رقم اللوحة")
            chassis = st.text_input("رقم القعادة")
        with col2:
            manifest_no = st.text_input("رقم البيان")
            bags = st.number_input("عدد الأكياس", min_value=0)
            fees = st.number_input("الرسوم (ريال)", min_value=0.0)
            date_val = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("✨ توليد الفاتورة")

    if submit:
        # تصميم الفاتورة مع كود يضمن ظهور الصورة
        st.markdown(f"""
        <div style="direction: rtl; border: 5px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: white; color: black; font-family: 'Arial'; text-align: right;">
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="{LOGO_URL}" style="width: 150px; height: auto;">
                <h2 style="color: #1E3A8A; margin-top: 5px;">مكتب أبو محمد للتخليص الجمركي</h2>
            </div>
            <hr style="border: 1px solid #1E3A8A;">
            <table style="width: 100%; font-size: 18px;">
                <tr><td><b>التاريخ:</b> {date_val}</td><td><b>رقم البيان:</b> {manifest_no}</td></tr>
                <tr><td><b>المستورد:</b> {importer}</td><td><b>السائق:</b> {driver_name}</td></tr>
                <tr><td><b>اللوحة:</b> {plate}</td><td><b>القعادة:</b> {chassis}</td></tr>
                <tr><td colspan="2"><b>الكمية:</b> {bags:,} كيس</td></tr>
            </table>
            <div style="margin-top: 20px; padding: 15px; background-color: #f1f5f9; border-radius: 10px; text-align: center; border: 1px solid #1E3A8A;">
                <h3 style="margin: 0; color: #1E3A8A;">إجمالي الرسوم: {fees:,.2f} ريال</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 إذا لم تظهر الصورة في الفاتورة، تأكد من تحديث الصفحة (Refresh).")
        st.code(f"{date_val}, {importer}, {driver_name}, {plate}, {chassis}, {manifest_no}, {bags}, {fees}", language="text")

with tab2:
    if st.button("تحديث البيانات"):
        df = pd.read_csv(csv_url)
        st.dataframe(df)
https://raw.githubusercontent.com/yusuf23000-ui/app.py-app/main/7569.jpg
