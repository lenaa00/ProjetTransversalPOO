import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rsafe",
    )
    return conn

class ApplicationMessagerie(tk.Tk):
    """Contrôleur principal de l'application."""
    def __init__(self):
        super().__init__()
        self.title("Messagerie Sécurisée")
        self.geometry("800x600")
        self.minsize(600, 500)

        # Remplacement de 'conteneur' par 'fenetre'
        self.fenetre = tk.Frame(self)
        self.fenetre.pack(fill="both", expand=True)
        self.fenetre.grid_rowconfigure(0, weight=1)
        self.fenetre.grid_columnconfigure(0, weight=1)

        self.ecrans = {}
        
        # Remplacement par tes anciens noms de pages
        for F in (PageAccueil, PageInscription):
            ecran = F(self.fenetre, self)
            self.ecrans[F] = ecran
            ecran.grid(row=0, column=0, sticky="nsew")

        self.afficher_accueil()

    def afficher_accueil(self):
        """Remet ta fonction afficher_accueil d'origine"""
        ecran = self.ecrans[PageAccueil]
        ecran.tkraise()

    def afficher_inscription(self):
        """Remet ta fonction afficher_inscription d'origine"""
        ecran = self.ecrans[PageInscription]
        ecran.tkraise()


class PageAccueil(tk.Frame):
    """Page de connexion."""
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        tk.Label(self, text="PAGE D'ACCUEIL", font=("Times New Roman", 20, "bold")).pack(pady=40)

        frame_central = tk.Frame(self)
        frame_central.pack(expand=True)

        # Remplacement par 'self.login'
        self.login = tk.LabelFrame(frame_central, text="Connexion User", padx=20, pady=20)
        self.login.pack(side="left", padx=20, fill="y")

        tk.Label(self.login, text="Identifiant").pack(anchor="w")
        self.entree_id = tk.Entry(self.login) 
        self.entree_id.pack(fill="x", pady=(0, 10))

        tk.Label(self.login, text="Mot de passe").pack(anchor="w")
        self.entree_mdp = tk.Entry(self.login, show="*") 
        self.entree_mdp.pack(fill="x", pady=(0, 10))

        tk.Label(self.login, text="Clé Privée").pack(anchor="w")
        tk.Button(self.login, text="importer", command=self.importer_cle).pack(anchor="w", pady=(0, 20))

        tk.Button(self.login, text="SE CONNECTER", bg="green", fg="white", command=self.se_connecter).pack(fill="x")

        # Remplacement par 'self.inscription'
        self.inscription = tk.LabelFrame(frame_central, text="Nouveau ?", padx=20, pady=20)
        self.inscription.pack(side="left", padx=20, fill="y")

        tk.Label(self.inscription, text="Pas encore de compte ?\nRejoignez le réseau.", justify="center").pack(pady=30)
        tk.Button(self.inscription, text="Créer un compte", font=("Times New Roman", 12),
                  command=self.controleur.afficher_inscription).pack(pady=10)

    def importer_cle(self):
        fichier = filedialog.askopenfilename(title="Sélectionner la clé privée")
        if fichier:
            messagebox.showinfo("Succès", f"Clé importée :\n{fichier}")

    def se_connecter(self):
        user = self.entree_id.get()
        messagebox.showinfo("Connexion", f"Tentative de connexion pour : {user}")


class PageInscription(tk.Frame):
    """Page de création de compte."""
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        # Remplacement par 'self.compte'
        self.compte = tk.LabelFrame(self, text="Créer un compte sécurisé", font=("Times New Roman", 14, "bold"), padx=30, pady=20)
        self.compte.pack(expand=True)

        tk.Label(self.compte, text="Clé Publique").grid(row=0, column=0, sticky="w", pady=5)
        self.entree_cle_pub = tk.Entry(self.compte, width=30)
        self.entree_cle_pub.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.compte, text="importer", font=("Times New Roman", 8)).grid(row=0, column=2, pady=5)

        tk.Label(self.compte, text="Nom Complet").grid(row=1, column=0, sticky="w", pady=5)
        self.entree_nom = tk.Entry(self.compte, width=30)
        self.entree_nom.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(self.compte, text="Identifiant unique").grid(row=2, column=0, sticky="w", pady=5)
        self.entree_id = tk.Entry(self.compte, width=30)
        self.entree_id.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(self.compte, text="Mot de passe robuste").grid(row=3, column=0, sticky="w", pady=5)
        self.entree_mdp = tk.Entry(self.compte, show="*", width=30)
        self.entree_mdp.grid(row=3, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        
        tk.Label(self.compte, text="- 8 car\n- Maj\n- Point...", font=("Times New Roman", 8), justify="left").grid(row=4, column=1, sticky="w")

        tk.Label(self.compte, text="Confirmer le mdp").grid(row=5, column=0, sticky="w", pady=5)
        self.entree_mdp_conf = tk.Entry(self.compte, show="*", width=30)
        self.entree_mdp_conf.grid(row=5, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        frame_btns = tk.Frame(self.compte)
        frame_btns.grid(row=6, column=0, columnspan=3, pady=20)
        
        tk.Button(frame_btns, text="Annuler", command=self.controleur.afficher_accueil).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Création du compte", bg="black", fg="white", command=self.finaliser_inscription).pack(side="left", padx=10)

    def finaliser_inscription(self):
        mdp1 = self.entree_mdp.get()
        mdp2 = self.entree_mdp_conf.get()
        
        if mdp1 != mdp2:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        messagebox.showinfo("Succès", "Compte créé ! Retour à l'accueil.")
        self.controleur.afficher_accueil()

if __name__ == "__main__":
    accueil = ApplicationMessagerie() # Reprend ton nom d'instance "accueil"
    accueil.mainloop()