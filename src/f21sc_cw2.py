import Model
import View
import Controller

mdl = Model.Model()
cnt = Controller.Controller(mdl)

if __name__ == "__main__":
    win = View.Window(cnt)
    win.mainloop()
