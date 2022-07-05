from tkinter import Entry, Tk, Label, PhotoImage, Button,Frame

text_index = 0
initial_text = ''
animate_after = None
BG = '#66bfbf'
length = None
list_ = None
dict_ = None


name1 = 'Player1'
name2 = 'Player2'


def items():
    global length, list_, dict_
    length = 0
    list_ = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7),
             (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
    dict_ = {
        '1': (75, 70), '2': (135, 70), '3': (205, 70),
        '4': (75, 135), '5': (135, 135), '6': (205, 135),
        '7': (75, 200), '8': (135, 200), '9': (205, 200)
    }


items()


def winning_window(root,T):
    frame = Frame(root,padx=50,pady=50,bg='#66bfbf')
    frame.place(x=0,y=0)
    Label(frame,text=T, font=('arial', 20, 'normal'), width=10, bg='#66bfbf').grid(
        column=0, row=0, ipadx=20, ipady=50, columnspan=2)
    
    Button(frame,text='Restart', command=lambda: [root.destroy(), twoPlayerWindow()],
           cursor='hand2', bg='Light Cyan', activebackground='#6f6f3f',
           activeforeground='White', border=0.5).grid(column=0, row=1)
    Button(frame,text='Main Menu', command=lambda: [root.destroy(), starting_window()],
           cursor='hand2', bg='Light Cyan', activebackground='#6f6f3f',
           activeforeground='White', border=0.5).grid(column=1, row=1)

    root.mainloop()


def twoPlayerWindow():
    root = Tk()
    root.focus_force()
    root.minsize(width=300, height=300)
    root.maxsize(width=300, height=300)
    root.title('Play Game')
    root.iconbitmap('icon.ico')
    root.config(bg='Light Blue')
    board_img = PhotoImage(master=root, file='Board.png')
    board = Label(master=root, image=board_img, bg=BG)
    board.pack(fill='both', anchor='center', expand=True)

    player_label = Label(text=f'{name1} (X) Chance.',
                         font=('arial', 12, 'bold'), bg=BG)
    player_label.place(x=50, y=10)

    def valueofX(x):   # find the accurate x cordinate.
        if 53 < x < 109:
            return(75)
        elif 120 < x < 178:
            return(135)
        elif 187 < x < 247:
            return(205)

    def findXandY(e, h):
        global dict_, length
        r = False
        x_cor = e.x
        y_cor = e.y
        x = None
        y = None
        if 187 < y_cor < 248:
            y = (200)
            x = valueofX(x_cor)
        elif 127 < y_cor < 178:
            y = (135)
            x = valueofX(x_cor)
        elif 51 < y_cor < 117:
            y = (70)
            x = valueofX(x_cor)
        values = [dict_[a] for a in dict_]
        if x != None and y != None and (x, y) in values:
            length += 1
            Label(text=h, bg='white', font=(
                'arial', 20, 'normal')).place(x=x, y=y)
            for key, value in dict_.items():
                if (x, y) == value:
                    dict_[key] = h
                    r = True
                    break
        return r

    def check():
        global length
        for a in list_:
            text_index = []
            for index in a:
                text_index.append(dict_[str(index)])
            if set(text_index) == {'X'}:
                board.unbind('<Button-1>')
                length = 0
                items()
                root.after(1000,
                lambda :winning_window(root,T=f'{name1} (X) Win.'))
                break
            elif set(text_index) == {'O'}:
                board.unbind('<Button-1>')
                length = 0
                items()
                root.after(1000,lambda:winning_window(root,T=f'{name2} (O) Win.'))
                break
        if length == 9:
            board.unbind('<Button-1>')
            items()
            root.after(1000,lambda:winning_window(root,T='Draw.'))

    def player_1(e):
        if findXandY(e, 'X'):
            player_label.config(text='')
            player_label.config(text=f'{name2} (O) Chance')
            board.unbind('<Button-1>')
            board.bind('<Button-1>', player_2)
            check()

    def player_2(e):
        if findXandY(e, 'O'):
            player_label.config(text='')
            player_label.config(text=f'{name1} (X) Chance')
            board.unbind('<Button-1>')
            board.bind('<Button-1>', player_1)
            check()
    board.bind('<Button-1>', player_1)

    root.mainloop()


def name_window():
    def btn(e=None):
        global name1, name2
        if p1.get() and p2.get():
            name1 = p1.get()
            name2 = p2.get()
            if name1 == name2:
                name1 += '1'
                name2 += '2'
            [r.destroy(), twoPlayerWindow()]
        else:
            pass
    r = Tk()
    r.title('Name')
    r['padx'] = 20
    r['pady'] = 20
    r.minsize(width=270, height=100)
    r.maxsize(width=270, height=100)
    Label(r, text='Player 1 Name: ',).grid(row=0, column=0)
    Label(r, text='Player 2 Name: ').grid(row=1, column=0)
    p1 = Entry(r,)
    p1.focus_force()
    p2 = Entry(r,)
    p1.grid(row=0, column=1)
    p2.grid(row=1, column=1)
    Button(r, text='Ok', bg='#A2D5AB', border=.5, padx=10,
           pady=2, cursor='hand2', command=btn).place(x=100, y=50)
    r.bind('<Return>',btn)

    r.mainloop()


def starting_window():
    global animate_after
    def change_color(value, btn):
        if value:
            btn.config(bg='#3A3845')
        else:
            btn.config(bg='#A2D5AB')

    def animate_text(e=None):
        global animate_after
        total_text = (main_label['text'])

        main_label['text'] = ''

        def a():
            global text_index, initial_text, animate_after
            main_label.unbind('<Enter>')
            try:
                initial_text += total_text[text_index]
                main_label['text'] = initial_text
                text_index = text_index+1
                animate_after = root.after(100, a)
            except IndexError:
                main_label.bind('<Enter>',animate_text)
                text_index = 0
                initial_text = ''
        a()

    root = Tk()
    root.focus_force()
    root.minsize(width=300, height=300)
    root.maxsize(width=300, height=300)
    root.title('Tic-Tac-Toe')
    root.iconbitmap('icon.ico')
    animate_after = root.after(1,lambda:1)
    root.config(pady=2, padx=2, bg='#39AEA9')
    main_label = Label(root, text='Tic-Tac-Toe Game',
                       font=('sacramento', 30, 'underline'), bg='#39AEA9')
    main_label.pack(fill='x', expand=True, anchor='n')
    play_btn = Button(root, text='Play', width=7, bg='#A2D5AB', border=.5, font=(
        'arial', 15, 'normal'), command=lambda: [root.after_cancel(animate_after),root.destroy(), name_window()], cursor='hand2')
    play_btn.place(x=40, y=150)
    quit_btn = Button(root, text='Quit', width=7, bg='#A2D5AB', border=.5, font=(
        'arial', 15, 'normal'), command=lambda :[root.after_cancel(animate_after),root.destroy()], cursor='hand2')
    quit_btn.place(x=180, y=150)
    play_btn.bind('<Enter>', lambda e: change_color(1, play_btn))
    play_btn.bind('<Leave>', lambda e: change_color(0, play_btn))
    quit_btn.bind('<Enter>', lambda e: change_color(1, quit_btn))
    quit_btn.bind('<Leave>', lambda e: change_color(0, quit_btn))
    main_label.bind('<Enter>', lambda e:[root.after(500,animate_text())])
    root.mainloop()

starting_window()
quit()
