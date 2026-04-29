#  Messagerie Sécurisée

Application de messagerie instantanée avec chiffrement de bout en bout, développée en Python dans le cadre d'un projet scolaire.

---

##  Équipe & Répartition du travail

| Membre | Rôle |
|---|---|
| Hermann | Authentification, Base de données, intégration |
| Katia | Interface Tkinter, messagerie, POO |
| Lena | Chiffrement RSA, `crypto.py` |
| Yacine | Fonctionnalité Bonus, documentation |

---

##  Architecture du projet

```
ProjetTransversalPOO/
├── _pycache_/       → Dossier contenant les clés privées des utilisateurs
├── cles_privees/    → Dossier contenant les clés privées des utilisateurs
├── auth.py          → Pages d'accueil, connexion, inscription
├── crypto.py        → Fonctions de chiffrement RSA et hashage
├── messagerie.py    → Page de conversation, envoi/réception
└── modele_Poo.py    → Classes logiques (Utilisateur, Message, Conversation)

```

---

##  Choix de conception

### Base de données : MySQL
Nous avons choisi MySQL car c'est une base de données relationnelle robuste, compatible avec Python via `mysql-connector`. Elle permet de stocker les utilisateurs, leurs clés publiques et les messages chiffrés de manière structurée.

### Interface : Tkinter
Tkinter est intégré nativement dans Python, ce qui évite d'installer des dépendances supplémentaires. Il permet de créer une interface graphique simple et fonctionnelle, adaptée au niveau du projet.

### Chiffrement : RSA -> Cryptography
Cryptography propose des fonctions hautement sécurisées pour le chiffrement et le déchiffrement, ainsi que pour d'autres opérations cryptographiques. Même les débutants peuvent facilement chiffrer des données sans se perdre car cette bibliothèque reste relativement intuitive. 


### Hashage : SHA256
Le mot de passe est hashé avec SHA256 avant d'être stocké en BDD. Grâce à ça, même si un hacker accède à la BDD, il ne peut pas lire les mots de passe en clair.

### Salage
Un sel statique (`SEL_UNIQUE = "MichaelJackson"`) est ajouté au mot de passe avant le hashage. Cela empêche les attaques par dictionnaire simples.

---

##  Mesures de sécurité

