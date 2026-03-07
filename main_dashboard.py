import customtkinter as ctk

root = ctk.CTk()
root.title("Smart Attendance System")
root.geometry("1280x720")
root.configure(fg_color="#EEEEF1")

#header
header = ctk.CTkFrame(root, height=70, corner_radius=0, fg_color="#FFFFFF")
header.pack(fill="x")

headerTitle = ctk.CTkLabel(header, text="Smart Attendance System",font=("Roboto",20), text_color="#000000", anchor="w")
headerTitle.place(x=50,y=20)

#sidebar
sidebar = ctk.CTkFrame(root,width=260,height=560,corner_radius=20,fg_color="#7F90DF")
sidebar.place(x=40, y=110)
sidebar.grid_propagate(False)

dashboardText = ctk.CTkLabel(sidebar,text="Dashboard",font=("Roboto",23), text_color="#000000", anchor="w")
dashboardText.grid(row=0, column=0, padx=40, pady=(30,0),sticky="w")

cameraText = ctk.CTkLabel(sidebar,text="Camera",font=("Roboto",23), text_color="#000000", anchor="w")
cameraText.grid(row=1, column=0, padx=40, pady=(30,0),sticky="w")

viewAttendanceText = ctk.CTkLabel(sidebar,text="View Attendance",font=("Roboto",23), text_color="#000000", anchor="w")
viewAttendanceText.grid(row=2, column=0, padx=40, pady=(30,0),sticky="w")

attendanceListText = ctk.CTkLabel(sidebar,text="Attendance List",font=("Roboto",23), text_color="#000000", anchor="w")
attendanceListText.grid(row=3, column=0, padx=40, pady=(30,0),sticky="w")

#background
contentBG = ctk.CTkFrame(root,width=900,height=560,corner_radius=20,fg_color="#FCAF58")
contentBG.place(x=330, y=110)
contentBG.grid_propagate(False)
contentBG.grid_columnconfigure((0,1,2), weight=0)
contentBG.grid_rowconfigure((0,1,2), weight=0)

#background
contentBG = ctk.CTkFrame(root,width=900,height=560,corner_radius=20,fg_color="#FCAF58")
contentBG.place(x=330, y=110)
contentBG.grid_propagate(False)

contentBG.grid_columnconfigure(0, weight=1)
contentBG.grid_columnconfigure(1, weight=1)
contentBG.grid_columnconfigure(2, weight=1)

contentBG.grid_rowconfigure(0, weight=0)
contentBG.grid_rowconfigure(1, weight=0)
contentBG.grid_rowconfigure(2, weight=1)

inner_x = 30
inner_top = 35
inner_gap = 20
inner_bottom = 30

#top cards
card_width = 250
card_height = 130

#present card
contentPresent = ctk.CTkFrame(contentBG,width=card_width,height=card_height,corner_radius=10,fg_color="#EEEEF1")
contentPresent.grid(row=0,column=0,padx=(inner_x,10),pady=(inner_top,inner_gap))
contentPresent.grid_propagate(False)

textPresent = ctk.CTkLabel(contentPresent,text="Present",font=("Roboto",30), text_color="#000000")
textPresent.grid(row=0, column=0, sticky="w", padx=20, pady=(15,0))

#late card
contentLate = ctk.CTkFrame(contentBG,width=card_width,height=card_height,corner_radius=10,fg_color="#EEEEF1")
contentLate.grid(row=0,column=1,padx=10,pady=(inner_top,inner_gap))
contentLate.grid_propagate(False)

textLate = ctk.CTkLabel(contentLate,text="Late",font=("Roboto",30), text_color="#000000")
textLate.grid(row=0, column=0, sticky="w", padx=20, pady=(15,0))

#absent card
contentAbsent = ctk.CTkFrame(contentBG,width=card_width,height=card_height,corner_radius=10,fg_color="#EEEEF1")
contentAbsent.grid(row=0,column=2,padx=(10,inner_x),pady=(inner_top,inner_gap))
contentAbsent.grid_propagate(False)

textAbsent = ctk.CTkLabel(contentAbsent,text="Absent",font=("Roboto",30), text_color="#000000")
textAbsent.grid(row=0, column=0, sticky="w", padx=20, pady=(15,0))

#middle row
#distribution
contentDistribution = ctk.CTkFrame(contentBG,height=150,corner_radius=10,fg_color="#EEEEF1")
contentDistribution.grid(row=1,column=0,columnspan=2,padx=(inner_x,10),pady=(0,inner_gap),sticky="ew")
contentDistribution.grid_propagate(False)

attendanceDistribution = ctk.CTkLabel(contentDistribution,text="Attendance Distribution",font=("Roboto",22), text_color="#000000")
attendanceDistribution.grid(row=0, column=0, sticky="w", padx=20, pady=(15,0))

#bottom row
#recents
contentRecent = ctk.CTkFrame(contentBG,width=0,height=190,corner_radius=10,fg_color="#EEEEF1")
contentRecent.grid(row=2,column=0,columnspan=2,padx=(inner_x,10),pady=(0,inner_bottom),sticky="nsew")
contentRecent.grid_propagate(False)

recentActivity = ctk.CTkLabel(contentRecent,text="Recent Activity",font=("Roboto",20), text_color="#000000")
recentActivity.grid(row=0, column=0, sticky="w", padx=20, pady=(15,0))

#top student
contentTopStudents = ctk.CTkFrame(contentBG,corner_radius=10,fg_color="#EEEEF1")
contentTopStudents.grid(row=1,column=2,rowspan=2,padx=(10, inner_x),pady=(0, inner_bottom),sticky="nsew")

topPerformingStudents = ctk.CTkLabel(contentTopStudents,text="Top Performing Students",font=("Roboto",16), text_color="#000000")
topPerformingStudents.grid(row=0, column=0, sticky="w", padx=20, pady=(15,0))
root.mainloop()