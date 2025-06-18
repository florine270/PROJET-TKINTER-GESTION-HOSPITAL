import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from connexion import (
    valider_entrees,
    lire_patients_bdd,
    ajouter_patient_bdd,
    modifier_patient_bdd,
    supprimer_patient_bdd,
    lire_medecins_bdd,
    ajouter_medecin_bdd,
    modifier_medecin_bdd,
    supprimer_medecin_bdd,
    ajouter_resultat_labo,
    lire_resultats_labo,
    ajouter_rendez_vous,
    lire_rendez_vous
)

def styliser():
    style = ttk.Style()
    try:
        style.theme_use('vista')  # ou 'clam' si vista n'existe pas
    except:
        style.theme_use('default')
    style.configure('Treeview', rowheight=30)
def ouvrir_interface_patients():
    fenetre = tk.Toplevel()
    fenetre.title("Gestion des Patients")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#F3E8FF")
    styliser()

    canevas = tk.Canvas(fenetre, bg="#F3E8FF")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canevas.yview)
    cadre_scrollable = ttk.Frame(canevas)
    cadre_scrollable.bind("<Configure>", lambda e: canevas.configure(scrollregion=canevas.bbox("all")))
    canevas.create_window((0, 0), window=cadre_scrollable, anchor="nw")
    canevas.configure(yscrollcommand=scrollbar.set)
    canevas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    colonnes = ["ID", "Nom", "Prénom", "Date de Naissance", "Sexe", "Adresse", "Remarque"]
    champs = []
    cadre_form = ttk.Frame(cadre_scrollable)
    cadre_form.pack(pady=10, padx=20)
    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="groove")
    form_bg.pack()

    for i, col in enumerate(colonnes):
        label = ttk.Label(form_bg, text=col + " :", background="white")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        champ = ttk.Combobox(form_bg, values=["Homme", "Femme"], state="readonly", width=37) if col == "Sexe" else ttk.Entry(form_bg, width=40)
        champ.grid(row=i, column=1, padx=10, pady=5)
        champs.append(champ)

    tableau = ttk.Treeview(cadre_scrollable, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(fill="both", expand=True, pady=10, padx=20)

    def charger():
        tableau.delete(*tableau.get_children())
        for ligne in lire_patients_bdd():
            tableau.insert("", "end", values=ligne)

    def ajouter():
        donnees = [champ.get() for champ in champs]
        if valider_entrees(donnees):
            ajouter_patient_bdd(donnees)
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
        donnees = [champ.get() for champ in champs]
        if valider_entrees(donnees):
            modifier_patient_bdd(donnees)
            charger()

    def supprimer():
        selection = tableau.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un patient.")
            return
        patient_id = tableau.item(selection[0])["values"][0]
        supprimer_patient_bdd(patient_id)
        charger()
        for champ in champs:
            champ.delete(0, tk.END)

    cadre_btns = ttk.Frame(cadre_scrollable)
    cadre_btns.pack(pady=15)
    for i, (texte, action) in enumerate([("Ajouter", ajouter), ("Modifier", modifier), ("Supprimer", supprimer)]):
        btn = ttk.Button(cadre_btns, text=texte, command=action)
        btn.grid(row=0, column=i, padx=10, ipadx=10, ipady=5)
    ttk.Button(cadre_btns, text="Recharger", command=charger).grid(row=0, column=3, padx=10, ipadx=10, ipady=5)

    tableau.bind("<<TreeviewSelect>>", remplir)
    charger()
def ouvrir_interface_medecins():
    fenetre = tk.Toplevel()
    fenetre.title("Gestion des Médecins")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#E6F4EA")
    styliser()

    canevas = tk.Canvas(fenetre, bg="#E6F4EA")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canevas.yview)
    cadre_scrollable = ttk.Frame(canevas)
    cadre_scrollable.bind("<Configure>", lambda e: canevas.configure(scrollregion=canevas.bbox("all")))
    canevas.create_window((0, 0), window=cadre_scrollable, anchor="nw")
    canevas.configure(yscrollcommand=scrollbar.set)
    canevas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    colonnes = ["ID", "Nom", "Prénom", "Spécialité", "Téléphone", "Email", "Adresse"]
    champs = []
    cadre_form = ttk.Frame(cadre_scrollable)
    cadre_form.pack(pady=10, padx=20)
    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="groove")
    form_bg.pack()

    for i, col in enumerate(colonnes):
        label = ttk.Label(form_bg, text=col + " :", background="white")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        champ = ttk.Entry(form_bg, width=40)
        champ.grid(row=i, column=1, padx=10, pady=5)
        champs.append(champ)

    tableau = ttk.Treeview(cadre_scrollable, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(expand=True, fill="both", pady=10, padx=20)

    def charger():
        tableau.delete(*tableau.get_children())
        for ligne in lire_medecins_bdd():
            tableau.insert("", "end", values=ligne)

    def ajouter():
        donnees = [champ.get() for champ in champs]
        if valider_entrees(donnees, is_medecin=True):
            ajouter_medecin_bdd(donnees)
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
            messagebox.showerror("Erreur", "Sélectionnez un médecin.")
            return
        donnees = [champ.get() for champ in champs]
        if valider_entrees(donnees, is_medecin=True):
            modifier_medecin_bdd(donnees)
            charger()

    def supprimer():
        selection = tableau.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un médecin.")
            return
        medecin_id = tableau.item(selection[0])["values"][0]
        supprimer_medecin_bdd(medecin_id)
        charger()
        for champ in champs:
            champ.delete(0, tk.END)

    cadre_btns = ttk.Frame(cadre_scrollable)
    cadre_btns.pack(pady=15)
    for i, (texte, action) in enumerate([("Ajouter", ajouter), ("Modifier", modifier), ("Supprimer", supprimer)]):
        btn = ttk.Button(cadre_btns, text=texte, command=action)
        btn.grid(row=0, column=i, padx=10, ipadx=10, ipady=5)
    ttk.Button(cadre_btns, text="Recharger", command=charger).grid(row=0, column=3, padx=10, ipadx=10, ipady=5)

    tableau.bind("<<TreeviewSelect>>", remplir)
    charger()
def ouvrir_interface_resultats_labo():
    fenetre = tk.Toplevel()
    fenetre.title("Résultats de Laboratoire")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#E1F5FE")
    styliser()

    canevas = tk.Canvas(fenetre, bg="#E1F5FE")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canevas.yview)
    cadre_scroll = ttk.Frame(canevas)
    cadre_scroll.bind("<Configure>", lambda e: canevas.configure(scrollregion=canevas.bbox("all")))
    canevas.create_window((0, 0), window=cadre_scroll, anchor="nw")
    canevas.configure(yscrollcommand=scrollbar.set)
    canevas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    champs = {}
    colonnes = ["Patient", "Type Analyse", "Valeur", "Unité", "Interprétation", "Date Analyse"]

    cadre_form = ttk.Frame(cadre_scroll)
    cadre_form.pack(pady=10)
    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="ridge")
    form_bg.pack()

    ttk.Label(form_bg, text="Patient :", background="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    patients = lire_patients_bdd()
    noms_patients = [f"{p[0]} - {p[1]} {p[2]}" for p in patients]
    patient_combo = ttk.Combobox(form_bg, values=noms_patients, state="readonly", width=37)
    patient_combo.grid(row=0, column=1, padx=10, pady=5)
    champs["Patient"] = patient_combo

    for i, champ in enumerate(colonnes[1:], start=1):
        ttk.Label(form_bg, text=champ + " :", background="white").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = ttk.Entry(form_bg, width=40)
        if champ == "Date Analyse":
            entry.insert(0, "jj/mm/aaaa")
        entry.grid(row=i, column=1, padx=10, pady=5)
        champs[champ] = entry

    tableau = ttk.Treeview(cadre_scroll, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(fill="both", expand=True, pady=10)

    def charger():
        tableau.delete(*tableau.get_children())
        for r in lire_resultats_labo():
            tableau.insert("", "end", values=r)

    def ajouter():
        sel = champs["Patient"].get()
        if not sel:
            messagebox.showerror("Erreur", "Sélectionnez un patient.")
            return
        id_patient = int(sel.split(" - ")[0])
        donnees = [
            id_patient,
            champs["Type Analyse"].get(),
            champs["Valeur"].get(),
            champs["Unité"].get(),
            champs["Interprétation"].get(),
            champs["Date Analyse"].get()
        ]
        try:
            datetime.strptime(donnees[-1], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erreur", "Date invalide. Format attendu : jj/mm/aaaa")
            return
        ajouter_resultat_labo(donnees)
        charger()
        for champ in champs.values():
            champ.delete(0, tk.END)
        patient_combo.set("")

    cadre_btns = ttk.Frame(cadre_scroll)
    cadre_btns.pack(pady=10)
    ttk.Button(cadre_btns, text="Ajouter Résultat", command=ajouter).grid(row=0, column=0, padx=10, ipadx=10, ipady=5)
    ttk.Button(cadre_btns, text="Recharger", command=charger).grid(row=0, column=1, padx=10, ipadx=10, ipady=5)

    charger()
def ouvrir_interface_rendez_vous():
    fenetre = tk.Toplevel()
    fenetre.title("Prise de Rendez-vous")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#FFF3E0")
    styliser()

    canevas = tk.Canvas(fenetre, bg="#FFF3E0")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canevas.yview)
    cadre_scroll = ttk.Frame(canevas)
    cadre_scroll.bind("<Configure>", lambda e: canevas.configure(scrollregion=canevas.bbox("all")))
    canevas.create_window((0, 0), window=cadre_scroll, anchor="nw")
    canevas.configure(yscrollcommand=scrollbar.set)
    canevas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    champs = {}

    cadre_form = ttk.Frame(cadre_scroll)
    cadre_form.pack(pady=10)
    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="ridge")
    form_bg.pack()

    # Patient
    ttk.Label(form_bg, text="Patient :", background="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    patients = lire_patients_bdd()
    noms_patients = [f"{p[0]} - {p[1]} {p[2]}" for p in patients]
    patient_combo = ttk.Combobox(form_bg, values=noms_patients, state="readonly", width=37)
    patient_combo.grid(row=0, column=1, padx=10, pady=5)
    champs["Patient"] = patient_combo

    # Médecin
    ttk.Label(form_bg, text="Médecin :", background="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    medecins = lire_medecins_bdd()
    noms_medecins = [f"{m[0]} - {m[1]} {m[2]}" for m in medecins]
    medecin_combo = ttk.Combobox(form_bg, values=noms_medecins, state="readonly", width=37)
    medecin_combo.grid(row=1, column=1, padx=10, pady=5)
    champs["Médecin"] = medecin_combo

    # Date et Heure
    ttk.Label(form_bg, text="Date et Heure (jj/mm/aaaa hh:mm) :", background="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    champ_datetime = ttk.Entry(form_bg, width=40)
    champ_datetime.insert(0, "17/06/2025 14:30")
    champ_datetime.grid(row=2, column=1, padx=10, pady=5)
    champs["DateHeure"] = champ_datetime

    # Motif
    ttk.Label(form_bg, text="Motif :", background="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    champ_motif = ttk.Entry(form_bg, width=40)
    champ_motif.grid(row=3, column=1, padx=10, pady=5)
    champs["Motif"] = champ_motif

    # Tableau
    colonnes = ["ID", "Patient", "Médecin", "Date/Heure", "Motif"]
    tableau = ttk.Treeview(cadre_scroll, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=150)
    tableau.pack(fill="both", expand=True, pady=10)

    def charger():
        tableau.delete(*tableau.get_children())
        for rdv in lire_rendez_vous():
            tableau.insert("", "end", values=rdv)

    def ajouter():
        if not champs["Patient"].get() or not champs["Médecin"].get():
            messagebox.showerror("Erreur", "Sélectionnez un patient et un médecin.")
            return
        try:
            dt = datetime.strptime(champs["DateHeure"].get(), "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date/heure incorrect.")
            return
        id_patient = int(champs["Patient"].get().split(" - ")[0])
        id_medecin = int(champs["Médecin"].get().split(" - ")[0])
        donnees = [id_patient, id_medecin, dt.strftime("%Y-%m-%d %H:%M:%S"), champs["Motif"].get()]
        ajouter_rendez_vous(donnees)
        charger()
        for champ in champs.values():
            champ.delete(0, tk.END)
        patient_combo.set("")
        medecin_combo.set("")

    cadre_btns = ttk.Frame(cadre_scroll)
    cadre_btns.pack(pady=10)
    ttk.Button(cadre_btns, text="Ajouter Rendez-vous", command=ajouter).grid(row=0, column=0, padx=10, ipadx=10, ipady=5)
    ttk.Button(cadre_btns, text="Recharger", command=charger).grid(row=0, column=1, padx=10, ipadx=10, ipady=5)

    charger()
