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
    supprimer_medecin_bdd
)

def styliser():
    style = ttk.Style()
    style.theme_use('vista')  # Tu peux aussi essayer 'clam', 'xpnative' selon ton OS
    style.configure('Treeview', rowheight=30)

def ouvrir_interface_patients():
    fenetre = tk.Toplevel()
    fenetre.title("Gestion des Patients")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#F3E8FF")
    styliser()

    # === Conteneur défilable ===
    canevas = tk.Canvas(fenetre, bg="#F3E8FF")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canevas.yview)
    cadre_scrollable = ttk.Frame(canevas)

    cadre_scrollable.bind(
        "<Configure>",
        lambda e: canevas.configure(scrollregion=canevas.bbox("all"))
    )

    canevas.create_window((0, 0), window=cadre_scrollable, anchor="nw")
    canevas.configure(yscrollcommand=scrollbar.set)

    canevas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === Barre de recherche ===
    recherche_var = tk.StringVar()
    champ_recherche = tk.Entry(cadre_scrollable, textvariable=recherche_var, width=40)
    champ_recherche.pack(pady=10)

    colonnes = ["ID", "Nom", "Prénom", "Date de Naissance", "Sexe", "Adresse", "Remarque"]
    champs = []

    cadre_form = ttk.Frame(cadre_scrollable)
    cadre_form.pack(pady=10, padx=20)

    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="groove")
    form_bg.pack()

    for i, col in enumerate(colonnes):
        label = ttk.Label(form_bg, text=col + " :", foreground="#333", background="white")
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

    tableau = ttk.Treeview(cadre_scrollable, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(expand=True, fill="both", pady=10, padx=20)

    def filtrer_tableau():
        texte = recherche_var.get().lower()
        for ligne in tableau.get_children():
            valeurs = tableau.item(ligne)['values']
            contenu = " ".join(str(v).lower() for v in valeurs)
            if texte in contenu:
                tableau.reattach(ligne, '', 'end')
            else:
                tableau.detach(ligne)

    recherche_var.trace_add("write", lambda *args: filtrer_tableau())

    def charger():
        tableau.delete(*tableau.get_children())
        for ligne in lire_patients_bdd():
            tableau.insert("", "end", values=ligne)

    def ajouter():
        donnees = [champ.get() for champ in champs]
        try:
            donnees[3] = datetime.strptime(donnees[3], "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Le format de la date doit être jj/mm/aaaa")
            return
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
        try:
            donnees[3] = datetime.strptime(donnees[3], "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Le format de la date doit être jj/mm/aaaa")
            return
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

    for i, (texte, action) in enumerate([
        ("Ajouter", ajouter), ("Modifier", modifier), ("Supprimer", supprimer)
    ]):
        btn = ttk.Button(cadre_btns, text=texte, command=action)
        btn.grid(row=0, column=i, padx=10, ipadx=10, ipady=5)

    btn_recharger = ttk.Button(cadre_btns, text="Recharger", command=charger)
    btn_recharger.grid(row=0, column=3, padx=10, ipadx=10, ipady=5)

    tableau.bind("<<TreeviewSelect>>", remplir)
    charger()

def ouvrir_interface_medecins():
    fenetre = tk.Toplevel()
    fenetre.title("Gestion des Médecins")
    fenetre.geometry("900x600")
    fenetre.configure(bg="#E6F4EA")
    styliser()

    # === Conteneur défilable ===
    canevas = tk.Canvas(fenetre, bg="#E6F4EA")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canevas.yview)
    cadre_scrollable = ttk.Frame(canevas)

    cadre_scrollable.bind(
        "<Configure>",
        lambda e: canevas.configure(scrollregion=canevas.bbox("all"))
    )

    canevas.create_window((0, 0), window=cadre_scrollable, anchor="nw")
    canevas.configure(yscrollcommand=scrollbar.set)

    canevas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === Barre de recherche ===
    recherche_var = tk.StringVar()
    champ_recherche = tk.Entry(cadre_scrollable, textvariable=recherche_var, width=40)
    champ_recherche.pack(pady=10)

    colonnes = ["ID", "Nom", "Prénom", "Spécialité", "Téléphone", "Email", "Adresse"]
    champs = []

    cadre_form = ttk.Frame(cadre_scrollable)
    cadre_form.pack(pady=10, padx=20)

    form_bg = tk.Frame(cadre_form, bg="white", bd=2, relief="groove")
    form_bg.pack()

    for i, col in enumerate(colonnes):
        label = ttk.Label(form_bg, text=col + " :", foreground="#2F4F2F", background="white")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        champ = ttk.Entry(form_bg, width=40)
        champ.grid(row=i, column=1, padx=10, pady=5)
        champs.append(champ)

    tableau = ttk.Treeview(cadre_scrollable, columns=colonnes, show="headings")
    for col in colonnes:
        tableau.heading(col, text=col)
        tableau.column(col, width=120)
    tableau.pack(expand=True, fill="both", pady=10, padx=20)

    def filtrer_tableau():
        texte = recherche_var.get().lower()
        for ligne in tableau.get_children():
            valeurs = tableau.item(ligne)['values']
            contenu = " ".join(str(v).lower() for v in valeurs)
            if texte in contenu:
                tableau.reattach(ligne, '', 'end')
            else:
                tableau.detach(ligne)

    recherche_var.trace_add("write", lambda *args: filtrer_tableau())

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

    for i, (texte, action) in enumerate([
        ("Ajouter", ajouter), ("Modifier", modifier), ("Supprimer", supprimer)
    ]):
        btn = ttk.Button(cadre_btns, text=texte, command=action)
        btn.grid(row=0, column=i, padx=10, ipadx=10, ipady=5)

    btn_recharger = ttk.Button(cadre_btns, text="Recharger", command=charger)
    btn_recharger.grid(row=0, column=3, padx=10, ipadx=10, ipady=5)

    tableau.bind("<<TreeviewSelect>>", remplir)
    charger()
