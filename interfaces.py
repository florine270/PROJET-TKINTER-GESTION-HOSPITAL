import tkinter as tk
from tkinter import ttk, messagebox
from connexion import lire_csv, ecrire_csv, valider_entrees, FILENAME_PATIENTS, FILENAME_MEDECINS
from datetime import datetime
def styliser():
    style = ttk.Style()
    style.theme_use('vista')
    style.configure('Treeview', rowheight=30)

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime



def valider_entrees(donnees):

    for i, val in enumerate(donnees):
        if i != 6 and not val.strip():
            messagebox.showerror("Erreur", "Tous les champs sauf 'Remarque' doivent être remplis.")
            return False

    date_naissance = donnees[3].strip()
    if date_naissance == "jj/mm/aaaa" or not date_naissance:
        messagebox.showerror("Erreur", "La date de naissance doit être renseignée au format jj/mm/aaaa.")
        return False
    try:
        datetime.strptime(date_naissance, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Erreur", "La date de naissance doit être au format jj/mm/aaaa.")
        return False

    return True


def ouvrir_interface_patients():
    fenetre = tk.Toplevel()
    fenetre.title("Gestion des Patients")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#F3E8FF")  # soft lavender background
    styliser()

    colonnes = ["ID", "Nom", "Prénom", "Date de Naissance", "Sexe", "Adresse", "Remarque"]
    champs = []

    cadre_form = ttk.Frame(fenetre)
    cadre_form.pack(pady=10, padx=20)

    # Add a background color and padding using a canvas or label
    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="groove")
    form_bg.pack()

    for i, col in enumerate(colonnes):
        label = ttk.Label(form_bg, text=col + " :", foreground="#333333", background="white")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        if col == "Sexe":
            champ = ttk.Combobox(form_bg, values=["Homme", "Femme"], state="readonly", width=37)
        elif col == "Date de Naissance":
            champ = ttk.Entry(form_bg, width=40)
            champ.insert(0, "jj/mm/aaaa")
        else:
            champ = ttk.Entry(form_bg, width=40)

        champ.grid(row=i, column=1, padx=10, pady=5)
        champs.append(champ)

    # Treeview styling
    style = ttk.Style()
    style.configure("Treeview", 
                    background="white", 
                    foreground="black", 
                    rowheight=30, 
                    fieldbackground="white")
    style.map('Treeview', background=[('selected', '#CBA1E9')])
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#D1B3FF", foreground="black")

    tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(expand=True, fill="both", pady=10, padx=20)

    def charger():
        tableau.delete(*tableau.get_children())
        for ligne in lire_csv(FILENAME_PATIENTS):
            tableau.insert("", "end", values=ligne)

    def ajouter():
        donnees = [champ.get() for champ in champs]
        if valider_entrees(donnees):
            patients = lire_csv(FILENAME_PATIENTS)
            patients.append(donnees)
            ecrire_csv(FILENAME_PATIENTS, patients)
            charger()
            for champ in champs: 
                champ.delete(0, tk.END)

    def remplir(event):
        selection = tableau.selection()
        if selection:
            ligne = tableau.item(selection[0])["values"]
            for champ, val in zip(champs, ligne):
                champ.delete(0, tk.END)
                champ.insert(0, val)

    def modifier():
        selection = tableau.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un patient.")
            return
        nouvelles = [champ.get() for champ in champs]
        if not valider_entrees(nouvelles):
            return
        patients = lire_csv(FILENAME_PATIENTS)
        patients[tableau.index(selection[0])] = nouvelles
        ecrire_csv(FILENAME_PATIENTS, patients)
        charger()

    def supprimer():
        selection = tableau.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un patient.")
            return
        patients = lire_csv(FILENAME_PATIENTS)
        del patients[tableau.index(selection[0])]
        ecrire_csv(FILENAME_PATIENTS, patients)
        charger()
        for champ in champs: 
            champ.delete(0, tk.END)

    cadre_btns = ttk.Frame(fenetre)
    cadre_btns.pack(pady=15)
    
    for i, (label, command) in enumerate([("Ajouter", ajouter), ("Modifier", modifier), ("Supprimer", supprimer)]):
        btn = ttk.Button(cadre_btns, text=label, command=command)
        btn.grid(row=0, column=i, padx=10, ipadx=10, ipady=5)

    tableau.bind("<<TreeviewSelect>>", remplir)
    charger()



def ouvrir_interface_medecins():
    fenetre = tk.Toplevel()
    fenetre.title("Gestion des Médecins")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#E6F4EA")  # Vert doux
    styliser()

    colonnes = ["ID", "Nom", "Prénom", "Spécialité", "Téléphone", "Email", "Adresse"]
    champs = []

    cadre_form = ttk.Frame(fenetre)
    cadre_form.pack(pady=10, padx=20)

    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="groove")
    form_bg.pack()

    for i, col in enumerate(colonnes):
        label = ttk.Label(form_bg, text=col + " :", foreground="#2F4F2F", background="white")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        champ = ttk.Entry(form_bg, width=40)
        champ.grid(row=i, column=1, padx=10, pady=5)
        champs.append(champ)

    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white")
    style.map('Treeview', background=[('selected', '#B6E1C2')])
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                    background="#A8D5BA", foreground="black")

    tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(expand=True, fill="both", pady=10, padx=20)

    def charger():
        tableau.delete(*tableau.get_children())
        for ligne in lire_csv(FILENAME_MEDECINS):
            tableau.insert("", "end", values=ligne)

    # Fonction ajouter correctement placée
    def ajouter():
        donnees = [champ.get() for champ in champs]

        if all(donnees):
            medecins = lire_csv(FILENAME_MEDECINS)
            medecins.append(donnees)
            ecrire_csv(FILENAME_MEDECINS, medecins)
            charger()
            for champ in champs:
                champ.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    def remplir(event):
        selection = tableau.selection()
        if selection:
            ligne = tableau.item(selection[0])["values"]
            for champ, val in zip(champs, ligne):
                champ.delete(0, tk.END)
                champ.insert(0, val)

    def modifier():
        selection = tableau.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un médecin.")
            return
        nouvelles = [champ.get() for champ in champs]
        if not valider_entrees(nouvelles, is_medecin=True):
            return
        medecins = lire_csv(FILENAME_MEDECINS)
        medecins[tableau.index(selection[0])] = nouvelles
        ecrire_csv(FILENAME_MEDECINS, medecins)
        charger()

    def supprimer():
        selection = tableau.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un médecin.")
            return
        medecins = lire_csv(FILENAME_MEDECINS)
        del medecins[tableau.index(selection[0])]
        ecrire_csv(FILENAME_MEDECINS, medecins)
        charger()
        for champ in champs:
            champ.delete(0, tk.END)

    cadre_btns = ttk.Frame(fenetre)
    cadre_btns.pack(pady=15)

    for i, (texte, action) in enumerate([
        ("Ajouter", ajouter), ("Modifier", modifier), ("Supprimer", supprimer)
    ]):
        btn = ttk.Button(cadre_btns, text=texte, command=action)
        btn.grid(row=0, column=i, padx=10, ipadx=10, ipady=5)

    tableau.bind("<<TreeviewSelect>>", remplir)
    charger()