import tkinter as tk
from tkinter import messagebox

class ApplicationMessagerie:
    def __init__(self, accueil):
        self.accueil = accueil
        self.accueil.title("Messagerie Sécurisée")
        self.accueil.geometry("1000x600")

        self.fenetre = tk.Frame(self.accueil)
        self.fenetre.pack(fill="both", expand=True)

        self.page_accueil = tk.Frame(self.fenetre)
        self.page_inscription = tk.Frame(self.fenetre)

        self.creer_design_accueil()
        self.creer_design_inscription()

        self.afficher_accueil()

    def afficher_accueil(self):
        self.page_inscription.pack_forget()
        self.page_accueil.pack(fill="both", expand=True) 

    def afficher_inscription(self):
        self.page_accueil.pack_forget() 
        self.page_inscription.pack(fill="both", expand=True) 

    def creer_design_accueil(self):
        tk.Label(self.page_accueil, text="PAGE D'ACCUEIL", font=("Times New Roman", 20, "bold")).pack(pady=20)
        
        self.login = tk.LabelFrame(self.page_accueil, text="Connexion User", padx=10, pady=10)
        self.login.place(x=100, y=100, width=300, height=350)
        tk.Label(self.login, text="Identifiant").pack(anchor="w")
        tk.Entry(self.login).pack(fill="x", pady=5)
        tk.Label(self.login, text="Mot de passe").pack(anchor="w")
        tk.Entry(self.login, show="*").pack(fill="x", pady=5)
        tk.Label(self.login, text="Clé Privée").pack(anchor="w")
        tk.Button(self.login, text="importer").pack(anchor="w")
        tk.Button(self.login, text="SE CONNECTER", bg="green", fg="white").pack(pady=20)

        self.inscription = tk.LabelFrame(self.page_accueil, text="Nouveau ?", padx=10, pady=10)
        self.inscription.place(x=450, y=100, width=400, height=350)
        
        tk.Button(self.inscription, text="Créer un compte", font=("Times New Roman", 12),
                  command=self.afficher_inscription).place(x=100, y=130, width=200, height=50)

    def creer_design_inscription(self):
        self.compte = tk.LabelFrame(self.page_inscription, text="Créer un compte sécurisé", font=("Times New Roman", 14, "bold"), padx=20, pady=20)
        self.compte.place(relx=0.5, rely=0.5, anchor="center", width=400, height=550)

        tk.Label(self.compte, text="Clé Publique").place(x=10, y=10)
        tk.Button(self.compte, text="importer", font=("Times New Roman", 8)).place(x=280, y=8)
        tk.Entry(self.compte).place(x=10, y=35, width=340)

        tk.Label(self.compte, text="Nom Complet").place(x=10, y=75)
        tk.Entry(self.compte).place(x=10, y=100, width=340)

        tk.Label(self.compte, text="Identifiant unique").place(x=10, y=140)
        tk.Entry(self.compte).place(x=10, y=165, width=340)

        tk.Label(self.compte, text="Mot de passe robuste").place(x=10, y=210)
        tk.Label(self.compte, text="- 8 car\n- Maj\n- Point...", font=("Times New Roman", 8), justify="left").place(x=10, y=235)
        tk.Entry(self.compte, show="*").place(x=10, y=280, width=340)

        tk.Label(self.compte, text="Confirmer le mdp").place(x=10, y=330)
        tk.Entry(self.compte, show="*").place(x=10, y=355, width=340)


        tk.Button(self.compte, text="Annuler", command=self.afficher_accueil).place(x=10, y=430, width=120)
        tk.Button(self.compte, text="Création du compte", bg="black", fg="white", 
                  command=self.finaliser_inscription).place(x=180, y=430, width=170)

    def finaliser_inscription(self):
        messagebox.showinfo("Succès", "Compte créé ! Retour à l'accueil.")
        self.afficher_accueil()

if __name__ == "__main__":
    accueil = tk.Tk()
    app = ApplicationMessagerie(accueil)
    accueil.mainloop()