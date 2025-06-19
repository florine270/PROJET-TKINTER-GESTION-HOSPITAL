import csv
import os
from tkinter import *
from tkinter import messagebox
from lang import t, switch_lang 

# Fichiers CSV
FILENAME_PATIENTS = "patients.csv"
FILENAME_MEDECINS = "medecins.csv"

# Identifiants de connexion
USERNAME = "hafsaoumaima"
PASSWORD = "dev@101"

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
        messagebox.showerror("Erreur", t("error_age"))
        return False
    return True

# === Interface de Connexion ===

def verifier_connexion():
    utilisateur = entry_user.get()
    mot_de_passe = entry_pass.get()
    if utilisateur == USERNAME and mot_de_passe == PASSWORD:
        messagebox.showinfo("Succès", t("success"))
    else:
        messagebox.showerror("Erreur", t("error_login"))

def changer_langue():
    switch_lang()
    update_interface()

def update_interface():
    root.title(t("title"))
    label_user.config(text=t("username"))
    label_pass.config(text=t("password"))
    btn_connexion.config(text=t("login"))
    btn_langue.config(text=t("lang"))

# Création de la fenêtre principale
root = Tk()
root.geometry("400x220")

label_user = Label(root, text="")
label_user.pack(pady=5)
entry_user = Entry(root)
entry_user.pack()

label_pass = Label(root, text="")
label_pass.pack(pady=5)
entry_pass = Entry(root, show="*")
entry_pass.pack()

btn_connexion = Button(root, text="", command=verifier_connexion)
btn_connexion.pack(pady=10)

btn_langue = Button(root, text="", command=changer_langue)
btn_langue.pack()

update_interface()
root.mainloop()
