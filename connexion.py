import csv
import os
import mysql.connector
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()
utilisateur = os.getenv("DB_USER") or "root"
mot_de_passe = os.getenv("DB_PASSWORD") or "vivien03."
bd = os.getenv("DB_NAME") or "hpms"

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

def valider_entrees(donnees, is_medecin=False):
    if any(not champ.strip() for champ in donnees):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return False
    if not donnees[0].isdigit():
        messagebox.showerror("Erreur", "L'ID doit être un nombre.")
        return False
    return True

def verifier_utilisateur_bdd(username, password):
    try:
        conn = mysql.connector.connect(
            host='localhost', user=utilisateur, password=mot_de_passe, database=bd
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
        return False
# ✅ Patients
def lire_patients_bdd():
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
        return []

def ajouter_patient_bdd(donnees):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = "INSERT INTO patients (id, nom, prenom, date_naissance, sexe, adresse, remarque) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, donnees)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def modifier_patient_bdd(donnees):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = "UPDATE patients SET nom=%s, prenom=%s, date_naissance=%s, sexe=%s, adresse=%s, remarque=%s WHERE id=%s"
        cursor.execute(sql, donnees[1:] + [donnees[0]])
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def supprimer_patient_bdd(patient_id):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
# 👨🏽‍⚕️ Médecins
def lire_medecins_bdd():
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medecins")
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))
        return []

def ajouter_medecin_bdd(donnees):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = "INSERT INTO medecins (id, nom, prenom, specialite, telephone, email, adresse) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, donnees)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def modifier_medecin_bdd(donnees):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = "UPDATE medecins SET nom=%s, prenom=%s, specialite=%s, telephone=%s, email=%s, adresse=%s WHERE id=%s"
        cursor.execute(sql, donnees[1:] + [donnees[0]])
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

def supprimer_medecin_bdd(medecin_id):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medecins WHERE id = %s", (medecin_id,))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur MySQL", str(e))

# 🧪 Résultats Labo
def ajouter_resultat_labo(donnees):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = """
            INSERT INTO resultats_labo (patient_id, type_analyse, valeur, unite, interpretation, date_analyse)
            VALUES (%s, %s, %s, %s, %s, STR_TO_DATE(%s, '%%d/%%m/%%Y'))
        """
        cursor.execute(sql, donnees)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur Labo", str(e))

def lire_resultats_labo():
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = """
            SELECT CONCAT(p.id, ' - ', p.nom, ' ', p.prenom),
                   r.type_analyse, r.valeur, r.unite, r.interpretation,
                   DATE_FORMAT(r.date_analyse, '%%d/%%m/%%Y')
            FROM resultats_labo r
            JOIN patients p ON r.id_patient = p.id
            ORDER BY r.date_analyse DESC
        """
        cursor.execute(sql)
        resultats = cursor.fetchall()
        return resultats
    except Exception as e:
        messagebox.showerror("Erreur Labo", str(e))
        return []

# 📅 Rendez-vous
def ajouter_rendez_vous(donnees):
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = "INSERT INTO rendez_vous (patient_id, medecin_id, date_heure, motif) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, donnees)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erreur RDV", str(e))

def lire_rendez_vous():
    try:
        conn = mysql.connector.connect(host='localhost', user=utilisateur, password=mot_de_passe, database=bd)
        cursor = conn.cursor()
        sql = """
            SELECT r.id,
                   CONCAT(p.id, ' - ', p.nom, ' ', p.prenom),
                   CONCAT(m.id, ' - ', m.nom, ' ', m.prenom),
                   DATE_FORMAT(r.date_heure, '%%d/%%m/%%Y %%H:%%i'),
                   r.motif
            FROM rendez_vous r
            JOIN patients p ON r.id_patient = p.id
            JOIN medecins m ON r.id_medecin = m.id
            ORDER BY r.date_heure DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erreur RDV", str(e))
        return []

