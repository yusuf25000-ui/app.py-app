import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="مكتب أبو محمد للتخليص", layout="wide")

# رابط الجدول
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.markdown("<h1 style='text-align: center;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 إدخال جديد", "📊 التقارير المرتبة"])

with tab1:
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            plate = st.text_input("رقم اللوحة")
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0)
            money = st.number_input("الرسوم", min_value=0.0)
            date_in = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("إصدار الفاتورة")
    
    if submit:
        st.success("تم إصدار الفاتورة بنجاح")
        # سطر البيانات الجاهز للنسخ (بالترتيب الصحيح)
        st.info("انسخ السطر التالي وضعه في الجدول:")
        row_to_copy = f"{date_in}, {importer}, {driver}, {plate}, {bags}, {money}"
        st.code(row_to_copy, language="text")

with tab2:
    if st.button("🔄 تحديث وعرض الجدول"):
        try:
            # قراءة البيانات
            df = pd.read_csv(csv_url)
            
            # تنظيف البيانات (تأكد من أن الأسماء تطابق الجدول)
            st.subheader("📋 كشف العمليات المكتملة")
            
            # عرض الإحصائيات بناءً على أسماء الأعمدة لضمان الدقة
            if not df.empty:
                # محاولة عرض البيانات بشكل منظم
                st.dataframe(df, use_container_width=True)
                
                # حساب الإجماليات إذا كانت الأسماء صحيحة
                if 'الرسوم' in df.columns and 'الأكياس' in df.columns:
                    c1, c2 = st.columns(2)
                    c1.metric("إجمالي المبالغ", f"{df['الرسوم'].sum():,.2f} ريال")
                    c2.metric("إجمالي الأكياس", f"{df['الأكياس'].sum():,}")
            else:
                st.info("الجدول فارغ")
        except Exception as e:
            st.error("حدث خطأ في قراءة الجدول. تأكد من أن الصف الأول في جوجل شيت يحتوي على العناوين.")
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
