[Worked fine with Python3.8]

The document clamTheme.txt is naturally located:
C:\Users\marin\AppData\Local\Programs\Python\Python38\tcl\tk8.6\ttk\

----------------------------------------------------------------------------------------------------------------------------
To force that code: 

/.../
style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview', rowheight=90, font=('Helvetica', 11))
/../

records = self.db.getAllRecords()
        tag = "COLOR"
        for index, record in enumerate(records):
            if (index != 0):
                tag = "NOCOLOR"
            self.tableWithResults.insert("", "end", values=record, tags=tag)
            #self.tableWithResults.insert("", "end", values=record)
        self.tableWithResults.tag_configure('COLOR', background='lightpink')

----------------------------------------------------------------------------------------------------------------------------

to be working (especially last one row) need to replace data in file clamTheme.txt with
clamTheme.txt in directory of VKR: S:\VKR_FILES (or another one)

----------------------------------------------------------------------------------------------------------------------------
Text to be change:

	ttk::style map Treeview \
	    -background [list disabled $colors(-frame)\
				{!disabled !selected} $colors(-window) \
				selected $colors(-selectbg)] \
	    -foreground [list disabled $colors(-disabledfg) \
				{!disabled !selected} black \
				selected $colors(-selectfg)]

----------------------------------------------------------------------------------------------------------------------------