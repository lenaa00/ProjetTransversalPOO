import tkinter as tk
from tkinter import messagebox
import mysql.connector
from crypto import encrypt, decrypt
from cryptography.hazmat.primitives import serialization
from modele_Poo import Utilisateur, Message, Conversation
from message_programme import MessageProgramme


def connection_bdd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rsafe",
    )
    return conn


class PageConversation(tk.Frame):
    def __init__(self, parent, app_messageie):
        super().__init__(parent)
        self.app_messageie = app_messageie
        self.utilisateur_connecte = None
        self.cle_privee = None
        self.contact_actuel = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        page_contacts = tk.Frame(self, bg="#2c2c2c", relief="sunken", borderwidth=2)
        page_contacts.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            page_contacts,
            text="Conversations",
            bg="#2c2c2c",
            fg="white",
            font=("Times New Roman", 14, "bold"),
        ).pack(pady=10)

        self.liste_contacts = tk.Listbox(
            page_contacts,
            font=("Times New Roman", 12),
            bg="#3c3c3c",
            fg="white",
            selectbackground="#4CAF50",
            borderwidth=0,
            highlightthickness=0,
        )
        self.liste_contacts.pack(fill="both", expand=True, padx=10, pady=10)
        self.liste_contacts.bind("<<ListboxSelect>>", self.ouvrir_conversation)

        tk.Button(
            page_contacts,
            text="Deconnexion",
            bg="#c0392b",
            fg="white",
            font=("Times New Roman", 11),
            command=self.deconnexion,
        ).pack(pady=10, padx=10, fill="x")

        zone_messages = tk.Frame(self, bg="#f0f0f0")
        zone_messages.grid(row=0, column=1, sticky="nsew")
        zone_messages.grid_rowconfigure(1, weight=1)
        zone_messages.grid_columnconfigure(0, weight=1)

        self.conversations = tk.Label(
            zone_messages,
            text="Selectionnez une conversation",
            bg="#4CAF50",
            fg="white",
            font=("Times New Roman", 13, "bold"),
            pady=10,
        )
        self.conversations.grid(row=0, column=0, sticky="ew")

        zone_chat = tk.Frame(zone_messages, bg="#f0f0f0")
        zone_chat.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        zone_chat.grid_rowconfigure(0, weight=1)
        zone_chat.grid_columnconfigure(0, weight=1)

        self.affichage_messages = tk.Text(
            zone_chat,
            state="disabled",
            wrap="word",
            font=("Times New Roman", 12),
            bg="#f0f0f0",
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
        )
        self.affichage_messages.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(zone_chat, command=self.affichage_messages.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.affichage_messages.config(yscrollcommand=scrollbar.set)

        self.affichage_messages.tag_configure("moi", foreground="white", background="#4CAF50")
        self.affichage_messages.tag_configure("autre", foreground="#333333", background="#ffffff")
        self.affichage_messages.tag_configure(
            "nom", foreground="#888888", font=("Times New Roman", 9, "italic")
        )

        saisie_texte = tk.Frame(zone_messages, bg="#e0e0e0", pady=8)
        saisie_texte.grid(row=2, column=0, sticky="ew")
        saisie_texte.grid_columnconfigure(0, weight=1)

        self.champ_texte = tk.Entry(
            saisie_texte,
            font=("Times New Roman", 12),
            relief="flat",
            bg="white",
            bd=5,
        )
        self.champ_texte.grid(row=0, column=0, sticky="ew", padx=(10, 5), ipady=6)
        self.champ_texte.bind("<Return>", lambda event: self.envoyer())

        tk.Label(
            saisie_texte,
            text="Delai (s)",
            bg="#e0e0e0",
            font=("Times New Roman", 10),
        ).grid(row=0, column=1, padx=(0, 5))

        self.champ_delai = tk.Entry(
            saisie_texte,
            width=7,
            font=("Times New Roman", 11),
            relief="flat",
            bg="white",
            bd=5,
        )
        self.champ_delai.grid(row=0, column=2, padx=(0, 5), ipady=6)

        tk.Button(
            saisie_texte,
            text="Programmer",
            bg="#2980b9",
            fg="white",
            font=("Times New Roman", 11, "bold"),
            relief="flat",
            command=self.programmer_message,
        ).grid(row=0, column=3, padx=(0, 5))

        tk.Button(
            saisie_texte,
            text="Envoyer",
            bg="#4CAF50",
            fg="white",
            font=("Times New Roman", 11, "bold"),
            relief="flat",
            command=self.envoyer,
        ).grid(row=0, column=4, padx=(0, 10))

        self.after(3000, self.actualiser_messages_programmes)

    def definir_utilisateur(self, nom, chemin_cle_privee):
        self.utilisateur_connecte = nom
        self.contact_actuel = None

        with open(chemin_cle_privee, "rb") as f:
            self.cle_privee = serialization.load_pem_private_key(f.read(), password=None)

        self.liste_contacts.delete(0, tk.END)

        self.affichage_messages.config(state="normal")
        self.affichage_messages.delete(1.0, tk.END)
        self.affichage_messages.config(state="disabled")

        self.conversations.config(text="Selectionnez une conversation")

        try:
            conn = connection_bdd()
            cursor = conn.cursor()
            cursor.execute("SELECT nom FROM utilisateurs WHERE nom != %s", (nom,))
            for (contact,) in cursor.fetchall():
                self.liste_contacts.insert(tk.END, contact)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur : {e}")

    def ouvrir_conversation(self, event):
        selection = self.liste_contacts.curselection()
        if selection:
            contact = self.liste_contacts.get(selection[0])
            self.contact_actuel = contact
        elif self.contact_actuel:
            contact = self.contact_actuel
        else:
            return

        self.conversations.config(text=f"Conversation chiffree avec {contact}")

        self.affichage_messages.config(state="normal")
        self.affichage_messages.delete(1.0, tk.END)

        try:
            conn = connection_bdd()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT expediteur_id, destinataire_id,
                       contenu_chiffre_destinataire, contenu_chiffre_expediteur
                FROM messages
                WHERE (
                    (expediteur_id = %s AND destinataire_id = %s)
                    OR (expediteur_id = %s AND destinataire_id = %s)
                )
                AND (date_programmee IS NULL OR date_programmee <= NOW())
                ORDER BY COALESCE(date_programmee, date_creation) ASC, date_creation ASC
            """,
                (self.utilisateur_connecte, contact, contact, self.utilisateur_connecte),
            )

            for msg in cursor.fetchall():
                try:
                    if msg["destinataire_id"] == self.utilisateur_connecte:
                        texte = decrypt(
                            msg["contenu_chiffre_destinataire"], self.cle_privee
                        ).decode("utf-8")
                        self.affichage_messages.insert(tk.END, f"{msg['expediteur_id']}\n", "nom")
                        self.affichage_messages.insert(tk.END, f" {texte} \n\n", "autre")
                    else:
                        texte = decrypt(
                            msg["contenu_chiffre_expediteur"], self.cle_privee
                        ).decode("utf-8")
                        self.affichage_messages.insert(tk.END, "Moi\n", "nom")
                        self.affichage_messages.insert(tk.END, f" {texte} \n\n", "moi")
                except Exception:
                    self.affichage_messages.insert(tk.END, "[Message illisible]\n")

            cursor.execute(
                """
                UPDATE messages SET lu = 1
                WHERE destinataire_id = %s AND expediteur_id = %s AND lu = 0
                AND (date_programmee IS NULL OR date_programmee <= NOW())
            """,
                (self.utilisateur_connecte, contact),
            )
            conn.commit()

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur : {e}")

        self.affichage_messages.config(state="disabled")
        self.affichage_messages.see(tk.END)

    def envoyer(self):
        texte = self.champ_texte.get().strip()
        if not texte:
            return

        selection = self.liste_contacts.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Selectionne un contact d'abord.")
            return
        contact = self.liste_contacts.get(selection[0])
        self.contact_actuel = contact

        try:
            conn = connection_bdd()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT cle_publique FROM utilisateurs WHERE nom = %s", (contact,))
            row = cursor.fetchone()
            cle_pub_destinataire = serialization.load_pem_public_key(row["cle_publique"].encode())

            cursor.execute("SELECT cle_publique FROM utilisateurs WHERE nom = %s", (self.utilisateur_connecte,))
            row2 = cursor.fetchone()
            cle_pub_expediteur = serialization.load_pem_public_key(row2["cle_publique"].encode())

            msg_bytes = texte.encode("utf-8")
            chiffre_dest = encrypt(msg_bytes, cle_pub_destinataire)
            chiffre_exp = encrypt(msg_bytes, cle_pub_expediteur)

            nouveau_msg = Message(
                expediteur=self.utilisateur_connecte,
                destinataire=contact,
                contenu_chiffre_dest=chiffre_dest,
                contenu_chiffre_exp=chiffre_exp,
            )

            cursor.execute(
                """
                INSERT INTO messages
                (expediteur_id, destinataire_id,
                 contenu_chiffre_destinataire, contenu_chiffre_expediteur)
                VALUES (%s, %s, %s, %s)
            """,
                (
                    nouveau_msg.expediteur,
                    nouveau_msg.destinataire,
                    nouveau_msg.contenu_chiffre_dest,
                    nouveau_msg.contenu_chiffre_exp,
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()

            self.affichage_messages.config(state="normal")
            self.affichage_messages.insert(tk.END, "Moi\n", "nom")
            self.affichage_messages.insert(tk.END, f" {texte} \n\n", "moi")
            self.affichage_messages.config(state="disabled")
            self.affichage_messages.see(tk.END)
            self.champ_texte.delete(0, tk.END)

        except mysql.connector.Error as e:
            messagebox.showerror("Erreur BDD", f"Erreur : {e}")

    def programmer_message(self):
        texte = self.champ_texte.get().strip()
        delai = self.champ_delai.get().strip()

        if not texte:
            return

        if not delai.isdigit() or int(delai) <= 0:
            messagebox.showerror("Erreur", "Le delai doit etre un nombre de secondes.")
            return

        selection = self.liste_contacts.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Selectionne un contact d'abord.")
            return
        contact = self.liste_contacts.get(selection[0])
        self.contact_actuel = contact

        try:
            message_programme = MessageProgramme(
                expediteur=self.utilisateur_connecte,
                destinataire=contact,
                contenu=texte,
                secondes=int(delai),
            )
            message_programme.enregistrer(connection_bdd)

            self.champ_texte.delete(0, tk.END)
            self.champ_delai.delete(0, tk.END)
            messagebox.showinfo("Message programme", f"Message programme dans {delai} secondes.")
        except (mysql.connector.Error, ValueError) as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")

    def actualiser_messages_programmes(self):
        if self.utilisateur_connecte is not None and self.contact_actuel is not None:
            self.ouvrir_conversation(None)

        self.after(3000, self.actualiser_messages_programmes)

    def deconnexion(self):
        messagebox.showinfo("Deconnexion", "Vous etes deconnecte.")
        self.utilisateur_connecte = None
        self.cle_privee = None
        self.contact_actuel = None
        self.app_messageie.afficher_accueil()
