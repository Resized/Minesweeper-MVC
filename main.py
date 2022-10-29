import tkinter as tk
from controller import Controller
from model import Model
from view import View

if __name__ == '__main__':

    # Initialisation of the data ###################################################
    model = Model()

    view = View()
    controller = Controller(model, view)
    view.set_controller(controller)

    # Creation of the GUI ##########################################################
    window = view.create_main_window()

    tk.mainloop()