### Chiffrement bout en bout
Lorsqu'un utilisateur s'inscrit sur le site de messagerie, il génère automatiquement une paire de clés. La clé publique est stockée dans la base de données, la clé privée est elle stockée localement sur le PC de l'utilisateur. 
Quand Hermann envoie un message à Katia :
1. Le message est chiffré avec la **clé publique de Katia** (stockée en BDD)
2. Le message est aussi chiffré avec la **clé publique de Hermann** (pour qu'il puisse relire ses propres messages)
3. Les deux versions chiffrées sont stockées en BDD dans `contenu_chiffre_destinataire` et `contenu_chiffre_expediteur`
4. Quand Katia ouvre la conversation, son app déchiffre le message avec **sa clé privée locale**

Même si un hacker accède à la BDD, il verra uniquement des données binaire illisibles.

### Stockage des clés privées
Les clés privées ne sont jamais envoyées sur le réseau ni stockées en BDD. Elles sont sauvegardées dans un dossier local `cles_privees/` sur la machine de l'utilisateur, sous la forme `nom_private.pem`.

### Mots de passe hachés et salés
```
mot de passe : "Abcd1234"
après salage : "Abcd1234MichaelJackson"
après hashage SHA256 : "ebe95f3906c098efaeb767..."
```
C'est cette valeur hashée qui est stockée en BDD, jamais le mot de passe en clair.

### Validation du mot de passe
Le mot de passe doit respecter ces règles :
- Minimum 8 caractères
- Au moins une majuscule
- Au moins un chiffre

---

##  Programmation Orientée Objet

### Classes dans `modele_Poo.py`

#### `Utilisateur`
Représente un utilisateur de l'application.
```python
class Utilisateur:
    def __init__(self, nom, cle_publique=None):
        self.nom = nom
        self.cle_publique = cle_publique
```

#### `Message`
Représente un message échangé entre deux utilisateurs.
```python
class Message:
    def __init__(self, expediteur, destinataire, 
                 contenu_chiffre_dest=None, contenu_chiffre_exp=None, lu=False):
        self.expediteur = expediteur
        self.destinataire = destinataire
        self.contenu_chiffre_dest = contenu_chiffre_dest
        self.contenu_chiffre_exp = contenu_chiffre_exp
        self.lu = lu  # False = non lu, True = lu
```

#### `Conversation`
Regroupe les messages entre deux utilisateurs.
```python
class Conversation:
    def __init__(self, utilisateur1, utilisateur2):
        self.utilisateur1 = utilisateur1
        self.utilisateur2 = utilisateur2
        self.messages = []
```

### Héritage
Les classes `PageAccueil`, `PageInscription` et `PageConversation` héritent toutes de `tk.Frame`. Cela évite de réécrire la logique de base des fenêtres Tkinter.


Si demain on voulait ajouter des messages vocaux ou des images, on créerait une classe `MessageImage` qui hériterait de `Message` sans modifier le code existant.

### Polymorphisme
La méthode `__str__` est définie différemment dans chaque classe :
- `Utilisateur.__str__` → retourne le nom de l'utilisateur
- `Message.__str__` → retourne expéditeur et destinataire
- `Conversation.__str__` → retourne les deux participants

---

## 🗄️ Structure de la base de données

### Table `utilisateurs`
| Colonne | Type | Description |
|---|---|---|
| id_user | INT | Identifiant unique |
| nom | VARCHAR(50) | Nom de l'utilisateur |
| mot_de_passe | TEXT | Hash SHA256 du mot de passe salé |
| cle_publique | LONGTEXT | Clé publique RSA au format PEM |
| date_creation | DATETIME | Date de création du compte |

### Table `messages`
| Colonne | Type | Description |
|---|---|---|
| id_message | INT | Identifiant unique |
| expediteur_id | VARCHAR(100) | Nom de l'expéditeur |
| destinataire_id | VARCHAR(100) | Nom du destinataire |
| contenu_chiffre_destinataire | BLOB | Message chiffré avec la clé publique du destinataire |
| contenu_chiffre_expediteur | BLOB | Message chiffré avec la clé publique de l'expéditeur |
| date_creation | DATETIME | Date d'envoi |
| lu | TINYINT | 0 = non lu, 1 = lu |

---

##  Tests réalisés

### Test 1 : Hashage et salage
**Objectif :** Vérifier que le hashage fonctionne correctement.

**Méthode :** Création de deux comptes (`Katia` et `Katia1`) avec le même mot de passe.

**Résultat :** Les deux hashs en BDD sont identiques, ce qui confirme que le hashage + salage fonctionne. Avec un sel statique, deux mots de passe identiques donnent le même hash — c'est la limite connue du sel unique.

---

### Test 2 : Chiffrement et déchiffrement des messages
**Objectif :** Vérifier que les messages sont bien chiffrés en BDD et déchiffrés à l'affichage.

**Méthode :** Connexion avec Lena, envoi d'un message à Katia. Vérification en BDD que le contenu est binaire (illisible). Connexion avec Katia, vérification que le message s'affiche correctement.

**Résultat :** Les messages sont bien stockés en BLOB chiffré en BDD, et correctement déchiffrés à l'affichage. 

---

### Test 3 : Statut lu/non lu
**Objectif :** Vérifier que la colonne `lu` se met bien à jour.

**Méthode :** Katia envoie un message à Test (lu = 0). Connexion avec Test, ouverture de la conversation avec Katia.

**Résultat :** La colonne `lu` passe de `0` à `1` en BDD après ouverture de la conversation. 

---

##  Difficultés rencontrées

### 1. Méthode `importer_cle` manquante
Le bouton "Importer" appelait une méthode inexistante, causant une `AttributeError` au lancement. **Solution :** Ajout de la méthode dans `PageAccueil`.

### 2. Import circulaire dans `messagerie.py`
Le fichier s'importait lui-même avec `from messagerie import PageConversation`. **Solution :** Suppression de cette ligne.

### 3. Types incorrects en BDD
Les colonnes `expediteur_id` et `destinataire_id` étaient de type `INT` alors que le code envoyait des noms (strings). **Solution :** `ALTER TABLE` pour passer en `VARCHAR(100)`.

### 4. Messages chiffrés stockés en TEXT au lieu de BLOB
Le chiffrement RSA produit des données binaires incompatibles avec le type TEXT. **Solution :** Modification des colonnes en `BLOB`.

### 5. Messages illisibles après déconnexion
Les anciens messages stockés avec les mauvais types ne pouvaient plus être déchiffrés. **Solution :** `DELETE FROM messages` et réinscription des utilisateurs.

### 6. Historique affiché sans cliquer sur un contact
Les messages s'affichaient automatiquement à l'arrivée sur la page. **Solution :** Ajout d'un `historique.delete()` dans `definir_utilisateur`.

### 7. `utilisateur_connecte` valait `None`
Les lignes pour passer le nom de l'utilisateur connecté n'étaient pas en place. **Solution :** Ajout de `page.definir_utilisateur()` dans `se_connecter`.

---

##  Lancer l'application

### Prérequis
```bash
pip install mysql-connector-python cryptography
```

### Lancement
```bash
python auth.py
```

### Configuration BDD
Importer le fichier `rsafe.sql` dans phpMyAdmin avant de lancer l'application.