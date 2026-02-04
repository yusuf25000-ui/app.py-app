import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="أبو محمد للتخليص", layout="wide")

# الرابط الخاص بجدولك
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏗️ مكتب أبو محمد للتخليص الجمركي")

# التبويبات
tab1, tab2 = st.tabs(["📝 إدخال فاتورة", "📊 التقارير"])

with tab1:
    with st.form("main_form"):
        imp = st.text_input("اسم المستورد")
        drv = st.text_input("اسم السائق")
        plate = st.text_input("رقم اللوحة")
        bags = st.number_input("عدد الأكياس", min_value=0)
        money = st.number_input("الرسوم الجمركية", min_value=0.0)
        btn = st.form_submit_button("إصدار الفاتورة")
    
    if btn:
        st.success("تم تجهيز بيانات الفاتورة")
        # تصميم الفاتورة للعرض فقط
        st.markdown(f"""
        <div style="direction:rtl; border:2px solid #1e3a8a; padding:15px; border-radius:10px; text-align:right;">
        <h3>فاتورة تخليص جمركي</h3>
        <b>السائق:</b> {drv}<br>
        <b>اللوحة:</b> {plate}<br>
        <b>المستورد:</b> {imp}<br>
        <b>الكمية:</b> {bags} كيس<br>
        <h4 style="color:green;">الإجمالي: {money} ريال</h4>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    if st.button("تحديث البيانات من جوجل"):
        try:
            df = pd.read_csv(csv_url)
            st.write("إحصائيات الجدول:")
            st.dataframe(df)
        except Exception as e:
            st.error("تأكد من وجود بيانات في جدول جوجل شيت أولاً")
