import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مكتب أبو محمد للتخليص", layout="centered")

# 2. رابط جدول جوجل الخاص بك
# تأكد من أن الرابط هو نفس الذي أرسلته لي سابقاً
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 3. واجهة البرنامج (الهوية البصرية)
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ مكتب أبو محمد للتخليص الجمركي</h1>", unsafe_allow_html=True)
st.divider()

# 4. التبويبات (فاتورة وتقارير)
tab1, tab2 = st.tabs(["📄 إصدار فاتورة", "📊 التقارير العامة"])

# --- التبويب الأول: إصدار الفاتورة ---
with tab1:
    st.subheader("📝 إدخال بيانات المعاملة")
    with st.form("invoice_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            plate = st.text_input("رقم القاطرة")
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("الرسوم (ريال)", min_value=0.0)
            date_in = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("✨ توليد الفاتورة")

    if submit:
        if importer and driver and plate:
            # عرض الفاتورة بتصميم احترافي
            st.markdown(f"""
            <div style="direction: rtl; border: 4px solid #1E3A8A; padding: 25px; border-radius: 15px; background-color: #FFFFFF; color: #000000; font-family: 'Arial';">
                <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 5px;">مكتب أبو محمد للتخليص الجمركي</h2>
                <p style="text-align: center; font-size: 14px; margin-top: 0;">خدمات التخليص والنقل</p>
                <hr style="border: 1px solid #1E3A8A;">
                <table style="width: 100%; font-size: 18px; border-spacing: 10px;">
                    <tr><td style="width: 40%;"><b>التاريخ:</b></td><td>{date_in}</td></tr>
                    <tr><td><b>اسم المستورد:</b></td><td>{importer}</td></tr>
                    <tr><td><b>اسم السائق:</b></td><td>{driver}</td></tr>
                    <tr><td><b>رقم القاطرة:</b></td><td>{plate}</td></tr>
                    <tr><td><b>عدد الأكياس:</b></td><td>{bags:,} كيس</td></tr>
                </table>
                <div style="margin-top: 20px; padding: 15px; background-color: #F1F5F9; border-radius: 10px; text-align: center; border: 1px solid #CBD5E1;">
                    <h3 style="margin: 0; color: #0F172A;">إجمالي الرسوم: {fees:,.2f} ريال</h3>
                </div>
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #64748B;">تمت المعالجة آلياً عبر نظام مكتب أبو محمد</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 يمكنك تصوير الشاشة (Screenshot) الآن لإرسال الفاتورة.")
            
            # سطر البيانات للنسخ اليدوي لجدول جوجل
            st.write("---")
            st.write("📝 بيانات للنسخ لجدول جوجل (اختياري):")
            st.code(f"{date_in}, {importer}, {driver}, {plate}, {bags}, {fees}", language="text")
        else:
            st.error("⚠️ يرجى تعبئة الحقول الأساسية (المستورد، السائق، اللوحة) لإصدار الفاتورة.")

# --- التبويب الثاني: التقارير ---
with tab2:
    st.subheader("📊 ملخص العمليات الإحصائي")
    if st.button("🔄 تحديث البيانات من جدول جوجل"):
        try:
            # قراءة البيانات
            df = pd.read_csv(csv_url)
            
            if not df.empty:
                # حساب الإحصائيات (تأكد أن الأعمدة في جدولك هي A=0, B=1, C=2, D=3, E=4, F=5)
                # العمود الخامس (E) هو الأكياس، والعمود السادس (F) هو الرسوم
                total_trucks = len(df)
                total_bags = pd.to_numeric(df.iloc[:, 4], errors='coerce').sum()
                total_money = pd.to_numeric(df.iloc[:, 5], errors='coerce').sum()

                # عرض العدادات
                c1, c2, c3 = st.columns(3)
                c1.metric("إجمالي القواطر", f"{total_trucks}")
                c2.metric("إجمالي الأكياس", f"{total_bags:,.0f}")
                c3.metric("إجمالي المبالغ", f"{total_money:,.2f} ريال")

                st.divider()
                st.write("📋 السجل التاريخي الكامل:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("الجدول في جوجل شيت فارغ حالياً.")
        except Exception as e:
            st.error("فشل في جلب البيانات. تأكد من أن جدول جوجل شيت يحتوي على بيانات وأن الرابط صحيح.")
