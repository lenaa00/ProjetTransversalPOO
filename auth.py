import tkinter as tk
from tkinter import messagebox, filedialog
from crypto import (
    hash_password_with_salt,
    verify_password,
    encrypt,
    decrypt,
    hash_data,
    add_salt,
    generate_key_pair,  # ✅ AJOUT
)
import mysql.connector
import hashlib, os


def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rsafe",
    )
    return conn


# ✅ AJOUT : sauvegarde locale clé privée
def sauvegarder_cle_privee_local(identifiant: str, cle_privee_pem: bytes):
    dossier = "cles_privees"
    os.makedirs(dossier, exist_ok=True)

    chemin = os.path.join(dossier, f"{identifiant}_private.pem")

    with open(chemin, "wb") as f:
        f.write(cle_privee_pem)

    return chemin


class ApplicationMessagerie(tk.Tk):
    """Contrôleur principal de l'application."""

    def __init__(self):
        super().__init__()
        self.title("Messagerie Sécurisée")
        self.geometry("800x600")
        self.minsize(600, 500)

        self.fenetre = tk.Frame(self)
        self.fenetre.pack(fill="both", expand=True)
        self.fenetre.grid_rowconfigure(0, weight=1)
        self.fenetre.grid_columnconfigure(0, weight=1)

        self.ecrans = {}

        for F in (PageAccueil, PageInscription):
            ecran = F(self.fenetre, self)
            self.ecrans[F] = ecran
            ecran.grid(row=0, column=0, sticky="nsew")

        self.afficher_accueil()

    def afficher_accueil(self):
        ecran = self.ecrans[PageAccueil]
        ecran.tkraise()

    def afficher_inscription(self):
        ecran = self.ecrans[PageInscription]
        ecran.tkraise()


