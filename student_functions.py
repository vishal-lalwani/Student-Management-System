from tkinter import messagebox, filedialog, Toplevel, W, END
import pandas as pd

def export_data(studentTable):
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        newlist.append(content['values'])

    table = pd.DataFrame(newlist, columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data saved successfully')

def add_student(cursor, con, student_data):
    try:
        query = 'INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, student_data)
        con.commit()
        messagebox.showinfo('Success', f'Id {student_data[0]} added successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error adding student: {e}')

def update_student(cursor, con, student_data):
    try:
        query = '''
        UPDATE students SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s 
        WHERE id=%s
        '''
        cursor.execute(query, student_data[1:] + [student_data[0]])
        con.commit()
        messagebox.showinfo('Success', f'Id {student_data[0]} updated successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error updating student: {e}')

def delete_student(cursor, con, student_id):
    try:
        result = messagebox.askyesno('Confirm Delete', f'Do you want to delete Id {student_id}?')
        if result:
            query = 'DELETE FROM students WHERE id=%s'
            cursor.execute(query, (student_id,))
            con.commit()
            messagebox.showinfo('Deleted', f'Id {student_id} deleted successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error deleting student: {e}')

def fetch_all_students(cursor):
    cursor.execute('SELECT * FROM students')
    return cursor.fetchall()
