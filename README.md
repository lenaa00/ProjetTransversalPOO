# 🔐 Messagerie Sécurisée

Application de messagerie instantanée avec chiffrement de bout en bout, développée en Python dans le cadre d'un projet scolaire.

---

## 🗂️ Architecture du projet

```
ProjetTransversalPOO/
│
├── cles_privees/          → Dossier contenant les clés privées des utilisateurs (fichiers .pem)
├── auth.py                → Pages d'accueil, connexion, inscription
├── crypto.py              → Fonctions de chiffrement RSA et hashage SHA-256
├── database.py            → Connexion et interactions avec la base de données
├── message_programme.py   → Fonctionnalité d'envoi de messages programmés
├── messagerie.py          → Page de conversation, envoi/réception des messages
├── modele_Poo.py          → Classes logiques (Utilisateur, Message, Conversation)
└── README.md              → Documentation du projet
```

---

## ⚙️ Choix de conception

### Base de données : MySQL
Nous avons choisi MySQL car c'est celle qu'on a le plus utilisée, c'est une base de données robuste, compatible avec Python via `mysql-connector`. Elle permet de stocker les utilisateurs, leurs clés publiques et les messages chiffrés de manière structurée.

### Interface : Tkinter
Tkinter est intégré nativement dans Python, ce qui évite d'installer des dépendances supplémentaires. Il permet de créer une interface graphique simple et fonctionnelle, adaptée au niveau du projet.

### Chiffrement : RSA via la bibliothèque Cryptography
La bibliothèque `cryptography` propose des fonctions hautement sécurisées pour le chiffrement et le déchiffrement. Elle reste relativement intuitive et simple.

### Hashage : SHA-256
Le mot de passe est hashé avec SHA-256 avant d'être stocké en BDD. Même si un hacker accède à la BDD, il ne peut pas lire les mots de passe en clair.

### Salage
Un sel statique (`SEL_UNIQUE = "MichaelJackson"`) est ajouté au mot de passe avant le hashage. Cela complique les attaques.

---

## 🔒 Mesures de sécurité

### Chiffrement bout en bout
Lorsqu'un utilisateur s'inscrit, il génère automatiquement une paire de clés RSA. La clé publique est stockée en BDD, la clé privée est stockée localement sur la machine de l'utilisateur.

