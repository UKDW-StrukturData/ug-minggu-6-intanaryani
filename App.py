import streamlit as st
from DatabaseManager import excelManager

em = excelManager("dataExcel.xlsx")
options = ["Choose Action", "Insert", "Edit", "Delete"]
choice = st.selectbox("Choose an action:", options)

if choice in ("Edit", "Delete"):
    nim = st.text_input("Enter targeted NIM:", key="targetNim")
    saveChange = st.checkbox("SaveChanges", value=False, key="saveChangeEditDelete")
    if choice == "Delete":
        if any(str(i).isalpha() for i in nim):
            st.error("Input nim harus angka semua")
        elif st.button("Delete"):
            if not em.getData("NIM", nim):
                st.error("nim not found")
            else:
                em.deleteData(nim, saveChange)
                if not em.getData("NIM", nim):
                    st.success("deleted")

if choice in ("Insert", "Edit"):
    newNim = st.text_input("Enter New NIM:", key="newNim")
    newName = st.text_input("Enter New Name:", key="newName")
    newGrade = st.text_input("Enter New Grade :", key="newGrade")
    saveChange = st.checkbox("SaveChanges", value=False, key="saveChangeInsertEdit")
    if choice == "Edit":
        if st.button("Edit"):
            if any(str(i).isalpha() for i in newNim):
                st.error("Input nim harus angka semua")
            elif any(str(i).isalpha() for i in newGrade):
                st.error("Input nilai harus angka semua")
            else:
                if not em.getData("NIM", nim):
                    st.error("Nim not found")
                else:
                    result = em.editData(
                        str(nim),
                        {
                            "NIM": str(newNim).strip(),
                            "Nama": str(newName).strip(),
                            "Nilai": int(newGrade.strip()),
                        },
                        saveChange,
                    )
                    if em.getData("NIM", newNim):
                        st.success("edited")
                    else:
                        st.error("edit failed")

    if choice == "Insert":
        if st.button("Insert"):
            if any(str(i).isalpha() for i in newNim):
                st.error("Input nim harus angka semua")
            elif any(str(i).isalpha() for i in newGrade):
                st.error("Input nilai harus angka semua")
            else:
                if em.getData("NIM", newNim):
                    st.error("Nim already exist")
                else:
                    em.insertData(
                        {
                            "NIM": str(newNim).strip(),
                            "Nama": str(newName).strip(),
                            "Nilai": int(newGrade.strip()),
                        },
                        saveChange,
                    )
                    if em.getData("NIM", newNim):
                        st.success("inserted")
                    else:
                        st.error("insert fail")

# Sistem filter data tabel berdasarkan kolom angka
option = ["Default", ">", "<", "=", "<=", ">="]
filterSelectBox = st.selectbox("Sort table by: ", option)

if filterSelectBox == "Default":
    st.table(em.getDataFrame())
else:
    targetFilterColumn = st.selectbox("Target Column", ["NIM", "Nilai"])
    filter_val = st.text_input("Filter Nilai")

    if filter_val != "":
        if not filter_val.isdigit():
            st.error("Filter harus berupa angka")
        else:
            df = em.getDataFrame()
            filter_val_int = int(filter_val)
            if filterSelectBox == ">":
                st.table(df[df[targetFilterColumn] > filter_val_int])
            elif filterSelectBox == "<":
                st.table(df[df[targetFilterColumn] < filter_val_int])
            elif filterSelectBox == "=":
                st.table(df[df[targetFilterColumn] == filter_val_int])
            elif filterSelectBox == "<=":
                st.table(df[df[targetFilterColumn] <= filter_val_int])
            elif filterSelectBox == ">=":
                st.table(df[df[targetFilterColumn] >= filter_val_int])