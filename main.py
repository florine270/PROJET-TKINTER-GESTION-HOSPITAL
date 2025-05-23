import tkinter as tk
from tkinter import ttk, messagebox
from connexion import USERNAME, PASSWORD
from interfaces import ouvrir_interface_patients, ouvrir_interface_medecins, styliser

def interface_connexion():
    def verifier_connexion():
        if champ_user.get() == USERNAME and champ_pass.get() == PASSWORD:
            fenetre_connexion.destroy()
            ouvrir_menu_principal()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    fenetre_connexion = tk.Tk()
    fenetre_connexion.title("Connexion")
    fenetre_connexion.geometry("400x250")
    fenetre_connexion.configure(bg="#f7f9fc")
    styliser()

    tk.Label(fenetre_connexion, text="Connexion", font=("Arial", 16, "bold"), bg="#f7f9fc").pack(pady=20)
    cadre = ttk.Frame(fenetre_connexion)
    cadre.pack()

    ttk.Label(cadre, text="Utilisateur :").grid(row=0, column=0, padx=10, pady=10)
    champ_user = ttk.Entry(cadre)
    champ_user.grid(row=0, column=1)

    ttk.Label(cadre, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=10)
    champ_pass = ttk.Entry(cadre, show="*")
    champ_pass.grid(row=1, column=1)

    ttk.Button(fenetre_connexion, text="Se connecter", command=verifier_connexion).pack(pady=20)
    fenetre_connexion.mainloop()

def ouvrir_menu_principal():
    menu = tk.Tk()
    menu.title("Menu Principal")
    menu.geometry("400x300")
    menu.configure(bg="#f0f4f8")

    tk.Label(menu, text="Menu Principal", font=("Arial", 20, "bold"), bg="#f0f4f8").pack(pady=20)
    ttk.Button(menu, text="Gérer les Patients", command=ouvrir_interface_patients).pack(pady=10)
    ttk.Button(menu, text="Gérer les Médecins", command=ouvrir_interface_medecins).pack(pady=10)
    ttk.Button(menu, text="Quitter", command=menu.destroy).pack(pady=20)

    menu.mainloop()

# Point d'entrée
if __name__ == "__main__":
    interface_connexion()
