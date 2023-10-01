import customtkinter
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import PIL.Image
import moviepy.editor as mp

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Setup GUI
app1 = customtkinter.CTk()
#root.geometry('%dx%d+%d+%d' % (w, h, 100, 20))
app1.geometry('%dx%d+%d+%d' % (1150, 650, 190, 200))
app1.title("RESEARCH PROGRAM")
app1.resizable(False, False)
app1.iconbitmap(r'./image/CSb.ico')

app1.grid_columnconfigure(1, weight=1)
app1.grid_columnconfigure((2, 3), weight=0)
app1.grid_rowconfigure((0, 0,0), weight=1)

frame_1 = customtkinter.CTkFrame(master=app1,width=140, corner_radius=0)
frame_1.grid(row=0, column=0, rowspan=4, sticky="nsew")
frame_1.grid_rowconfigure(4, weight=1)


#Name Program
label_Name = customtkinter.CTkLabel(master=frame_1,text="Wall Heat Transfer Calculation Program", font=customtkinter.CTkFont(size=20, weight="bold"))
label_Name.grid(row=0, column=0, padx=26, pady=(20, 10))

#Temperature
label_BoTemp = customtkinter.CTkLabel(master=frame_1,text="Boundary Temperature",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_BoTemp.place(x=20,y=60)

entry_BoTemp = customtkinter.CTkEntry(master=frame_1, placeholder_text="°C")
entry_BoTemp.place(x=220,y=60) 

#Intitial Temp
label_InTemp = customtkinter.CTkLabel(master=frame_1,text="Initial Temperature",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_InTemp.place(x=20,y=100) 

entry_InTemp = customtkinter.CTkEntry(master=frame_1, placeholder_text="°C")
entry_InTemp.place(x=220,y=100) 

#Wall Thickness
label_Wall = customtkinter.CTkLabel(master=frame_1,text="Wall Thickness",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_Wall.place(x=20,y=140) 

entry_Wall = customtkinter.CTkEntry(master=frame_1, placeholder_text= "CM.")
entry_Wall.place(x=220,y=140) 

#K
label_K = customtkinter.CTkLabel(master=frame_1,text="Thermal Conductivity (K)",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_K.place(x=20,y=180) 

entry_K = customtkinter.CTkEntry(master=frame_1, placeholder_text= "W/(m.°C)")
entry_K.place(x=220,y=180) 

#C
label_C = customtkinter.CTkLabel(master=frame_1,text="Specific Heat Capacity (c)",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_C.place(x=20,y=220) 

entry_C = customtkinter.CTkEntry(master=frame_1, placeholder_text= "kg/m3")
entry_C.place(x=220,y=220) 

#Lo
label_Lo = customtkinter.CTkLabel(master=frame_1,text="Density (ρ)",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_Lo.place(x=20,y=260) 

entry_Lo = customtkinter.CTkEntry(master=frame_1, placeholder_text= "kJ/(kg. °C")
entry_Lo.place(x=220,y=260) 

#The experimental time
label_T = customtkinter.CTkLabel(master=frame_1,text="The experimental time",font=customtkinter.CTkFont(size=17), justify=customtkinter.LEFT)
label_T.place(x=20,y=300) 

entry_T = customtkinter.CTkEntry(master=frame_1, placeholder_text= "sec.")
entry_T.place(x=220,y=300) 

#Graph
label_G = customtkinter.CTkLabel(master=frame_1,text="Graphical result", font=customtkinter.CTkFont(size=18, weight="bold"))
label_G.place(x=150,y=390) 

label_G = customtkinter.CTkLabel(master=frame_1,text="Fill the time period of each line in the graph",font=customtkinter.CTkFont(size=12))
label_G.place(x=20,y=430)

entry_G = customtkinter.CTkEntry(master=frame_1,width=70 ,placeholder_text= "sec.")
entry_G.place(x=260,y=430)

#Animation
label_A = customtkinter.CTkLabel(master=frame_1,text="Animated result", font=customtkinter.CTkFont(size=18, weight="bold"))
label_A.place(x=150,y=500)

#Command ShowLo
def ShowLoInNewwindow():
    
    filename = r'./image/Thermal Conductivity.jpg'
    # setup new window
    new_window = customtkinter.CTkToplevel(app1)
    new_window.title("Thermal Conductivity")
    new_window.geometry('%dx%d+%d+%d' % (700, 500, 1650, 200))
    new_window.resizable(False, False)
    # get image
    image = customtkinter.CTkImage((PIL.Image.open(filename)),size=(700, 500))                             
    # load image
    panel = customtkinter.CTkLabel(new_window,text="", image=image)
    panel.image = image
    panel.pack(fill="both", expand=True)

#CommandCal
def CalGraph():

    length = float(entry_Wall.get())
    plate_length = int(entry_Wall.get())
    max_iter_time = int(entry_T.get())

    KK=float(entry_K.get())
    c=float(entry_C.get())
    p=float(entry_Lo.get())

    alpha = KK/(c*p)
    delta_x = float(length/(plate_length-1))
    delta_t = 1
    gamma = (alpha * delta_t) / (delta_x ** 2)

    if gamma > 0.5 :
        messagebox.showerror("Error Input","The value of Gamma is much higher than 0.5, it is Divergent Sequence.")
    else :
        pass

    # Initialize solution: the grid of u(k, i, j)
    u = np.empty((max_iter_time, plate_length))

    # Initial condition everywhere inside the grid
    u_initial = float(entry_InTemp.get())

    # Boundary conditions
    
    u_left = float(entry_BoTemp.get())

    # Set the initial condition
    u.fill(u_initial)

    # Set the boundary conditions
    u[:, 0] = u_left

    for k in range(0, max_iter_time-1):
        for i in range(1, plate_length-1):       
            u[k + 1, i] = gamma * (u[k][i+1] + u[k][i-1]  - 2*u[k][i]) + u[k][i]
        u[k + 1, plate_length-1] = gamma * (u[k][plate_length-1] + u[k][plate_length-2]  - 2*u[k][plate_length-1]) + u[k][plate_length-1]

    print("Last temp at the last time =",u[max_iter_time-1][plate_length-1])

    x=range(1, plate_length+1)
    #print(x)

    for k in range(0,max_iter_time,(int(entry_G.get())-1)):
        
        y=u[k,:]

        # plotting the points 
        plt.plot(x, y,color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='red', markersize=6)

    
    # naming the x axis
    plt.xlabel(f"The wall cross section")
    # naming the y axis
    plt.ylabel('Temperature (C)')
    
    # giving a title to my graph
    plt.title(f"Heat diffusion through building wall at {int(entry_T.get())} sec.")

    plt.grid()
    
    # function to show the plot
    plt.show()

def CalAniXX():

    length = float(entry_Wall.get())
    plate_length = int(entry_Wall.get())
    max_iter_time = int(int(entry_T.get())+int(1000))

    KK=float(entry_K.get())
    c=float(entry_C.get())
    p=float(entry_Lo.get())

    alpha = KK/(c*p)
    delta_x = float(length/(plate_length-1))
    delta_t = 1
    gamma = (alpha * delta_t) / (delta_x ** 2)

    #gamma = 1
    if gamma > 0.5 :
        messagebox.showerror("Error Input","The value of Gamma is much higher than 0.5, it is Divergent Sequence.")
    else :
        pass

    # Initialize solution: the grid of u(k, i, j)
    u = np.empty((max_iter_time, plate_length))

    # Initial condition everywhere inside the grid
    u_initial = float(entry_InTemp.get())

    # Boundary conditions
    u_left = float(entry_BoTemp.get())

    # Set the initial condition
    u.fill(u_initial)

    # Set the boundary conditions
    u[:, 0] = u_left

    for k in range(0, max_iter_time-1):
        for i in range(1, plate_length-1):       
            u[k + 1, i] = gamma * (u[k][i+1] + u[k][i-1]  - 2*u[k][i]) + u[k][i]
        u[k + 1, plate_length-1] = gamma * (u[k][plate_length-1] + u[k][plate_length-2]  - 2*u[k][plate_length-1]) + u[k][plate_length-1]

    print("Last temp at the last time =",u[max_iter_time-1001][plate_length-1])

    v = np.repeat(u[:, :, np.newaxis], plate_length, axis=2)

    def plotheatmap(u_k, k):
        # Clear the current plot figure
        plt.clf()

        plt.title(f"Temperature at {k} sec.")
        plt.xlabel("Wall Thickness")
        plt.ylabel("Wall Thickness")

        # Transpose u_k (swap x and y axes) for plotting
        u_k_transposed = np.transpose(u_k)

        plt.pcolormesh(u_k_transposed, cmap=plt.cm.jet, vmin=float(u_initial), vmax=float(u_left))
        plt.colorbar()
        return plt

    def animate(k):
        k = k*(100)
        plotheatmap(v[k], k)

    anim = animation.FuncAnimation(plt.figure(), animate, interval=800, frames=max_iter_time, repeat=False)
    anim.save(r'./Animation_result/heat_equation_solution.gif')

def CalAni():
    try:
        CalAniXX()
    except:
        pass

    clip = mp.VideoFileClip(r'./Animation_result/heat_equation_solution.gif')
    clip.write_videofile(r'./Animation_result/heat_equation_solution.mp4')

    def load_Video():
        file_path = r'./Animation_result/heat_equation_solution.mp4'
        if file_path:
            vid_player.load(file_path)
            btn_text.set("Pause")
            vid_player.play()

    load_Video()

#Play_Pause
def play_pause():
    if vid_player.is_paused():
        vid_player.play()
        btn_text.set("Pause")
    else:
        vid_player.pause()
        btn_text.set("Play")

#All Button

button_Lo = customtkinter.CTkButton(master=frame_1,text="Ref.",width=12,height=108, command=ShowLoInNewwindow)
button_Lo.place(x=380,y=180) 

button_CalG = customtkinter.CTkButton(master=frame_1,text="Graph",width=80, command=CalGraph)
button_CalG.place(x=340,y=430) 

button_CalA = customtkinter.CTkButton(master=frame_1,text="Animation",width=80, command=CalAni)
button_CalA.place(x=180,y=540) 

vid_player = TkinterVideo(master=app1,width=250,bg='#000001')
vid_player.grid(row=0, column=1, padx=(20, 20), pady=(20, 20),sticky="nsew") #pass

btn_text = tk.StringVar()
button_pause = customtkinter.CTkButton(master=app1,textvariable=btn_text, command=play_pause)
button_pause.grid(row=2, column=1,pady=(10, 5))
btn_text.set("Pause") 

app1.mainloop()
