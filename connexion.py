import csv
import os
from tkinter import *
import mysql.connector
from tkinter import messagebox

# Fichiers CSV
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
        messagebox.showerror("Erreur", t("error_fields"))
        return False
    if not donnees[0].isdigit():
        messagebox.showerror("Erreur", t("error_id"))
        return False
    if not is_medecin and not donnees[3].isdigit():
        messagebox.showerror("Erreur", "L'âge doit être un nombre.")
        return False
    return True
