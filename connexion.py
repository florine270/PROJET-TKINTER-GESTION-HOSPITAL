import csv
import os
import mysql.connector
from tkinter import messagebox

print(">>> Chargement du fichier connexion.py")

# Fichiers CSV (optionnel si MySQL seulement)
FILENAME_PATIENTS = "patients.csv"
FILENAME_MEDECINS = "medecins.csv"

def lire_csv(fichier):
    if not os.path.exists(fichier):
        return []
    with open(fichier, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

def ecrire_csv(fichier, donnees):
    with open(fichier, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(donnees)

#  Validation corrigée sans vérification d'âge
def valider_entrees(donnees, is_medecin=False):
    if any(not champ.strip() for champ in donnees):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return False
    if not donnees[0].isdigit():
        messagebox.showerror("Erreur", "L'ID doit être un nombre.")
        return False
    return True

# Connexion utilisateur
def verifier_utilisateur_bdd(username, password):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
        return False

#  Fonctions Patients MySQL
def lire_patients_bdd():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        conn.close()
        return patients
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
        return []

def ajouter_patient_bdd(donnees):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        sql = """
            INSERT INTO patients (id, nom, prenom, date_naissance, sexe, adresse, remarque)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, donnees)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def supprimer_patient_bdd(patient_id):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def modifier_patient_bdd(donnees):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        sql = """
            UPDATE patients
            SET nom = %s, prenom = %s, date_naissance = %s, sexe = %s, adresse = %s, remarque = %s
            WHERE id = %s
        """
        cursor.execute(sql, donnees[1:] + [donnees[0]])
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

#  Fonctions Médecins MySQL
def lire_medecins_bdd():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medecins")
        medecins = cursor.fetchall()
        conn.close()
        return medecins
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
        return []

def ajouter_medecin_bdd(donnees):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        sql = """
            INSERT INTO medecins (id, nom, prenom, specialite, telephone, email, adresse)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, donnees)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def supprimer_medecin_bdd(medecin_id):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medecins WHERE id = %s", (medecin_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def modifier_medecin_bdd(donnees):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vivien03.',
            database='hpms'
        )
        cursor = conn.cursor()
        sql = """
            UPDATE medecins
            SET nom = %s, prenom = %s, specialite = %s,
                telephone = %s, email = %s, adresse = %s
            WHERE id = %s
        """
        cursor.execute(sql, donnees[1:] + [donnees[0]])
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))


