import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد واجهة النظام بناءً على الاستمارة الرسمية
st.set_page_config(page_title="نظام المعاينة الجمركية", layout="wide")

st.title("📋 استمارة معاينة الغمارة والجوانب")
st.write("نقل بضائع محلية - مصلحة الضرائب والجمارك")

with st.form("customs_form", clear_on_submit=True):
    # القسم الأول: بيانات عامة
    st.subheader("📌 البيانات العامة والشحنة")
    col1, col2, col3 = st.columns(3)
    with col1:
        importer = st.text_input("اسم المستورد")
        driver_name = st.text_input("اسم السائق")
    with col2:
        statement_no = st.text_input("رقم البيان")
        seal_no = st.text_input("رقم السيل")
    with col3:
        report_date = st.date_input("التاريخ", datetime.now())
        goods_type = st.text_input("نوع البضاعة")

    st.divider()

    # القسم الثاني: بيانات الإسمنت (بناءً على طلبك)
    st.subheader("🏗️ تفاصيل الإسمنت والكميات")
    col4, col5, col6 = st.columns(3)
    with col4:
        cement_type = st.text_input("نوع الإسمنت")
    with col5:
        bags_count = st.number_input("عدد الأكياس", min_value=0, step=1)
    with col6:
        company_origin = st.text_input("إنتاج شركة /")

    st.divider()

    # القسم الثالث: بيانات الوسيلة (السيارة)
    st.subheader("🚛 بيانات وسيلة النقل")
    col7, col8 = st.columns(2)
    with col7:
        plate_no = st.text_input("رقم اللوحة")
    with col8:
        chassis_no = st.text_input("رقم القعادة")

    st.divider()

    # القسم الرابع: المصادقة
    st.subheader("✍️ المصادقة والاعتماد")
    col9, col10 = st.columns(2)
    with col9:
        inspector_auth = st.checkbox("توقيع ومصادقة المعاين")
    with col10:
        officer_auth = st.checkbox("توقيع ومصادقة الضابطة الجمركية")

    # زر الإرسال النهائي
    submitted = st.form_submit_button("🚀 إرسال البيانات آلياً لمختص الثمن")

if submitted:
    if inspector_auth and officer_auth:
        st.success("✅ تم الاعتماد والإرسال بنجاح لمختص الثمن")
        # عرض ملخص سريع
        st.info(f"تم تسجيل القاطرة رقم {plate_no} - حمولة {cement_type}")
    else:
        st.warning("🚫 لا يمكن الإرسال بدون مصادقة 'المعاين' و 'الضابطة الجمركية' معاً.")
