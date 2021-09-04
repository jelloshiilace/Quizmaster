from tkinter import *
import csv
import random



#FUNCTIONS/COMMANDS



def rules(): #clear frame, display rules
    f1.grid(row=4, columnspan=5)
    
    for widget in f1.winfo_children():
        widget.destroy()
        
    Rules='''
WELCOME TO QUIZMASTER!!!

ALL YOU NEED TO DO IS ANSWER 10 MULTIPLE CHOICE QUESTOIONS!!

YOU CAN CLICK 'QUIT' TO EXIT

OTHERWISE, YOUR SCORE WILL BE DISPLAYED AT THE END

GOOD LUCK!!!
'''
    
    r= Label(f1,
             text=Rules,
             width=112,
             height=15,
             bg="black",
             fg="white",
             font="none 10 bold")
    r.pack()
    
def score():
    
    #calculate score
    score=0
    for i in range(10):
        if useranswers[i]==answers[i]:
            score+=1
            
    #display score
    for widget in f1.winfo_children(): #clear frame
        widget.destroy()
    result = "Your score is "+ str(score)+ "/10"
    s= Label(f1,
             text=result,
             width=90,
             pady=10,
             bg="black",
             fg="white",
             font="helvetica 12 bold")
    s.pack()
    
    #display highscore
    highscore=0
    with open("highscore.txt", "r") as obj:
        for line in obj.readline():
            if score >= int(line):
                highscore = score
            else:
                highscore = line
    obj.close()
    with open("highscore.txt", "w") as obj2:
        obj2.write(str(highscore))
    obj2.close()
    
    hs = "Your highscore is " + str(highscore)
    h= Label(f1,
             text=hs,
             width=90,
             pady=10,
             bg="black",
             fg="white",
             font="helvetica 10 bold")
    h.pack()
    
    #spacer:
    Label(f1, text="", bg="black").pack()
    
    #display correct answers
    Label(f1,
          text="CORRECT ANSWERS:",
          bg="black",
          fg="white",
          font="none 12 bold").pack()
    
    #spacer:
    Label(f1, text="", bg="black").pack()
    
    #scrollable frame for correct answers
    container = Frame(f1,
                      width=890,
                      height=100,
                      bg="black",
                      borderwidth=0,
                      highlightthickness=0)
    canvas = Canvas(container,
                    width=890,
                    height=100,
                    bg="black",
                    borderwidth=0,
                    highlightthickness=0)
    scrollbar = Scrollbar(container,
                          orient="vertical",
                          command=canvas.yview)
    scrollable_frame = Frame(canvas)
    
    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=(0,0,250,250)))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    for i in range(10):
        text= "Q" + str(i+1) + ". " + questions[i].lower().capitalize() + " - " + answers[i]
        Label(scrollable_frame,
              text=text,
              bg="black",
              fg="white",
              width=110,
              font="none 10 bold").pack(fill="both", expand=True)
        
    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
     
def confirmanswer(): #add options selected to the useranswer list
    useranswers[qno-1]= str(v.get())
    
def display_ques(qno): #question+options
    
    #question label
    q = Label(f1,
              text=questions[qno],
              width=90,
              bg="black",
              fg="white",
              pady=10,
              font="none 12 bold")
    q.pack()

    #options radiobuttons
    global v
    v = StringVar()
    v.set(str(useranswers[qno]))
    for i in options[qno] :
        button= Radiobutton(f1,
                            text = i,
                            variable = v,
                            value = i,
                            command=confirmanswer,
                            pady=3,
                            padx=3,
                            font="helvetica 10 bold",
                            bg="black",
                            fg="white",
                            relief="sunken",
                            indicatoron=0,
                            selectcolor="grey",
                            width=25)
        button.pack()
        
    #spacer:
    Label(f1, text="", bg="black").pack()

def nextbutton(qno):
    if qno==10: #display view score button
        button = Button(f1,
                        text="VIEW SCORE",
                        command=score,
                        pady=3,
                        padx=3,
                        font="helvetica 10 bold",
                        bg="black",
                        fg="white",
                        relief="sunken")
        button.pack(side=BOTTOM)
        return
    else: #display next button
        button = Button(f1,
                        text="NEXT",
                        command= quiz,
                        pady=3,
                        padx=3,
                        font="helvetica 10 bold",
                        bg="black",
                        fg="white",
                        relief="sunken")
        button.pack(side=BOTTOM)

def skiptoques(): #update question number, jump to question
    global qno
    qno= int(w.get())
    quiz()
    
def questionbar():
    f2=Frame(f1)
    f2.pack()
    global w
    w= IntVar()
    w.set(qno)
    for i in range(10):
        button = Radiobutton(f2,
                            text = str(i+1),
                            variable = w,
                            value = i,
                            command = skiptoques,
                            pady=3,
                            padx=3,
                            font="helvetica 10 bold",
                            bg="black",
                            fg="white",
                            relief="sunken",
                            indicatoron=0,
                            selectcolor="grey",
                            width=5)
        button.grid(row=1, column=i)

def quiz():
    f1.grid(row=4, columnspan=5)
    
    for widget in f1.winfo_children(): #clear frame
        widget.destroy()

    questionbar() #display questionbar on top
    
    global qno
    
    display_ques(qno) #questions+corresponding options

    qno+=1

    nextbutton(qno) #next/viewscore button

def initiate(): #generate question, option, answer list; make useranswer list, set qno=0
    
    global questions, options, answers, useranswers, qno, name
    
    qno=0
    questions = []
    options = []
    answers = []
    useranswers = []
    
    ques_nos = tuple(random.sample(range(1, 35), 10))

    with open("questions.csv", "r") as file:
        csvreader = csv.reader(file)
        
        temp_list=[row for idx, row in enumerate(csvreader) if idx in ques_nos]
        
        for i in temp_list:
            questions.append(i[0])
            options.append(random.sample(i[1:5], len(i[1:5])))
            answers.append(i[5])
            useranswers.append("")
    file.close()
    
    quiz()




#WIDGETS




#window
root= Tk()
root.configure(bg="black")
root.maxsize(width=1000, height=500)
root.minsize(width=1000, height=500)

#banner
banner=PhotoImage(file="banner.gif")
Banner=Label(root,
             image=banner,
             height=100)
Banner.grid(row=0, column=0, columnspan=5)

#spacer
Label(root, text="", bg="black").grid(row=1)

#buttons

#rules
b1=Button(root,
          text="RULES",
          command=rules,
          pady=10,
          padx=10,
          font="helvetica 20 bold",
          bg="black",
          fg="white",
          relief="sunken",
          width=6)

b1.grid(row=2, column=1, sticky=E)

#play
b2=Button(root,
          text="PLAY",
          command=initiate,
          pady=10,
          padx=10,
          font="helvetica 20 bold",
          bg="black",
          fg="white",
          relief="sunken",
          width=6)
b2.grid(row=2, column=2)

#quit
b3= Button(root,
           text="QUIT",
           command= root.destroy,
           pady=10, padx=10,
           font="helvetica 20 bold",
           bg="black",
           fg="white",
           relief="sunken",
           width=6)
b3.grid(row=2, column=3, sticky=W)

#spacer
Label(root, text="", bg="black").grid(row=3)

#base frame
f1= Frame(root,
         width=920,
         height=240,
         bg="black",
         bd=2,
         relief="groove")


root.mainloop()
