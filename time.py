import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import sys

while True:
    print("\n=== STUDENT UTILITY MAIN MENU ===")
    print("1. To-Do List")
    print("2. Time Table Generator")
    print("3. Study Tracker")
    print("4. Exit")
    choice = input("Enter choice (1-4): ")

    if choice == '1':
        root = tk.Tk() 
        tasks = []

        def refresh_listbox():
            listbox.delete(0, tk.END)
            for task in tasks:
                display = f"{task['name']} [{task['status']}]"
                listbox.insert(tk.END, display)
                if task['status'] == "Done":
                    listbox.itemconfig(tk.END, {'fg': '#27ae60'})
                else:
                    listbox.itemconfig(tk.END, {'fg': '#e74c3c'})

        def add_task():
            task_text = entry.get()
            if task_text:
                tasks.append({"name": task_text, "status": "Pending"})
                entry.delete(0, tk.END)
                refresh_listbox()
            else:
                messagebox.showwarning("Error", "Please enter a task!")

        def mark_done():
            try:
                index = listbox.curselection()[0]
                tasks[index]["status"] = "Done"
                refresh_listbox()
            except IndexError:
                messagebox.showwarning("Error", "Select a task first!")

        def delete_task():
            try:
                index = listbox.curselection()[0]
                del tasks[index]
                refresh_listbox()
            except IndexError:
                messagebox.showwarning("Error", "Select a task first!")

        root.title("My Colorful To-Do")
        root.geometry("400x500")
        root.configure(bg="#2c3e50")
        entry = tk.Entry(root, width=30, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50")
        entry.pack(pady=20)
        btn_add = tk.Button(root, text="Add Task", command=add_task, bg="#27ae60", fg="white")
        btn_add.pack(pady=5)
        listbox = tk.Listbox(root, width=40, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50")
        listbox.pack(pady=10)
        btn_frame = tk.Frame(root, bg="#2c3e50")
        btn_frame.pack()
        btn_done = tk.Button(btn_frame, text="Mark Done", command=mark_done, bg="#3498db", fg="white")
        btn_done.pack(side=tk.LEFT, padx=5)
        btn_del = tk.Button(btn_frame, text="Delete", command=delete_task, bg="#e74c3c", fg="white")
        btn_del.pack(side=tk.LEFT, padx=5)
        
        root.mainloop() 

    elif choice == '2':
        root = tk.Tk() # 
        root.title("Smart Time Table Generator")
        root.geometry("900x780")
        root.config(bg="lightblue")
        subjects = []
        hours = []

        def add_subject():
            sub = subject_entry.get()
            hr = hour_entry.get()
            if sub == "" or hr == "":
                messagebox.showerror("Error", "Enter subject and hours")
                return
            try: hr = int(hr)
            except:
                messagebox.showerror("Error", "Hours must be number")
                return
            subjects.append(sub)
            hours.append(hr)
            listbox.insert(tk.END, sub + " - " + str(hr) + " hrs")
            subject_entry.delete(0, tk.END)
            hour_entry.delete(0, tk.END)

        def show_time(total_minutes):
            return f"{(total_minutes // 60) % 24:02d}:{total_minutes % 60:02d}"

        def generate_timetable():
            if len(subjects) == 0:
                messagebox.showerror("Error", "Add subjects first")
                return
            name = name_entry.get()
            student_class = class_entry.get()
            if name == "" or student_class == "":
                messagebox.showerror("Error", "Enter student name and class")
                return
            try: break_time = int(break_entry.get())
            except:
                messagebox.showerror("Error", "Enter break time")
                return
            output.delete("1.0", tk.END)
            student_type = option.get()
            data = sorted(list(zip(subjects, hours)), key=lambda x: x[1], reverse=True)
            output.insert(tk.END, "STUDENT TIME TABLE\n=============================\n")
            output.insert(tk.END, f"Name  : {name}\nClass : {student_class}\nType  : {student_type}\n\n")

            if student_type == "Early Bird":
                current = 6 * 60
                long_break_done = False
                for sub, hr in data:
                    start, end = current, current + hr * 60
                    output.insert(tk.END, f"{show_time(start)} - {show_time(end)}   -->   {sub}\n")
                    current = end
                    if current >= 11*60 and not long_break_done:
                        output.insert(tk.END, f"{show_time(current)} - 15:00   -->   Long Break\n\n")
                        current = 15 * 60
                        long_break_done = True
                    else:
                        b_end = current + break_time
                        output.insert(tk.END, f"{show_time(current)} - {show_time(b_end)}   -->   Break\n\n")
                        current = b_end
            else:
                current = 16 * 60
                end_limit = 26 * 60
                dinner_done = False
                remaining = []
                for sub, hr in data:
                    need = hr * 60
                    if current + need > end_limit:
                        remaining.append((sub, hr))
                        continue
                    start, end = current, current + need
                    output.insert(tk.END, f"{show_time(start)} - {show_time(end)}   -->   {sub}\n")
                    current = end
                    if current >= 20*60 and not dinner_done:
                        d_end = current + 60
                        output.insert(tk.END, f"{show_time(current)} - {show_time(d_end)}   -->   Dinner Break\n\n")
                        current = d_end
                        dinner_done = True
                    else:
                        b_end = current + break_time
                        output.insert(tk.END, f"{show_time(current)} - {show_time(b_end)}   -->   Break\n\n")
                        current = b_end
                if remaining:
                    output.insert(tk.END, "\nNEXT DAY MORNING SESSION\n-----------------------------\n")
                    current = 10 * 60
                    lunch_done = False
                    for sub, hr in remaining:
                        start, end = current, current + hr * 60
                        output.insert(tk.END, f"{show_time(start)} - {show_time(end)}   -->   {sub}\n")
                        current = end
                        if current >= 13*60 and not lunch_done:
                            l_end = current + 60
                            output.insert(tk.END, f"{show_time(current)} - {show_time(l_end)}   -->   Lunch Break\n\n")
                            current = l_end
                            lunch_done = True
                        else:
                            b_end = current + break_time
                            output.insert(tk.END, f"{show_time(current)} - {show_time(b_end)}   -->   Break\n\n")
                            current = b_end

        tk.Label(root, text="Smart Time Table Generator", font=("Arial",18,"bold"), bg="lightblue").pack(pady=10)
        frame1 = tk.Frame(root, bg="lightblue")
        frame1.pack()
        tk.Label(frame1, text="Student Name:", bg="lightblue").grid(row=0,column=0,padx=10,pady=5)
        name_entry = tk.Entry(frame1)
        name_entry.grid(row=0,column=1)
        tk.Label(frame1, text="Class:", bg="lightblue").grid(row=1,column=0,padx=10,pady=5)
        class_entry = tk.Entry(frame1)
        class_entry.grid(row=1,column=1)
        frame2 = tk.Frame(root, bg="lightblue")
        frame2.pack(pady=10)
        tk.Label(frame2, text="Subject Name:", bg="lightblue").grid(row=0,column=0,padx=10,pady=5)
        subject_entry = tk.Entry(frame2)
        subject_entry.grid(row=0,column=1)
        tk.Label(frame2, text="Study Hours:", bg="lightblue").grid(row=1,column=0,padx=10,pady=5)
        hour_entry = tk.Entry(frame2)
        hour_entry.grid(row=1,column=1)
        tk.Button(frame2, text="Add Subject", bg="yellow", command=add_subject).grid(row=2,column=0,columnspan=2,pady=10)
        listbox = tk.Listbox(root, width=42, height=6)
        listbox.pack(pady=10)
        option = tk.StringVar(value="Early Bird")
        tk.Label(root, text="Select Student Type:", bg="lightblue").pack()
        tk.OptionMenu(root, option, "Early Bird", "Night Owl").pack(pady=5)
        tk.Label(root, text="Short Break Time (Minutes):", bg="lightblue").pack()
        break_entry = tk.Entry(root)
        break_entry.pack(pady=5)
        tk.Button(root, text="Generate Time Table", bg="orange", command=generate_timetable).pack(pady=10)
        output = tk.Text(root, width=78, height=25)
        output.pack(pady=10)
        
        root.mainloop()

    elif choice == '3':
        def show_graph(spent, goal):
            labels = ['Studied', 'Remaining']
            remaining = max(0, goal - spent)
            plt.figure(figsize=(6, 6))
            plt.pie([spent, remaining], labels=labels, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#FFC107'])
            plt.title('Study Goal Progress')
            plt.show()

        study_hours = 0
        try:
            goal_hours = float(input("Enter your total study goal (hours): "))
        except ValueError:
            goal_hours = 1.0

        while True:
            print("\n--- TRACKER MENU ---")
            print("1. Add Study Duration\n2. View Percentage (Text)\n3. View Visual Progress\n4. Back to Main Menu")
            c = input("Select: ")
            if c == '1':
                try: study_hours += float(input("Enter hours studied: "))
                except: print("Invalid.")
            elif c == '2':
                print(f"\nProgress: {(study_hours / goal_hours) * 100:.2f}% ({study_hours}/{goal_hours} hrs)")
            elif c == '3':
                if study_hours == 0: print("No data yet!")
                else: show_graph(study_hours, goal_hours)
            elif c == '4': break

    elif choice == '4':
        break
    else:
        print("Invalid choice.")