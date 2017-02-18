from tkinter import *
import json
import datetime

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()

        def template_load(selected):
            if selected != "Workout":
                templates_dict = {
                    "A": ["Back Squat", "Bench Press", "Bent Over Row", "Curls", "Hyperextensions", "Cable Crunches"],
                    "B": ["Back Squat", "Deadlift", "Overhead Press", "Chest Fly", "Dips", "Lateral Raises"]
                }
                workout = templates_dict[selected]
                for x in range(0,6):
                    self.ex_labs[x]['text']=workout[x]
                frame.update()

        #date label
        self.date_label = Label(frame, text="Enter date: ")
        self.date_label.grid(row=0,column=0,sticky='e')
        #date input
        self.date = StringVar()
        self.date_input = Entry(frame,textvariable=self.date)
        self.date_input.grid(row=0,column=1,columnspan=6,sticky='w')
        #workout option
        self.options = ("A","B")
        self.workout_select = StringVar()
        self.workout_select.set("Workout")
        self.option = OptionMenu(frame, self.workout_select,*self.options,command=lambda name=self.workout_select: template_load(name)) #on change, load template
        self.option.grid(row=1, column=0)


    #Header Labels
        self.ex_label = Label(frame,text="Exercise")
        self.ex_label.grid(row=2,column=0)
        set_labs = []
        wtxrps_labs = []
        self.ex_labs = []
        self.wtxrps_entries = []
        cols = [1, 3, 5, 7, 9]
        # exercise labels
        for i in range(1, 7):
            cur_var = StringVar()
            cur_var.set("")
            cur_lab = Label(frame, text=cur_var.get())
            cur_lab.grid(row=2 + i, column=0)
            self.ex_labs.append(cur_lab)
        for i in range(1,6):
            # SET LABELS
            cur_set = Label(frame, text="Set" + str(i))
            cur_set.grid(row=1, column=cols[i - 1], columnspan=2)
            set_labs.append(cur_set)
            # WEIGHTxREPS labels
            cur_wt = Label(frame, text="Weight")
            cur_wt.grid(row=2, column=cols[i - 1])
            cur_rps = Label(frame, text="Reps")
            cur_rps.grid(row=2, column=cols[i - 1] + 1)
            wtxrps_labs.append([cur_wt, cur_rps])

        for rown,lift in enumerate(self.ex_labs):
            #entries
            col_entries = []
            for coln in range(1,6):
                wt_in = DoubleVar()
                wt_entry = Entry(frame,textvariable=wt_in)
                wt_entry.grid(row=3+rown,column=cols[coln-1],columnspan=1)
                wt_entry.config(width=5)
                rep_in = DoubleVar()
                rep_entry = Entry(frame,textvariable=rep_in)
                rep_entry.grid(row=3+rown,column=cols[coln-1]+1,columnspan=1)
                rep_entry.config(width=5)
                col_entries.append({"set"+str(coln):(wt_in,rep_in)})

            self.wtxrps_entries.append({lift:col_entries})

        # Add exercise
        self.qrow = 10
        self.added_entries = []
        def addrow():
            print("Add row")
            new_ex_entry = Entry(frame)
            new_ex_entry.grid(row=self.qrow,column=0)

            new_cols = []
            for coln in range(1,6):
                wt_in = DoubleVar()
                wt_entry = Entry(frame,textvariable=wt_in)
                wt_entry.grid(row=self.qrow,column=cols[coln-1],columnspan=1)
                wt_entry.config(width=5)
                rep_in = DoubleVar()
                rep_entry = Entry(frame,textvariable=rep_in)
                rep_entry.grid(row=self.qrow,column=cols[coln-1]+1,columnspan=1)
                rep_entry.config(width=5)
                new_cols.append({"set"+str(coln):(wt_in,rep_in)})

            self.added_entries.append({new_ex_entry:new_cols})



            self.qrow = self.qrow + 1

            self.addrow_btn.grid_forget()
            self.msg_box.grid_forget()
            self.enter_btn.grid_forget()
            self.quit_btn.grid_forget()

            create_footer()



        def create_footer():
            self.addrow_btn = Button(frame,text="Add Exercise",command=addrow)
            self.addrow_btn.grid(row=self.qrow, column=0, columnspan=1)


            #System message placeholder
            self.sys_msg = StringVar()
            self.msg_box = Label(frame,text=self.sys_msg.get())
            self.msg_box.grid(row=self.qrow+1,column=1,columnspan=9)

            ####SUBMIT
            self.enter_btn = Button(frame, text="Submit", fg="blue", command=submit_entries)
            self.enter_btn.grid(row=self.qrow + 1, column=0, columnspan=1, sticky='w')

            ####QUIT BUTTON
            self.quit_btn = Button(frame, text="QUIT", fg="red", command=frame.quit)
            self.quit_btn.grid(row=self.qrow + 1, column=10, columnspan=4)

        #Submit entries to JSON
        def submit_entries():
            if not self.ex_labs[0]['text']:
                self.msg_box['text']='ERROR: you must select a workout!'
            else:
                try:
                    for row in self.added_entries:
                        self.wtxrps_entries.append(row)

                    data = {}
                    excs = {}
                    for row in self.wtxrps_entries:
                        print(row)
                        for lift,sets in row.items():
                            if not lift['text']:
                                lift = lift.get()
                            else:
                                lift = lift['text']
                            print(lift)
                            sets_get = {}
                            for set in sets:
                                for setnum, vals in set.items():
                                    sets_get[setnum]=(vals[0].get(),vals[1].get())
                            excs[lift]=sets_get
                    data[self.date.get()]=excs
                    with open("{}.json".format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')), 'w') as data_file:
                        json.dump(data, data_file, indent=4)
                except:
                    self.msg_box['text'] =("Unexpected error:",sys.exc_info()[0],sys.exc_info()[1])
                    raise

        #initialize footer
        create_footer()

################################
'''#######  RUN APP  ########'''
################################
root = Tk()
app = App(root)
root.mainloop()
root.destroy()
