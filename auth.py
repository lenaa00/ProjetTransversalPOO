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

        # Conteneur principal qui va accueillir les écrans
        self.conteneur = tk.Frame(self)
        self.conteneur.pack(fill="both", expand=True)
        self.conteneur.grid_rowconfigure(0, weight=1)
        self.conteneur.grid_columnconfigure(0, weight=1)

        # Dictionnaire pour stocker les vues
        self.ecrans = {}
        
        for F in (EcranAccueil, EcranInscription):
            ecran = F(self.conteneur, self)
            self.ecrans[F] = ecran
            ecran.grid(row=0, column=0, sticky="nsew")

        # Démarrer sur l'accueil
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

        # Frame central pour aligner login et inscription proprement
        frame_central = tk.Frame(self)
        frame_central.pack(expand=True)

        # --- Section Connexion ---
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

        # --- Section Inscription ---
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
        # Exemple de récupération des données tapées
        user = self.entree_id.get()
        messagebox.showinfo("Connexion", f"Tentative de connexion pour : {user}")


class EcranInscription(tk.Frame):
    """Page de création de compte."""
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        compte_frame = tk.LabelFrame(self, text="Créer un compte sécurisé", font=("Times New Roman", 14, "bold"), padx=30, pady=20)
        compte_frame.pack(expand=True)

        # Utilisation de Grid pour un formulaire bien aligné
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

        # Boutons
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
>>>>>>> 6c0db14b4b377315f7ef75a24d93a867068f6709
