import customtkinter as ctk
import cv2
from PIL import Image, ImageTk


# main application window
root = ctk.CTk()
root.title("Smart Attendance System")
root.geometry("1280x720")
root.configure(fg_color="#EEEEF1")


# ---------- HEADER SECTION ----------

# top header container
header = ctk.CTkFrame(root, height=70, corner_radius=0, fg_color="#FFFFFF")
header.pack(fill="x")

# system title in header
headerTitle = ctk.CTkLabel(header, text="Smart Attendance System", font=("Roboto",20), text_color="#000000", anchor="w")
headerTitle.place(x=50, y=20)


# ---------- SIDEBAR NAVIGATION ----------

# floating sidebar panel
sidebar = ctk.CTkFrame(root, width=260, height=560, corner_radius=20, fg_color="#7F90DF")
sidebar.place(x=40, y=110)
sidebar.grid_propagate(False)

# dashboard page
dashboardText = ctk.CTkLabel(sidebar, text="Dashboard", font=("Roboto",23), text_color="#000000", anchor="w")
dashboardText.grid(row=0, column=0, padx=40, pady=(30,0), sticky="w")

# camera page
cameraText = ctk.CTkLabel(sidebar, text="Camera", font=("Roboto",23), text_color="#000000", anchor="w")
cameraText.grid(row=1, column=0, padx=40, pady=(30,0), sticky="w")

# viewing attendance records
viewAttendanceText = ctk.CTkLabel(sidebar, text="View Attendance", font=("Roboto",23), text_color="#000000", anchor="w")
viewAttendanceText.grid(row=2, column=0, padx=40, pady=(30,0), sticky="w")

# complete attendance log
attendanceListText = ctk.CTkLabel(sidebar, text="Attendance List", font=("Roboto",23), text_color="#000000", anchor="w")
attendanceListText.grid(row=3, column=0, padx=40, pady=(30,0), sticky="w")


# ---------- CAMERA DISPLAY PANEL ----------

# live camera preview
contentCam = ctk.CTkFrame(root, width=540, height=400, corner_radius=20, fg_color="#FCAF58")
contentCam.place(x=330, y=110)
contentCam.grid_propagate(False)

# webcam capture
cap = cv2.VideoCapture(0)

 render camera frames inside the UI
cameraLabel = ctk.CTkLabel(contentCam, text="")
cameraLabel.pack(expand=True, fill="both", padx=20, pady=20)


# ---------- STATISTICS PANEL ----------

# container for attendance statistics or system messages
contentStat = ctk.CTkFrame(root, width=540, height=140, corner_radius=20, fg_color="#FCAF58")
contentStat.place(x=330, y=530)
contentStat.grid_propagate(False)


# ---------- ID PREVIEW PANEL ----------

# container used to preview detected student ID information
contentIDPreview = ctk.CTkFrame(root, width=300, height=560, corner_radius=20, fg_color="#FCAF58")
contentIDPreview.place(x=900, y=110)
contentIDPreview.grid_propagate(False)

# label title for ID preview section
contentIDPreview_Text = ctk.CTkLabel(contentIDPreview, text="ID PREVIEW", font=("Roboto",32), text_color="#000000", anchor="w")
contentIDPreview_Text.grid(row=0, column=0, padx=20, pady=(20,0), sticky="w")


# ---------- CAMERA UPDATE LOOP ----------

# continuously capture frames from webcam and display inside UI
def update_camera():
    ret, frame = cap.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # convert OpenCV BGR frame to RGB format

        img = Image.fromarray(frame)                     # convert numpy frame into PIL image
        img = img.resize((560, 400))                     # resize image to fit camera panel

        imgtk = ImageTk.PhotoImage(image=img)            # convert PIL image into tkinter compatible format

        cameraLabel.imgtk = imgtk                        # store reference to prevent garbage collection
        cameraLabel.configure(image=imgtk)               # display frame inside label

    cameraLabel.after(10, update_camera)                 # refresh camera frame every 10 milliseconds


# start the continuous camera update loop
update_camera()


# ---------- WINDOW CLOSE HANDLER ----------

# release webcam when application closes
def on_closing():
    cap.release()
    root.destroy()

# bind window close event to clean up function
root.protocol("WM_DELETE_WINDOW", on_closing)


# start the GUI application loop
root.mainloop()