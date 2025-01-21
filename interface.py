import spotifyapihandler
import tkinter as tk
from tkinter import messagebox

# teljes program keret, tkinter dok
class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
# alap "bejelentkező" felület
    def create_widgets(self):
        # Cím
        self.label_asd = tk.Label(self, text="Bejelentkezés")
        self.label_client_id = tk.Label(self, text="client_id:")
        self.entry_client_id = tk.Entry(self)
        self.label_client_secret = tk.Label(self, text="client_secret:")
        self.entry_client_secret = tk.Entry(self)
        self.submit_button = tk.Button(self, text="Küldés", command=self.submit_form)

        # Form elemek
        self.label_asd.pack(pady=5)
        self.label_client_id.pack(pady=5)
        self.entry_client_id.pack(pady=5)
        self.label_client_secret.pack(pady=5)
        self.entry_client_secret.pack(pady=5)
        self.submit_button.pack(pady=10)

    def create_chooser(self):
        # Gombok új ablakba
        
        self.button1 = tk.Button(self, text="Kedvenc előadók", command=self.button1_action)
        self.button2 = tk.Button(self, text="Kedvenc zenék rövidtávon", command=self.button2_action)
        self.button3 = tk.Button(self, text="Kedvenc zenék középtávon", command=self.button3_action)
        self.button4 = tk.Button(self, text="Kedvenc zenék hosszútávon", command=self.button4_action)

        self.button1.pack(pady=10)
        self.button2.pack(pady=10)
        self.button3.pack(pady=10)
        self.button4.pack(pady=10)

# kedvenc előadók gomb
    def button1_action(self):
        favourites = spotifyapihandler.process_top_artists()
        info_window = tk.Toplevel(self)
        info_window.title = "Kedvenc előadóid:"
        text_widget = tk.Text(info_window, width=100,height=20)
        text_widget.pack(padx=10,pady=10)
        for artist in favourites:
            text_widget.insert(tk.END,f"{artist}\n")
        text_widget.config(state=tk.DISABLED)

        # messagebox.showinfo("Kedvenc előadóid", f"A következők a kedvenc előadóid és azok felkapottsága:\n {favourites} ")
        
# rövidtávon kedvenc zenék gomb
    def button2_action(self):
        tracks = spotifyapihandler.process_top_songs_short()
        info_window = tk.Toplevel(self)
        info_window.title = "Kedvenc zenéid rövid időintervallumban"
        text_widget = tk.Text(info_window, width=100,height=40)
        text_widget.pack(padx=10,pady=10)
        for track in tracks:
                text_widget.insert(tk.END,f"{track}\n")
        text_widget.config(state=tk.DISABLED)
# középtávon kedvenc zenék
    def button3_action(self):
        tracks = spotifyapihandler.process_top_songs_medium()
        info_window = tk.Toplevel(self)
        info_window.title = "Kedvenc zenéid közepes időintervallumban"
        text_widget = tk.Text(info_window,width=100,height=40)
        text_widget.pack(padx=20,pady=20)
        for track in tracks:
                text_widget.insert(tk.END,f"{track}\n")
        text_widget.config(state=tk.DISABLED)
#hosszútávon kedvenc zenék gomb
    def button4_action(self):
        tracks= spotifyapihandler.process_top_songs_long()
        info_window = tk.Toplevel(self)
        info_window.title ="Kedvenc zenék hosszú időintervallumban"
        text_widget = tk.Text(info_window,width=100,height=40)
        text_widget.pack(padx=20,pady=20)
        for track in tracks:
            text_widget.insert(tk.END,f"{track}\n")
        text_widget.config(state=tk.DISABLED) # módosítás titlás

    def submit_form(self):
        # A form beküldése
        client_id = self.entry_client_id.get()
        client_secret = self.entry_client_secret.get()
        if spotifyapihandler.importdatas(client_id,client_secret) == False: # Jelenleg csak az enyémmel működik
            messagebox.showinfo("HIBA","Rosszul megadott credentialok, próbálj újra")
            root.quit()
        else:
            messagebox.showinfo("SIKERES BEJELENTKEZÉS",f"Sikeres bejelentkezés a következő accountodba:\n{spotifyapihandler.process_user_profile()}")
            self.clear_widgets()  # Az előző form eltüntetése
            self.create_chooser()  # Új gombok megjelenítése
    
    def show_message(self):
        # Csak egy egyszerű szöveg megjelenítése
        self.message_label = tk.Label(self, text="Adatok sikeresen beküldve")
        self.message_label.pack(pady=20)
    
    
    def clear_widgets(self):
        # Minden widget eltüntetése
        for widget in self.winfo_children():
            widget.destroy()

# Alkalmazás elindítása
root = tk.Tk()
root.title("Szimpla Form és Menü")
root.geometry("300x250")
app = App(master=root)
app.mainloop()
