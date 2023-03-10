import PySimpleGUI as sg


def edit_cell(window, key, row, col, justify='left'):

    global textvariable, edit

    def callback(event, row, col, text, key):
        global edit
        # event.widget gives you the same entry widget we created earlier
        widget = event.widget
        if key == 'Focus_Out':
            # Get new text that has been typed into widget
            text = widget.get()
            # Print to terminal
            print(text)
        # Destroy the entry widget
        widget.destroy()
        # Destroy all widgets
        widget.master.destroy()
        # Get the row from the table that was edited
        # table variable exists here because it was called before the callback
        values = list(table.item(row, 'values'))
        # Store new value in the appropriate row and column
        values[col] = text
        table.item(row, values=values)
        edit = False

    if edit or row <= 0:
        return

    edit = True
    # Get the Tkinter functionality for our window
    root = window.TKroot
    # Gets the Widget object from the PySimpleGUI table - a PySimpleGUI table is really
    # what's called a TreeView widget in TKinter
    table = window[key].Widget
    # Get the row as a dict using .item function and get individual value using [col]
    # Get currently selected value
    text = table.item(row, "values")[col]
    # Return x and y position of cell as well as width and height (in TreeView widget)
    x, y, width, height = table.bbox(row, col)

    # Create a new container that acts as container for the editable text input widget
    frame = sg.tk.Frame(root)
    # put frame in same location as selected cell
    frame.place(x=x, y=y, anchor="nw", width=width, height=height)

    # textvariable represents a text value
    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    # Used to acceot single line text input from user - editable text input
    # frame is the parent window, textvariable is the initial value, justify is the position
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    # Organizes widgets into blocks before putting them into the parent
    entry.pack()
    # selects all text in the entry input widget
    entry.select_range(0, sg.tk.END)
    # Puts cursor at end of input text
    entry.icursor(sg.tk.END)
    # Forces focus on the entry widget (actually when the user clicks because this initiates all this Tkinter stuff, e
    # ending with a focus on what has been created)
    entry.focus_force()
    # When you click outside of the selected widget, everything is returned back to normal
    # lambda e generates an empty function, which is turned into an event function
    # which corresponds to the "FocusOut" (clicking outside of the cell) event
    entry.bind("<FocusOut>", lambda e, r=row, c=col, t=text,
               k='Focus_Out': callback(e, r, c, t, k))


def create_table(headings, data):
    print(headings)
    print(data)
    global edit
    edit = False
    table_window_layout = [
        [sg.Table(
            values=data,
            headings=headings,
            display_row_numbers=True,
            max_col_width=35,
            auto_size_columns=True,
            justification='right',
            num_rows=10,
            key='-TABLE-',
            row_height=35,
            tooltip="Table",
            enable_click_events=True,
        )]
    ]

    table_window = sg.Window(
        "Table", table_window_layout, modal=True)

    while True:
        event, values = table_window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif isinstance(event, tuple):
            print("isInstance")
            if isinstance(event[2][0], int) and event[2][0] > -1:
                cell = row, col = event[2]
                print(row)

        # Displays that coordinates of the cell that was clicked on
            edit_cell(table_window, '-TABLE-', row+1, col+1, justify='right')

    table_window.close()
