import streamlit as st
import pandas as pd
import sqlite3
conn = sqlite3.connect('taxi.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS taxi(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    model TEXT,
    year INTEGER,
    color TEXT,
    taxi_id INTEGER,
    FOREIGN KEY (taxi_id) REFERENCES Doctors(ID))""")
cur.execute("""CREATE TABLE IF NOT EXISTS drivers(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    birth_date TEXT,
    phone_number INTEGER,
    adress TEXT)""")
def add_taxi(name, model, year, color):
    cur.execute("INSERT INTO taxi (Name, model, year, color) VALUES (?, ?, ?, ?)",
              (name, model, year, color))
    conn.commit()
    st.success('taxi added to database!')
def add_drivers(name,birth_date,phone_number,adress):
    cur.execute("INSERT INTO Drivers (Name,Birth_date,Phone_number,adress) VALUES (?, ?, ?, ?)",
              (name,birth_date,phone_number,adress))
    conn.commit()
    st.success('Drivers added to database!')
def update_taxi(ID, name=None, model=None, phone_number=None, color=None):
    update_cols = []
    update_vals = []
    if name is not None:
        update_cols.append('name = ?')
        update_vals.append(name)
    if model is not None:
        update_cols.append('model = ?')
        update_vals.append(model)
    if phone_number is not None:
        update_cols.append('phone_number= ?')
        update_vals.append(phone_number)
    if color is not None:
        update_cols.append('color = ?')
        update_vals.append(color)
    if len(update_cols) == 0:
        st.warning('Please specify at least one field to update')
        return
    update_cols_str = ', '.join(update_cols)
    update_vals.append(ID)
    cur.execute(f"UPDATE taxi SET {update_cols_str} WHERE ID = ?", update_vals)
    conn.commit()
    st.success('taxi information updated')
def view_taxi():
    st.subheader('List of taxi')
    cur.execute("SELECT * FROM taxi")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'name', 'model', 'year', 'color','taxi_id'])
    st.dataframe(df)
def view_drivers():
    st.subheader('List of drivers')
    cur.execute("SELECT * FROM drivers")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'name', 'birth_date', 'phone_number', 'adress'])
    st.dataframe(df)
def delete_drivers(taxi_id):
    cur.execute("DELETE FROM taxi WHERE ID=?", (taxi_id,))
    conn.commit()
    st.success('taxi deleted from database!')
def main():
    st.title('taxi company')
    menu = ['Add taxi', 'View taxi', 'Add driver','View driver']
    choice = st.sidebar.selectbox('Select an option', menu)
    if choice == 'Add taxi':
        st.subheader('Add new taxi')
        Name = st.text_input('Name')
        model= st.text_input('model')
        year = st.text_input('year')
        color = st.selectbox('color', ['green', 'yellow', 'red'])
        if st.button('Add taxi'):
            add_taxi(Name, model, year, color)
    elif choice == 'Add Drivers':
        st.subheader('Add new driver')
        Name = st.text_input('name')
        birth_date = st.text_input('birth_date')
        phone_number = st.text_input('phone_number')
        adress = st.selectbox('adress')
        if st.button('Add Driver'):
            add_drivers (Name, birth_date, phone_number, 'adress')
    elif choice == 'View taxi':
        view_taxi()
        dropbox = ['Delete taxi','Update taxi']
        choices = st.selectbox('Select an option', dropbox)
        if choices == 'Delete taxi':
            st.subheader('Delete taxi')
            taxi_id = st.text_input('taxi ID')
            if st.button('Delete taxi'):
                Delete_taxi (taxi_id)
        elif choices == 'Update taxi':
            taxi_id = st.text_input('taxi ID')
            name = st.text_input('name')
            birth_date= st.text_input('modeli')
            phone_number = st.text_input('year')
            color = st.selectbox('color', ['green', 'yellow', 'red'])
            if st.button('Update taxi'):
                update_taxi(taxi_id, name, model, year, color)
    elif choice == 'View drivers':
        view_drivers()
if __name__ == '__main__':
    main()
conn.commit()
conn.close()