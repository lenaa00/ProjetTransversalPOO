class Utilisateur:
    def __init__(self, nom, cle_publique=None):
        self.nom = nom
        self.cle_publique = cle_publique

    def __str__(self):
        return f"Utilisateur({self.nom})"


class Message:
    def __init__(
        self,
        expediteur,
        destinataire,
        contenu_chiffre_dest=None,
        contenu_chiffre_exp=None,
        lu=False,
        date_programmee=None,
    ):
        self.expediteur = expediteur
        self.destinataire = destinataire
        self.contenu_chiffre_dest = contenu_chiffre_dest
        self.contenu_chiffre_exp = contenu_chiffre_exp
        self.lu = lu
        self.date_programmee = date_programmee

    def __str__(self):
        return f"Message de {self.expediteur} a {self.destinataire}"


class MessageProgramme(Message):
    def __init__(self, expediteur, destinataire, contenu, secondes):
        super().__init__(expediteur, destinataire)
        self.contenu = contenu
        self.secondes = secondes

    def __str__(self):
        return (
            f"Message programme de {self.expediteur} a {self.destinataire} "
            f"dans {self.secondes} secondes"
        )


class Conversation:
    def __init__(self, utilisateur1, utilisateur2):
        self.utilisateur1 = utilisateur1
        self.utilisateur2 = utilisateur2
        self.messages = []

    def ajouter_message(self, message):
        self.messages.append(message)

    def __str__(self):
        return f"Conversation entre {self.utilisateur1} et {self.utilisateur2}"
