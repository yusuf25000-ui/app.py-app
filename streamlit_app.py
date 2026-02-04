import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# إعداد واجهة التطبيق
st.set_page_config(page_title="مكتب أبو محمد للتخلص الجمركي", layout="centered")

# دالة لتحويل النص إلى ملف PDF بسيط (HTML-based)
def create_pdf_link(content, filename):
    b64 = base64.b64encode(content.encode('utf-8-sig')).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}.html" style="text-decoration:none;"><button style="background-color:#1E3A8A; color:white; border-radius:5px; padding:10px;">📥 تحميل الفاتورة (PDF/HTML)</button></a>'

# الهوية البصرية
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)
st.divider()

# نموذج الإدخال
with st.form("abu_mohammed_pro", clear_on_submit=False):
    st.subheader("📑 بيانات الفاتورة الجمركية")
    col1, col2 = st.columns(2)
    with col1:
        importer = st.text_input("اسم المستورد")
        driver_name = st.text_input("اسم السائق")
        truck_no = st.text_input("رقم القاطرة")
    with col2:
        truck_type = st.selectbox("نوع القاطرة", ["قاطرة فـلاب", "سطحة", "جوانب", "دينا"])
        bags_count = st.number_input("عدد الأكياس", min_value=0)
        total_fees = st.number_input("إجمالي الرسوم (ريال)", min_value=0.0)
    
    submit = st.form_submit_button("🚀 إصدار الفاتورة النهائية")

if submit:
    if importer and driver_name:
        # تصميم الفاتورة
        invoice_content = f"""
        <div style="direction: rtl; font-family: 'Arial'; border: 2px solid #1E3A8A; padding: 20px;">
            <h2 style="text-align: center;">مكتب أبو محمد للتخليص الجمركي</h2>
            <p><b>التاريخ:</b> {datetime.now().strftime('%Y-%m-%d')}</p>
            <hr>
            <p><b>اسم المستورد:</b> {importer}</p>
            <p><b>اسم السائق:</b> {driver_name}</p>
            <p><b>رقم القاطرة:</b> {truck_no}</p>
            <p><b>الكمية:</b> {bags_count} كيس</p>
            <h3 style="background-color: #f0f0f0; padding: 10px;">إجمالي الرسوم: {total_fees:,.2f} ريال</h3>
        </div>
        """
        st.markdown(invoice_content, unsafe_allow_html=True)
        
        # زر التحميل
        st.markdown(create_pdf_link(invoice_content, f"فاتورة_{driver_name}"), unsafe_allow_html=True)
        st.info("ملاحظة: اضغط على الزر أعلاه لحفظ الفاتورة على هاتفك.")
    else:
        st.error("يرجى إكمال البيانات أولاً")
        # عرض الملخص في جدول منسق
        summary_data = {
            "التاريخ": [report_date],
            "رقم البيان": [statement_ref],
            "السائق": [driver_name],
            "رقم القاطرة": [truck_no],
            "نوعها": [truck_type],
            "خط السير": [route],
            "إجمالي الأكياس": [f"{total_bags:,.0f} كيس"]
        }
        
        df = pd.DataFrame(summary_data)
        st.table(df)
        
        # ميزة إضافية: تنبيه إذا كان العدد ضخماً
        if total_bags > 1000:
            st.warning("⚠️ ملاحظة: الكمية تتجاوز 1000 كيس، يرجى التأكد من مطابقة الحمولة.")
            
    except ValueError:
        st.error("❌ خطأ في إدخال عدد الأكياس. يرجى كتابة أرقام فقط (مثال: 500 أو 500+200)")

