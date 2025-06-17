# lang.py

translations = {
    "fr": {
        "title": "Connexion - Gestion Hospitalière",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login": "Se connecter",
        "success": "Connexion réussie !",
        "error_login": "Nom d'utilisateur ou mot de passe incorrect.",
        "error_fields": "Tous les champs doivent être remplis.",
        "error_id": "L'ID doit être un nombre.",
        "error_age": "L'âge doit être un nombre.",
        "lang": "English"
    },
    "en": {
        "title": "Login - Hospital Management",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "success": "Login successful!",
        "error_login": "Incorrect username or password.",
        "error_fields": "All fields must be filled.",
        "error_id": "ID must be a number.",
        "error_age": "Age must be a number.",
        "lang": "Français"
    }
}

current_lang = "fr"

def t(key):
    return translations[current_lang].get(key, key)

def switch_lang():
    global current_lang
    current_lang = "en" if current_lang == "fr" else "fr"
