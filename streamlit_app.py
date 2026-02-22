import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="مكتب أبو محمد للتخليص", layout="wide")

# رابط الجدول الخاص بك (للقراءة)
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- وظيفة جلب البيانات للتعبئة الآلية ---
@st.cache_data(ttl=60) # تحديث الذاكرة كل دقيقة
def get_drivers_data():
    try:
        df = pd.read_csv(csv_url)
        # الاحتفاظ بآخر بيانات مسجلة لكل سائق
        drivers_db = df.drop_duplicates(subset=['السائق'], keep='last')
        return drivers_db
    except:
        return pd.DataFrame()

drivers_df = get_drivers_data()

# --- واجهة البرنامج ---
# إضافة الصورة في الأعلى
st.image("https://raw.githubusercontent.com/yusuf23000-ui/app.py-app/main/7569.jpg", use_column_width=True)
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ نظام مكتب أبو محمد للتخليص</h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["📄 إصدار فاتورة ذكية", "📊 التقارير العامة"])

with tab1:
    st.subheader("📝 إدخال معاملة جديدة")
    
    # ميزة التعبئة الآلية: البحث عن السائق
    search_driver = st.selectbox("ابحث عن سائق مسجل (أو اختر 'جديد')", ["جديد"] + list(drivers_df['السائق'].unique()) if not drivers_df.empty else ["جديد"])
    
    # تحديد البيانات الافتراضية إذا كان السائق معروفاً
    default_plate = ""
    default_chassis = ""
    if search_driver != "جديد":
        driver_info = drivers_df[drivers_df['السائق'] == search_driver].iloc[0]
        default_plate = driver_info['اللوحة']
        default_chassis = driver_info['القعادة'] if 'القعادة' in driver_info else ""

    with st.form("invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver_name = st.text_input("اسم السائق", value=search_driver if search_driver != "جديد" else "")
            plate = st.text_input("رقم اللوحة", value=default_plate)
            chassis = st.text_input("رقم القعادة", value=default_chassis)
        with col2:
            manifest_no = st.text_input("رقم البيان")
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("الرسوم (ريال)", min_value=0.0)
            date_val = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("✨ توليد الفاتورة للطباعة")

    if submit:
        if importer and driver_name:
            # تصميم الفاتورة مع الشعار الجديد
            st.markdown(f"""
            <div style="direction: rtl; border: 5px solid #1E3A8A; padding: 30px; border-radius: 20px; background-color: white; color: black; font-family: 'Arial';">
                <div style="text-align: center;">
                    <img src="https://raw.githubusercontent.com/yusuf23000-ui/app.py-app/main/7569.jpg" width="300">
                    <h2 style="color: #1E3A8A; margin-top: 10px;">فاتورة تخليص جمركي</h2>
                </div>
                <hr style="border: 2px solid #1E3A8A;">
                <div style="display: flex; justify-content: space-between; font-size: 18px;">
                    <p><b>التاريخ:</b> {date_val}</p>
                    <p><b>رقم البيان:</b> {manifest_no}</p>
                </div>
                <table style="width: 100%; font-size: 19px; border-collapse: collapse; margin-top: 15px;">
                    <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border: 1px solid #ddd;"><b>المستورد:</b></td><td style="padding: 10px; border: 1px solid #ddd;">{importer}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd;"><b>السائق:</b></td><td style="padding: 10px; border: 1px solid #ddd;">{driver_name}</td></tr>
                    <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border: 1px solid #ddd;"><b>اللوحة / القعادة:</b></td><td style="padding: 10px; border: 1px solid #ddd;">{plate} / {chassis}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd;"><b>الكمية:</b></td><td style="padding: 10px; border: 1px solid #ddd;">{bags:,} كيس</td></tr>
                </table>
                <div style="margin-top: 25px; padding: 20px; background-color: #E0E7FF; border-radius: 15px; text-align: center;">
                    <h2 style="margin: 0; color: #1E3A8A;">إجمالي الرسوم: {fees:,.2f} ريال</h2>
                </div>
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #777;">صادر عن النظام الإلكتروني لمكتب أبو محمد</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ الفاتورة جاهزة. خذ لقطة شاشة.")
            # سطر البيانات المطور للنسخ
            st.write("📋 سطر البيانات المحدث (لصقه في الإكسل):")
            row_data = f"{date_val}, {importer}, {driver_name}, {plate}, {chassis}, {manifest_no}, {bags}, {fees}"
            st.code(row_data, language="text")

with tab2:
    st.subheader("📊 ملخص الحسابات والبيانات المسجلة")
    if st.button("🔄 تحديث"):
        st.cache_data.clear()
        df = pd.read_csv(csv_url)
        st.dataframe(df, use_container_width=True)
