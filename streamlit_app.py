import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# إعداد واجهة التطبيق
st.set_page_config(page_title="أبو محمد للتخليص الجمركي", layout="centered")

# دالة لتحميل الفاتورة
def get_table_download_link(html_content, filename):
    b64 = base64.b64encode(html_content.encode('utf-8-sig')).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}.html" style="text-decoration:none;"><button style="background-color:#1E3A8A; color:white; border-radius:5px; padding:10px; width:100%;">📥 تحميل الفاتورة (PDF/HTML)</button></a>'

# الهوية البصرية
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)
st.divider()

# نموذج الإدخال
with st.form("invoice_form", clear_on_submit=False):
    st.subheader("📝 بيانات البيان الجمركي")
    col1, col2 = st.columns(2)
    with col1:
        importer = st.text_input("اسم المستورد")
        driver = st.text_input("اسم السائق")
        truck_no = st.text_input("رقم القاطرة")
    with col2:
        truck_type = st.selectbox("نوع القاطرة", ["قاطرة فـلاب", "سطحة", "جوانب", "دينا"])
        bags = st.number_input("عدد الأكياس", min_value=0, step=1)
        fees = st.number_input("إجمالي الرسوم (ريال)", min_value=0.0)
    
    submit = st.form_submit_button("🚀 إصدار الفاتورة النهائية")

if submit:
    if importer and driver and truck_no:
        # تصميم الفاتورة الرقمية
        invoice_html = f"""
        <div style="direction: rtl; font-family: 'Arial'; border: 3px double #1E3A8A; padding: 20px; border-radius: 10px; background-color: white;">
            <h2 style="text-align: center; color: #1E3A8A;">مكتب أبو محمد للتخليص الجمركي</h2>
            <p style="text-align: center;">التاريخ: {datetime.now().strftime('%Y-%m-%d')}</p>
            <hr>
            <table style="width: 100%; border-collapse: collapse; font-size: 18px;">
                <tr><td style="padding: 8px;"><b>اسم المستورد:</b></td><td>{importer}</td></tr>
                <tr><td style="padding: 8px;"><b>اسم السائق:</b></td><td>{driver}</td></tr>
                <tr><td style="padding: 8px;"><b>رقم القاطرة:</b></td><td>{truck_no}</td></tr>
                <tr><td style="padding: 8px;"><b>نوع القاطرة:</b></td><td>{truck_type}</td></tr>
                <tr><td style="padding: 8px;"><b>عدد الأكياس:</b></td><td>{bags:,} كيس</td></tr>
            </table>
            <hr>
            <h3 style="text-align: center; background-color: #f0f4ff; padding: 15px;">إجمالي الرسوم: {fees:,.2f} ريال</h3>
            <p style="text-align: center; font-size: 12px; color: gray;">صدرت آلياً من نظام أبو محمد للتخليص</p>
        </div>
        """
        st.markdown(invoice_html, unsafe_allow_html=True)
        
        # زر التحميل
        st.markdown(get_table_download_link(invoice_html, f"فاتورة_{driver}"), unsafe_allow_html=True)
        st.success("تم إصدار الفاتورة. يمكنك الآن تصوير الشاشة أو ضغط زر التحميل.")
    else:
        st.error("⚠️ يرجى تعبئة الحقول الأساسية أولاً.")
