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
        self.title("Messagerie Sécurisée ")
        self.geometry("800x600")
        self.minsize(600, 500)

       
        self.conteneur = tk.Frame(self)
        self.conteneur.pack(fill="both", expand=True)
        self.conteneur.grid_rowconfigure(0, weight=1)
        self.conteneur.grid_columnconfigure(0, weight=1)

       
        self.ecrans = {}
        
        for F in (EcranAccueil, EcranInscription):
            ecran = F(self.conteneur, self)
            self.ecrans[F] = ecran
            ecran.grid(row=0, column=0, sticky="nsew")

       
        self.afficher_ecran(EcranAccueil)

    def afficher_ecran(self, page_class):
        """Place l'écran demandé au premier plan."""
        ecran = self.ecrans[page_class]
        ecran.tkraise()


class EcranAccueil(tk.Frame):
    """Page de connexion."""
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        tk.Label(self, text="PAGE D'ACCUEIL", font=("Times New Roman", 20, "bold")).pack(pady=40)

        
        frame_central = tk.Frame(self)
        frame_central.pack(expand=True)

        
        login_frame = tk.LabelFrame(frame_central, text="Connexion User", padx=20, pady=20)
        login_frame.pack(side="left", padx=20, fill="y")

        tk.Label(login_frame, text="Identifiant").pack(anchor="w")
        self.entree_id = tk.Entry(login_frame) # Sauvegardé dans self !
        self.entree_id.pack(fill="x", pady=(0, 10))

        tk.Label(login_frame, text="Mot de passe").pack(anchor="w")
        self.entree_mdp = tk.Entry(login_frame, show="*") # Sauvegardé dans self !
        self.entree_mdp.pack(fill="x", pady=(0, 10))

        tk.Label(login_frame, text="Clé Privée").pack(anchor="w")
        tk.Button(login_frame, text="Importer (.pem)", command=self.importer_cle).pack(anchor="w", pady=(0, 20))

        tk.Button(login_frame, text="SE CONNECTER", bg="green", fg="white", command=self.se_connecter).pack(fill="x")

        
        inscription_frame = tk.LabelFrame(frame_central, text="Nouveau ?", padx=20, pady=20)
        inscription_frame.pack(side="left", padx=20, fill="y")

        tk.Label(inscription_frame, text="Pas encore de compte ?\nRejoignez le réseau.", justify="center").pack(pady=30)
        tk.Button(inscription_frame, text="Créer un compte", font=("Times New Roman", 12),
                  command=lambda: controleur.afficher_ecran(EcranInscription)).pack(pady=10)

    def importer_cle(self):
        """Ouvre un explorateur pour choisir le fichier de clé."""
        fichier = filedialog.askopenfilename(title="Sélectionner la clé privée")
        if fichier:
            messagebox.showinfo("Succès", f"Clé importée :\n{fichier}")

    def se_connecter(self):
        
        user = self.entree_id.get()
        messagebox.showinfo("Connexion", f"Tentative de connexion pour : {user}")


class EcranInscription(tk.Frame):
    """Page de création de compte."""
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        compte_frame = tk.LabelFrame(self, text="Créer un compte sécurisé", font=("Times New Roman", 14, "bold"), padx=30, pady=20)
        compte_frame.pack(expand=True)

       
        tk.Label(compte_frame, text="Clé Publique").grid(row=0, column=0, sticky="w", pady=5)
        self.entree_cle_pub = tk.Entry(compte_frame, width=30)
        self.entree_cle_pub.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(compte_frame, text="Importer", font=("Times New Roman", 8)).grid(row=0, column=2, pady=5)

        tk.Label(compte_frame, text="Nom Complet").grid(row=1, column=0, sticky="w", pady=5)
        self.entree_nom = tk.Entry(compte_frame, width=30)
        self.entree_nom.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(compte_frame, text="Identifiant unique").grid(row=2, column=0, sticky="w", pady=5)
        self.entree_id = tk.Entry(compte_frame, width=30)
        self.entree_id.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(compte_frame, text="Mot de passe robuste").grid(row=3, column=0, sticky="w", pady=5)
        self.entree_mdp = tk.Entry(compte_frame, show="*", width=30)
        self.entree_mdp.grid(row=3, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        
        tk.Label(compte_frame, text="(- 8 car, Maj, Point...)", font=("Times New Roman", 8, "italic")).grid(row=4, column=1, sticky="w")

        tk.Label(compte_frame, text="Confirmer le mdp").grid(row=5, column=0, sticky="w", pady=5)
        self.entree_mdp_conf = tk.Entry(compte_frame, show="*", width=30)
        self.entree_mdp_conf.grid(row=5, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        
        frame_btns = tk.Frame(compte_frame)
        frame_btns.grid(row=6, column=0, columnspan=3, pady=20)
        
        tk.Button(frame_btns, text="Annuler", command=lambda: controleur.afficher_ecran(EcranAccueil)).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Création du compte", bg="black", fg="white", command=self.finaliser_inscription).pack(side="left", padx=10)

    def finaliser_inscription(self):
        mdp1 = self.entree_mdp.get()
        mdp2 = self.entree_mdp_conf.get()
        
        if mdp1 != mdp2:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        messagebox.showinfo("Succès", "Compte créé ! Retour à l'accueil.")
        self.controleur.afficher_ecran(EcranAccueil)

if __name__ == "__main__":
    app = ApplicationMessagerie()
    app.mainloop()