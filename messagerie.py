import tkinter as tk
from tkinter import messagebox
import mysql.connector
from crypto import encrypt, decrypt
from cryptography.hazmat.primitives import serialization

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rsafe",
    )
    return conn

class PageConversation(tk.Frame):
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur
        self.utilisateur_connecte = None  
        self.cle_privee = None            

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        
        frame_contacts = tk.Frame(self, bg="#2c2c2c", relief="sunken", borderwidth=2)
        frame_contacts.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame_contacts, text="💬 Conversations", bg="#2c2c2c", fg="white",
                 font=("Times New Roman", 14, "bold")).pack(pady=10)

        self.liste_contacts = tk.Listbox(frame_contacts, font=("Times New Roman", 12),
                                          bg="#3c3c3c", fg="white", selectbackground="#4CAF50",
                                          borderwidth=0, highlightthickness=0)
        self.liste_contacts.pack(fill="both", expand=True, padx=10, pady=10)
        self.liste_contacts.bind("<<ListboxSelect>>", self.charger_conversation)

        tk.Button(frame_contacts, text="Déconnexion", bg="#c0392b", fg="white",
                  font=("Times New Roman", 11), command=self.deconnexion).pack(pady=10, padx=10, fill="x")

        
        frame_chat = tk.Frame(self, bg="#f0f0f0")
        frame_chat.grid(row=0, column=1, sticky="nsew")
        frame_chat.grid_rowconfigure(1, weight=1)
        frame_chat.grid_columnconfigure(0, weight=1)

        
        self.entete = tk.Label(frame_chat, text="Sélectionnez une conversation",
                                bg="#4CAF50", fg="white",
                                font=("Times New Roman", 13, "bold"), pady=10)
        self.entete.grid(row=0, column=0, sticky="ew")

        
        frame_messages = tk.Frame(frame_chat, bg="#f0f0f0")
        frame_messages.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_messages.grid_rowconfigure(0, weight=1)
        frame_messages.grid_columnconfigure(0, weight=1)

        self.historique = tk.Text(frame_messages, state='disabled', wrap="word",
                                   font=("Times New Roman", 12), bg="#f0f0f0",
                                   borderwidth=0, highlightthickness=0, padx=10, pady=10)
        self.historique.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(frame_messages, command=self.historique.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.historique.config(yscrollcommand=scrollbar.set)

        # Style de page de messagerie 
        self.historique.tag_configure("moi",foreground="white", background="#4CAF50")
        self.historique.tag_configure("autre",foreground="#333333", background="#ffffff")
        self.historique.tag_configure("nom", foreground="#888888", font=("Times New Roman", 9, "italic"))
       
        frame_saisie = tk.Frame(frame_chat, bg="#e0e0e0", pady=8)
        frame_saisie.grid(row=2, column=0, sticky="ew")
        frame_saisie.grid_columnconfigure(0, weight=1)

        self.entree_message = tk.Entry(frame_saisie, font=("Times New Roman", 12),
                                        relief="flat", bg="white", bd=5)
        self.entree_message.grid(row=0, column=0, sticky="ew", padx=(10, 5), ipady=6)
        self.entree_message.bind("<Return>", lambda event: self.envoyer_message())

        tk.Button(frame_saisie, text="Envoyer 🔒", bg="#4CAF50", fg="white",
                  font=("Times New Roman", 11, "bold"),
                  relief="flat", command=self.envoyer_message).grid(row=0, column=1, padx=(0, 10))

    def definir_utilisateur(self, nom, chemin_cle_privee):
        self.utilisateur_connecte = nom

        with open(chemin_cle_privee, "rb") as f:
            self.cle_privee = serialization.load_pem_private_key(f.read(), password=None)

        self.liste_contacts.delete(0, tk.END)

        self.historique.config(state='normal')
        self.historique.delete(1.0, tk.END)
        self.historique.config(state='disabled')

        self.entete.config(text="🔒 Sélectionnez une conversation")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nom FROM utilisateurs WHERE nom != %s", (nom,))
            for (contact,) in cursor.fetchall():
                self.liste_contacts.insert(tk.END, contact)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur : {e}")

    def charger_conversation(self, event):
        selection = self.liste_contacts.curselection()
        if not selection:
            return
        contact = self.liste_contacts.get(selection[0])

        
        self.entete.config(text=f"🔒 Conversation chiffrée avec {contact}")

        self.historique.config(state='normal')
        self.historique.delete(1.0, tk.END)

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT expediteur_id, destinataire_id, contenu_chiffre_destinataire, contenu_chiffre_expediteur
                FROM messages
                WHERE (expediteur_id = %s AND destinataire_id = %s)
                   OR (expediteur_id = %s AND destinataire_id = %s)
                ORDER BY date_creation ASC
            """, (self.utilisateur_connecte, contact, contact, self.utilisateur_connecte))

            for msg in cursor.fetchall():
                try:
                    if msg["destinataire_id"] == self.utilisateur_connecte:
                        texte = decrypt(msg["contenu_chiffre_destinataire"], self.cle_privee).decode("utf-8")
                        self.historique.insert(tk.END, f"{msg['expediteur_id']}\n", "nom")
                        self.historique.insert(tk.END, f" {texte} \n\n", "autre")
                    else:
                        texte = decrypt(msg["contenu_chiffre_expediteur"], self.cle_privee).decode("utf-8")
                        self.historique.insert(tk.END, f"Moi\n", "nom")
                        self.historique.insert(tk.END, f" {texte} \n\n", "moi")
                except Exception:
                    self.historique.insert(tk.END, "[Message illisible]\n")

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur : {e}")

        self.historique.config(state='disabled')
        self.historique.see(tk.END)

    def envoyer_message(self):
        texte = self.entree_message.get().strip()
        if not texte:
            return

        selection = self.liste_contacts.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionne un contact d'abord.")
            return
        contact = self.liste_contacts.get(selection[0])

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT cle_publique FROM utilisateurs WHERE nom = %s", (contact,))
            row = cursor.fetchone()
            cle_pub_destinataire = serialization.load_pem_public_key(row["cle_publique"].encode())

            cursor.execute("SELECT cle_publique FROM utilisateurs WHERE nom = %s", (self.utilisateur_connecte,))
            row2 = cursor.fetchone()
            cle_pub_expediteur = serialization.load_pem_public_key(row2["cle_publique"].encode())

            msg_bytes = texte.encode("utf-8")
            chiffre_dest = encrypt(msg_bytes, cle_pub_destinataire)
            chiffre_exp  = encrypt(msg_bytes, cle_pub_expediteur)

            cursor.execute("""
                INSERT INTO messages (expediteur_id, destinataire_id, contenu_chiffre_destinataire, contenu_chiffre_expediteur)
                VALUES (%s, %s, %s, %s)
            """, (self.utilisateur_connecte, contact, chiffre_dest, chiffre_exp))
            conn.commit()
            cursor.close()
            conn.close()

            self.historique.config(state='normal')
            self.historique.insert(tk.END, "Moi\n", "nom")
            self.historique.insert(tk.END, f" {texte} \n\n", "moi")
            self.historique.config(state='disabled')
            self.historique.see(tk.END)
            self.entree_message.delete(0, tk.END)

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur : {e}")

    def deconnexion(self):
        messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")
        self.utilisateur_connecte = None
        self.cle_privee = None
        self.controleur.afficher_accueil()