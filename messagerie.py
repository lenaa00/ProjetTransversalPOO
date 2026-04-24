import tkinter as tk
from tkinter import messagebox

class PageConversation(tk.Frame):
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        frame_contacts = tk.Frame(self, bg="#d9d9d9", relief="sunken", borderwidth=2)
        frame_contacts.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame_contacts, text="Conversations", bg="#d9d9d9", font=("Times New Roman", 14, "bold")).pack(pady=10)
        
        self.liste_contacts = tk.Listbox(frame_contacts, font=("Times New Roman", 12))
        self.liste_contacts.pack(fill="both", expand=True, padx=10, pady=10)
        
        for contact in ["Julia", "Dylan", "TechLead"]:
            self.liste_contacts.insert(tk.END, contact)

        tk.Button(frame_contacts, text="Déconnexion", command=self.deconnexion).pack(pady=10, padx=10, fill="x")

        frame_chat = tk.Frame(self)
        frame_chat.grid(row=0, column=1, sticky="nsew")
        frame_chat.grid_rowconfigure(0, weight=1) 
        frame_chat.grid_columnconfigure(0, weight=1)

        self.historique = tk.Text(frame_chat, state='disabled', wrap="word", font=("Times New Roman", 12))
        self.historique.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.entree_message = tk.Entry(frame_chat, font=("Times New Roman", 12))
        self.entree_message.grid(row=1, column=0, sticky="ew", padx=(10, 0), pady=10, ipady=8)
        
        self.entree_message.bind("<Return>", lambda event: self.envoyer_message())

        tk.Button(frame_chat, text="Envoyer 🔒", bg="green", fg="white", font=("Times New Roman", 12, "bold"), 
                  command=self.envoyer_message).grid(row=1, column=1, padx=10, pady=10)

    def envoyer_message(self):
        texte = self.entree_message.get().strip()
        
        if not texte: 
            return 

        self.historique.config(state='normal')
        self.historique.insert(tk.END, f"Moi: {texte}\n")
        self.historique.config(state='disabled')
        
        self.entree_message.delete(0, tk.END)

    def deconnexion(self):
        messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")
        self.controleur.afficher_accueil()