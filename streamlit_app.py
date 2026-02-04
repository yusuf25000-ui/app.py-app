import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="أبو محمد للتخليص", layout="wide")

# رابط الجدول الخاص بك
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)
st.divider()

# التبويبات
tab1, tab2 = st.tabs(["📝 إدخال جديد", "📊 التقارير"])

with tab1:
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            plate = st.text_input("رقم اللوحة")
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0, value=0)
            fees = st.number_input("الرسوم", min_value=0.0, value=0.0)
            date_in = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("🚀 إصدار الفاتورة")
    
    if submit:
        st.success("✅ تم إصدار الفاتورة")
        # تصميم الفاتورة
        st.markdown(f"""
        <div style="direction:rtl; border:2px solid #1e3a8a; padding:15px; border-radius:10px; background-color:#fdfdfd;">
            <h3 style="text-align:center;">فاتورة تخليص جمركي</h3>
            <p><b>السائق:</b> {driver}</p>
            <p><b>اللوحة:</b> {plate}</p>
            <p><b>المستورد:</b> {importer}</p>
            <p><b>الكمية:</b> {bags:,} كيس</p>
            <h4 style="color:blue;">إجمالي الرسوم: {fees:,.2f} ريال</h4>
            <p style="font-size:10px; color:gray;">التاريخ: {date_in}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # سطر البيانات للنسخ
        st.info("💡 انسخ السطر التالي وضعه في ملف جوجل شيت:")
        row_text = f"{date_in}, {importer}, {driver}, {plate}, {bags}, {fees}"
        st.code(row_text, language="text")

with tab2:
    if st.button("🔄 تحديث البيانات من جوجل"):
        try:
            # قراءة البيانات مع تجاهل أخطاء العناوين
            df = pd.read_csv(csv_url)
            
            if not df.empty:
                st.subheader("📋 كشف العمليات")
                st.dataframe(df, use_container_width=True)
                
                # حساب الإجماليات بناءً على موقع العمود (العمود 5 للأكياس و6 للرسوم)
                # نستخدم try للتأكد من أن الأعمدة تحتوي على أرقام
                try:
                    total_bags = pd.to_numeric(df.iloc[:, 4]).sum()
                    total_fees = pd.to_numeric(df.iloc[:, 5]).sum()
                    
                    c1, c2 = st.columns(2)
                    c1.metric("إجمالي الأكياس", f"{total_bags:,}")
                    c2.metric("إجمالي المبالغ", f"{total_fees:,.2f} ريال")
                except:
                    st.warning("تأكد من إدخال الأرقام بشكل صحيح في الجدول (الأعمدة 5 و 6)")
            else:
                st.info("الجدول فارغ")
        except Exception as e:
            st.error("فشل الاتصال بالجدول. تأكد من أن الرابط يعمل وأنك أضفت بيانات.")
