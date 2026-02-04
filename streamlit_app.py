import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة وتنسيقها
st.set_page_config(page_title="مكتب أبو محمد للتخلص", layout="centered")

# رابط جدول جوجل الخاص بك
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# عنوان المكتب
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)
st.divider()

# التبويبات للتنقل بين الفاتورة والتقرير
tab1, tab2 = st.tabs(["📄 إصدار فاتورة", "📊 التقرير العام"])

with tab1:
    st.subheader("📝 أدخل بيانات المعاملة")
    with st.form("invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            plate = st.text_input("رقم القاطرة")
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("الرسوم الجمركية (ريال)", min_value=0.0)
            date_in = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("✨ توليد الفاتورة")

    if submit:
        # تصميم الفاتورة بشكل رسمي وجميل
        st.markdown(f"""
        <div style="direction: rtl; border: 5px solid #1E3A8A; padding: 25px; border-radius: 15px; background-color: white; color: black; font-family: 'Arial';">
            <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 0;">مكتب أبو محمد للتخليص الجمركي</h2>
            <p style="text-align: center; font-size: 14px; color: #555;">الجمهورية اليمنية - منفذ جمركي</p>
            <hr style="border: 1px solid #1E3A8A;">
            <table style="width: 100%; border-collapse: collapse; font-size: 18px; margin-top: 15px;">
                <tr><td style="padding: 10px;"><b>تاريخ البيان:</b></td><td>{date_in}</td></tr>
                <tr><td style="padding: 10px;"><b>اسم المستورد:</b></td><td>{importer}</td></tr>
                <tr><td style="padding: 10px;"><b>اسم السائق:</b></td><td>{driver}</td></tr>
                <tr><td style="padding: 10px;"><b>رقم القاطرة:</b></td><td>{plate}</td></tr>
                <tr><td style="padding: 10px;"><b>كمية الحمولة:</b></td><td>{bags:,} كيس</td></tr>
            </table>
            <div style="margin-top: 20px; padding: 15px; background-color: #F0F4FF; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0; color: #1E3A8A;">إجمالي الرسوم: {fees:,.2f} ريال</h3>
            </div>
            <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888;">شكرًا لتعاملكم مع مكتب أبو محمد</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 يمكنك الآن أخذ لقطة شاشة (Screenshot) للفاتورة أعلاه.")
        
        # كود النسخ للجدول
        st.write("---")
        st.write("📋 بيانات للنسخ لجدول جوجل:")
        st.code(f"{date_in}, {importer}, {driver}, {plate}, {bags}, {fees}", language="text")

with tab2:
    st.subheader("📊 ملخص التقارير اليومية والأسبوعية")
    if st.button("🔄 تحديث وقراءة البيانات"):
        try:
            df = pd.read_csv(csv_url)
            if not df.empty:
                # إحصائيات سريعة
                total_trucks = len(df)
                # استخدام ترتيب الأعمدة (التاريخ=0، المستورد=1، السائق=2، اللوحة=3، الأكياس=4، الرسوم=5)
                total_bags = pd.to_numeric(df.iloc[:, 4], errors='coerce').sum()
                total_money = pd.to_numeric(df.iloc[:, 5], errors='coerce').sum()

                c1, c2, c3 = st.columns(3)
                c1.metric("عدد القواطر", f"{total_trucks}")
                c2.metric("إجمالي الأكياس", f"{total_bags:,.0f}")
                c3.metric("إجمالي المبالغ", f"{total_money:,.2f}")

                st.divider()
                st.write("📋 كشف تفصيلي بالعمليات:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("الجدول لا يحتوي على بيانات حالياً.")
        except Exception as e:
            st.error("لم نتمكن من قراءة الجدول. تأكد أن الأعمدة في جوجل شيت تبدأ من (A1) بهذا الترتيب: التاريخ، المستورد، السائق، اللوحة، الأكياس، الرسوم.")

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
