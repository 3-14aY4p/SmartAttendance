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

contentCam = ctk.CTkFrame(root,width=540,height=400,corner_radius=20,fg_color="#FCAF58")
contentCam.place(x=330, y=110)
contentCam.grid_propagate(False)

contentStat = ctk.CTkFrame(root,width=540,height=140,corner_radius=20,fg_color="#FCAF58")
contentStat.place(x=330, y=530)
contentStat.grid_propagate(False)

contentIDPreview =  ctk.CTkFrame(root,width=300,height=560,corner_radius=20,fg_color="#FCAF58")
contentIDPreview.place(x=900, y=110)
contentIDPreview.grid_propagate(False)

contentIDPreview_Text = ctk.CTkLabel(contentIDPreview, text="ID PREVIEW",font=("Roboto",32), text_color="#000000", anchor="w")
contentIDPreview_Text.grid(row=0, column=0, padx=20, pady=(20,0),sticky="w")

root.mainloop()