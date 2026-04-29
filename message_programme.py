from cryptography.hazmat.primitives import serialization

from crypto import encrypt
from modele_Poo import MessageProgramme as ModeleMessageProgramme


class MessageProgramme(ModeleMessageProgramme):
    def enregistrer(self, connection_bdd):
        conn = connection_bdd()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT cle_publique FROM utilisateurs WHERE nom = %s", (self.destinataire,))
        row_destinataire = cursor.fetchone()

        cursor.execute("SELECT cle_publique FROM utilisateurs WHERE nom = %s", (self.expediteur,))
        row_expediteur = cursor.fetchone()

        if row_destinataire is None or row_expediteur is None:
            cursor.close()
            conn.close()
            raise ValueError("Utilisateur introuvable.")

        cle_pub_destinataire = serialization.load_pem_public_key(
            row_destinataire["cle_publique"].encode()
        )
        cle_pub_expediteur = serialization.load_pem_public_key(
            row_expediteur["cle_publique"].encode()
        )

        msg_bytes = self.contenu.encode("utf-8")
        self.contenu_chiffre_dest = encrypt(msg_bytes, cle_pub_destinataire)
        self.contenu_chiffre_exp = encrypt(msg_bytes, cle_pub_expediteur)

        cursor.execute(
            """
                INSERT INTO messages
                (expediteur_id, destinataire_id, contenu_chiffre_destinataire,
                 contenu_chiffre_expediteur, date_programmee)
                VALUES (%s, %s, %s, %s, DATE_ADD(NOW(), INTERVAL %s SECOND))
            """,
            (
                self.expediteur,
                self.destinataire,
                self.contenu_chiffre_dest,
                self.contenu_chiffre_exp,
                self.secondes,
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()