class PageAccueil(tk.Frame):
    """Page de connexion."""

    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        tk.Label(
            self, text="PAGE D'ACCUEIL", font=("Times New Roman", 20, "bold")
        ).pack(pady=40)

        frame_central = tk.Frame(self)
        frame_central.pack(expand=True)

        self.login = tk.LabelFrame(
            frame_central, text="Connexion User", padx=20, pady=20
        )
        self.login.pack(side="left", padx=20, fill="y")

        tk.Label(self.login, text="Identifiant").pack(anchor="w")
        self.entree_id = tk.Entry(self.login)
        self.entree_id.pack(fill="x", pady=(0, 10))

        tk.Label(self.login, text="Mot de passe").pack(anchor="w")
        self.entree_mdp = tk.Entry(self.login, show="*")
        self.entree_mdp.pack(fill="x", pady=(0, 10))

        tk.Label(self.login, text="Clé Privée").pack(anchor="w")
        tk.Button(self.login, text="importer", command=self.importer_cle).pack(
            anchor="w", pady=(0, 20)
        )

        tk.Button(
            self.login,
            text="SE CONNECTER",
            bg="green",
            fg="white",
            command=self.se_connecter,
        ).pack(fill="x")

        self.inscription = tk.LabelFrame(
            frame_central, text="Nouveau ?", padx=20, pady=20
        )
        self.inscription.pack(side="left", padx=20, fill="y")

        tk.Button(
            self.inscription,
            text="Créer un compte",
            font=("Times New Roman", 12),
            command=self.controleur.afficher_inscription,
        ).pack(pady=10)

    def importer_cle(self):
        fichier = filedialog.askopenfilename(title="Sélectionner la clé privée")
        if fichier:
            messagebox.showinfo("Succès", f"Clé importée :\n{fichier}")

    def se_connecter(self):
        identifiant = self.entree_id.get().strip()
        mdp_saisi = self.entree_mdp.get()

        if not identifiant or not mdp_saisi:
            messagebox.showerror("Erreur", "Identifiant et mot de passe obligatoires.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM utilisateurs WHERE nom = %s"
            cursor.execute(sql, (identifiant,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur de connexion à la BDD : {e}")
            return

        if not user:
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")
            return

        sel_bdd = user["sel"]
        hash_bdd = user["mot_de_passe"]

        a_hasher = (mdp_saisi + sel_bdd).encode("utf-8")
        hash_saisi = hashlib.sha256(a_hasher).hexdigest()

        if hash_saisi == hash_bdd:
            messagebox.showinfo("Succès", f"Connexion réussie, bienvenue {user['nom']} !")
        else:
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")


class PageInscription(tk.Frame):
    """Page de création de compte."""

    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur

        self.compte = tk.LabelFrame(
            self,
            text="Créer un compte sécurisé",
            font=("Times New Roman", 14, "bold"),
            padx=30,
            pady=20,
        )
        self.compte.pack(expand=True)

        tk.Label(self.compte, text="Clé Publique").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entree_cle_pub = tk.Entry(self.compte, width=30)
        self.entree_cle_pub.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.compte, text="importer", font=("Times New Roman", 8)).grid(
            row=0, column=2, pady=5
        )

        tk.Label(self.compte, text="Nom Complet").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entree_nom = tk.Entry(self.compte, width=30)
        self.entree_nom.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(self.compte, text="Identifiant unique").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entree_id = tk.Entry(self.compte, width=30)
        self.entree_id.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(self.compte, text="Mot de passe robuste").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.entree_mdp = tk.Entry(self.compte, show="*", width=30)
        self.entree_mdp.grid(row=3, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        tk.Label(
            self.compte,
            text="- 8 car\n- Maj\n- Chiffre",
            font=("Times New Roman", 8),
            justify="left",
        ).grid(row=4, column=1, sticky="w")

        tk.Label(self.compte, text="Confirmer le mdp").grid(
            row=5, column=0, sticky="w", pady=5
        )
        self.entree_mdp_conf = tk.Entry(self.compte, show="*", width=30)
        self.entree_mdp_conf.grid(
            row=5, column=1, columnspan=2, sticky="we", padx=5, pady=5
        )

        frame_btns = tk.Frame(self.compte)
        frame_btns.grid(row=6, column=0, columnspan=3, pady=20)

        tk.Button(
            frame_btns,
            text="Annuler",
            command=self.controleur.afficher_accueil,
        ).pack(side="left", padx=10)

        tk.Button(
            frame_btns,
            text="Création du compte",
            bg="black",
            fg="white",
            command=self.finaliser_inscription,
        ).pack(side="left", padx=10)

    def mot_de_passe_est_robuste(self, mdp: str) -> bool:
        if len(mdp) < 8:
            return False
        if not any(c.isupper() for c in mdp):
            return False
        if not any(c.isdigit() for c in mdp):
            return False
        return True

    def generer_sel_et_hash(self, mot_de_passe: str) -> tuple[str, str]:
        sel = os.urandom(16).hex()
        a_hasher = (mot_de_passe + sel).encode("utf-8")
        hash_mdp = hashlib.sha256(a_hasher).hexdigest()
        return sel, hash_mdp

    def finaliser_inscription(self):
        nom_complet = self.entree_nom.get().strip()
        identifiant = self.entree_id.get().strip()
        mdp1 = self.entree_mdp.get()
        mdp2 = self.entree_mdp_conf.get()

        if not nom_complet or not mdp1 or not mdp2:
            messagebox.showerror("Erreur", "Nom et mot de passe sont obligatoires.")
            return

        if mdp1 != mdp2:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        if not self.mot_de_passe_est_robuste(mdp1):
            messagebox.showerror(
                "Mot de passe faible",
                "Le mot de passe doit faire au moins 8 caractères,\n"
                "contenir une majuscule et un chiffre.",
            )
            return

        sel, hash_mdp = self.generer_sel_et_hash(mdp1)

        
        cle_privee, cle_publique = generate_key_pair()

        
        sauvegarder_cle_privee_local(identifiant, cle_privee)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """
                INSERT INTO utilisateurs (nom, mot_de_passe, sel, cle_publique)
                VALUES (%s, %s, %s, %s)
            """

            valeurs = (nom_complet, hash_mdp, sel, cle_publique.decode("utf-8"))

            cursor.execute(sql, valeurs)
            conn.commit()
            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Impossible de créer le compte : {e}")
            return

        messagebox.showinfo("Succès", "Compte créé ! Retour à l'accueil.")
        self.controleur.afficher_accueil()


if __name__ == "__main__":
    accueil = ApplicationMessagerie()
    accueil.mainloop()