import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات التطبيق باسم أبو محمد
st.set_page_config(page_title="مكتب أبو محمد للتخليص", layout="wide", page_icon="🏗️")

# رابط الجدول الذي أرسلته (بصيغة CSV للقراءة)
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# واجهة البرنامج
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["📝 إصدار فاتورة جديدة", "📊 التقارير الأسبوعية واليومية"])

with tab1:
    with st.form("invoice_form", clear_on_submit=True):
        st.subheader("📋 إدخال بيانات المعاملة")
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            truck_no = st.text_input("رقم اللوحة / القاطرة")
            truck_type = st.selectbox("نوع القاطرة", ["فـلاب", "سطحة", "جوانب", "دينا"])
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("إجمالي الرسوم الجمركية (ريال)", min_value=0.0)
            date_val = st.date_input("التاريخ", datetime.now())
            route = st.text_input("خط السير")
        
        submit = st.form_submit_button("🚀 إصدار ملخص الفاتورة")

    if submit:
        if importer and driver:
            st.success("✅ تم توليد الملخص بنجاح")
            # تصميم الفاتورة الرقمية
            invoice_html = f"""
            <div style="direction: rtl; border: 3px double #1E3A8A; padding: 20px; border-radius: 10px; background-color: #f9f9f9; color: #333;">
                <h2 style="text-align: center; color: #1E3A8A;">مكتب أبو محمد للتخليص الجمركي</h2>
                <hr>
                <p><b>اسم السائق:</b> {driver}</p>
                <p><b>رقم اللوحة:</b> {truck_no} ({truck_type})</p>
                <p><b>اسم المستورد:</b> {importer}</p>
                <p><b>عدد الأكياس:</b> {bags:,} كيس</p>
                <p><b>خط السير:</b> {route}</p>
                <h3 style="text-align: center; background-color: #E0E7FF; padding: 10px;">إجمالي الرسوم: {fees:,.2f} ريال</h3>
                <p style="text-align: center; font-size: 12px; color: gray;">تاريخ: {date_val}</p>
            </div>
            """
            st.markdown(invoice_html, unsafe_allow_html=True)
            
            # سطر البيانات للنسخ اليدوي (بسبب قيود الاشتراك في جوجل)
            st.info("💡 لنسخ هذه المعاملة إلى جدول التقارير، انسخ السطر أدناه وضعه في ملف جوجل شيت:")
            data_row = f"{date_val}, {importer}, {driver}, {truck_no}, {truck_type}, {bags}, {fees}, {route}"
            st.code(data_row, language="text")
        else:
            st.error("يرجى إكمال البيانات الأساسية")

with tab2:
    st.subheader("📈 ملخص العمليات من جدول جوجل")
    if st.button("🔄 تحديث البيانات من الجدول"):
        try:
            # قراءة البيانات مباشرة من الرابط الذي قدمته
            df = pd.read_csv(csv_url)
            
            if not df.empty:
                # حساب الإحصائيات (نفترض أن الأعمدة مرتبة كما طلبنا)
                c1, c2, c3 = st.columns(3)
                c1.metric("إجمالي القواطر", len(df))
                # ملاحظة: سنستخدم أسماء الأعمدة كما هي في ملفك أو بالترتيب الرقمي
                c2.metric("إجمالي الأكياس", f"{df.iloc[:, 5].sum():,}") 
                c3.metric("إجمالي الرسوم", f"{df.iloc[:, 6].sum():,.2f}")
                
                st.write("📋 سجل العمليات التاريخي:")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("الجدول فارغ حالياً.")
        except Exception as e:
            st.error("تأكد من أن الجدول يحتوي على بيانات وأن الأعمدة مرتبة بشكل صحيح.")
            st.info("يجب أن تكون الأعمدة في الجدول بالترتيب: التاريخ، المستورد، السائق، اللوحة، النوع، الأكياس، الرسوم، خط السير")
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
