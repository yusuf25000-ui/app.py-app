import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="مكتب أبو محمد للتخلص", layout="wide")

# الربط القوي بجدول جوجل
conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ نظام مكتب أبو محمد للتخليص</h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["📄 إصدار وحفظ فاتورة", "📊 تقارير الحسابات"])

with tab1:
    st.subheader("📝 إدخال معاملة جديدة")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            plate = st.text_input("رقم اللوحة")
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("الرسوم (ريال)", min_value=0.0)
            date_val = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("🚀 حفظ وإصدار الفاتورة")

    if submit:
        if importer and driver:
            # 1. جلب البيانات القديمة
            df_old = conn.read()
            # 2. إضافة السطر الجديد
            new_row = pd.DataFrame([{
                "التاريخ": str(date_val),
                "المستورد": importer,
                "السائق": driver,
                "اللوحة": plate,
                "الأكياس": bags,
                "الرسوم": fees
            }])
            df_final = pd.concat([df_old, new_row], ignore_index=True)
            # 3. التحديث المباشر في جوجل شيت
            conn.update(data=df_final)
            
            st.success("✅ تم الحفظ تلقائياً في الجدول!")
            
            # عرض الفاتورة للتصوير
            st.markdown(f"""
            <div style="direction: rtl; border: 4px solid #1E3A8A; padding: 20px; border-radius: 10px; background-color: white; color: black;">
                <h2 style="text-align: center;">فاتورة تخليص جمركي</h2>
                <hr>
                <p><b>السائق:</b> {driver} | <b>اللوحة:</b> {plate}</p>
                <p><b>المستورد:</b> {importer} | <b>الكمية:</b> {bags} كيس</p>
                <h3 style="text-align: center; background-color: #f1f5f9; padding: 10px;">الإجمالي: {fees:,.2f} ريال</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("يرجى إدخال البيانات الأساسية")

with tab2:
    st.subheader("📈 التقرير العام")
    if st.button("🔄 تحديث الحسابات"):
        df = conn.read()
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("عدد القواطر", len(df))
            c2.metric("إجمالي الأكياس", f"{pd.to_numeric(df['الأكياس']).sum():,}")
            c3.metric("إجمالي المبالغ", f"{pd.to_numeric(df['الرسوم']).sum():,.2f}")
            st.dataframe(df, use_container_width=True)