Quand Hermann envoie un message à Katia :
1. Le message est chiffré avec la **clé publique de Katia** (stockée en BDD)
2. Le message est aussi chiffré avec la **clé publique de Hermann** (pour qu'il puisse relire ses propres messages)
3. Les deux versions chiffrées sont stockées en BDD dans `contenu_chiffre_destinataire` et `contenu_chiffre_expediteur`
4. Quand Katia ouvre la conversation, son app déchiffre le message avec **sa clé privée locale**

Même si un hacker accède à la BDD, il verra uniquement des données binaires illisibles.

### Stockage des clés privées
Les clés privées ne sont jamais envoyées sur le réseau ni stockées en BDD. Elles sont sauvegardées dans le dossier local `cles_privees/` sous la forme `identifiant_private.pem`.

### Mots de passe hachés et salés
```
Mot de passe saisi   : "Abcd1234"
Après salage         : "Abcd1234MichaelJackson"
Après hashage SHA256 : "ebe95f3906c098efaeb767..."
```
C'est cette valeur hashée qui est stockée en BDD, jamais le mot de passe en clair.

### Validation du mot de passe
Le mot de passe doit respecter ces règles :
- Minimum 8 caractères
- Au moins une majuscule
- Au moins un chiffre

---

## 🏗️ Programmation Orientée Objet

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
| id_user | INT AUTO_INCREMENT | Identifiant unique |
| nom | VARCHAR(50) | Nom complet de l'utilisateur |
| identifiant | TEXT | Identifiant de connexion |
| mot_de_passe | TEXT | Hash SHA-256 du mot de passe salé |
| cle_publique | LONGTEXT | Clé publique RSA au format PEM |
| date_creation | DATETIME | Date de création du compte |

### Table `messages`
| Colonne | Type | Description |
|---|---|---|
| id_message | INT AUTO_INCREMENT | Identifiant unique |
| expediteur_id | VARCHAR(100) | Nom de l'expéditeur |
| destinataire_id | VARCHAR(100) | Nom du destinataire |
| contenu_chiffre_destinataire | BLOB | Message chiffré avec la clé publique du destinataire |
| contenu_chiffre_expediteur | BLOB | Message chiffré avec la clé publique de l'expéditeur |
| date_creation | DATETIME | Date d'envoi (automatique) |
| date_programmee | DATETIME | Date d'envoi différé (fonctionnalité bonus) |
| lu | TINYINT(1) | 0 = non lu, 1 = lu |

---

## ⭐ Fonctionnalité supplémentaire : Messages programmés

Nous avons ajouté la possibilité d'envoyer un message à une date et heure future. Le message est chiffré et stocké en BDD immédiatement, mais il n'apparaît chez le destinataire qu'une fois la date programmée dépassée.

Un planificateur tourne en arrière-plan (thread Python) et vérifie toutes les 5 secondes si des messages programmés doivent être envoyés. Cette fonctionnalité est gérée dans `message_programme.py` et utilise la classe `MessageProgramme` qui hérite de `Message`.

---

## 🧪 Tests réalisés

### Test 1 — Inscription et génération des clés
**Objectif :** Vérifier que l'inscription fonctionne correctement.

**Méthode :** Création d'un compte → vérification en BDD que le mot de passe est bien hashé (pas en clair) et que la clé publique est bien stockée. Vérification que le fichier `.pem` a bien été créé dans `cles_privees/`.

**Résultat :** Le mot de passe est hashé en BDD, la clé publique est présente, le fichier `.pem` est créé localement. ✅

---

### Test 2 — Hashage et salage
**Objectif :** Vérifier que le hashage fonctionne correctement.

**Méthode :** Création de deux comptes avec le même mot de passe. Vérification en BDD que les deux hashs sont identiques.

**Résultat :** Les deux hashs sont identiques → confirme que le hashage fonctionne. C'est aussi la limite connue du sel statique : deux mots de passe identiques donnent le même hash. Dans un vrai système on utiliserait un sel aléatoire par utilisateur. ✅

---

### Test 3 — Connexion
**Objectif :** Vérifier que l'authentification fonctionne.

**Méthode :** Test avec un bon mot de passe → connexion réussie. Test avec un mauvais mot de passe → message d'erreur. Test avec un utilisateur inexistant → message d'erreur.

**Résultat :** Les trois cas fonctionnent correctement. ✅

---

### Test 4 — Chiffrement et déchiffrement des messages
**Objectif :** Vérifier que les messages sont bien chiffrés en BDD et déchiffrés à l'affichage.

**Méthode :** Connexion avec Lena, envoi d'un message à Katia. Vérification en BDD que le contenu est en BLOB binaire (illisible). Connexion avec Katia, vérification que le message s'affiche correctement en clair.

**Résultat :** Les messages sont stockés en BLOB chiffré en BDD et correctement déchiffrés à l'affichage. ✅

---

### Test 5 — Statut lu/non lu
**Objectif :** Vérifier que la colonne `lu` se met bien à jour.

**Méthode :** Katia envoie un message à Hermann (`lu = 0`). Connexion avec Hermann, ouverture de la conversation avec Katia.

**Résultat :** La colonne `lu` passe de `0` à `1` en BDD après ouverture de la conversation. ✅

---

## ⚠️ Difficultés rencontrées

### Types incorrects en BDD
Les colonnes `expediteur_id` et `destinataire_id` étaient de type `INT` alors que le code envoyait des noms (strings). Tous les messages étaient stockés avec la valeur `0`. **Solution :** `ALTER TABLE` pour passer en `VARCHAR(100)`.

### Messages chiffrés stockés en TEXT au lieu de BLOB
Le chiffrement RSA produit des données binaires incompatibles avec le type TEXT. **Solution :** Modification des colonnes en `BLOB`.

### Historique affiché sans cliquer sur un contact
Les messages s'affichaient automatiquement à l'arrivée sur la page de conversation. **Solution :** Ajout d'un `historique.delete()` dans `definir_utilisateur`.

---

## 🚀 Lancer l'application

### Prérequis
```bash
pip install mysql-connector-python cryptography
```

### Configuration BDD
Importer le fichier `rsafe.sql` dans phpMyAdmin avant de lancer l'application.

### Lancement
```bash
python auth.py
```