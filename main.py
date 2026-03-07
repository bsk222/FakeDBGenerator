import sys
import subprocess
import os
import random
import threading
from datetime import datetime
import webbrowser

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

print("Vérification des dépendances...")
for pkg in ["faker", "pandas", "customtkinter", "openpyxl", "pyarrow"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        install(pkg)

import customtkinter as ctk
from faker import Faker
import pandas as pd

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("2xOneFakeDbGenerator")
        self.geometry("1480x1020")
        self.resizable(True, True)

        self.faker = None
        self.selected_fields = []
        self.selected_index = -1

        self.real_email_domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
            "orange.fr", "free.fr", "sfr.fr", "laposte.net", "wanadoo.fr",
            "live.fr", "msn.com", "protonmail.com", "yahoo.fr", "bbox.fr", "gmx.fr"
        ]

        self.templates = {
            "Aucun": [],
            "CAF (Allocataires)": ["Prénom", "Nom", "Date de naissance", "Adresse complète", "Ville", "Code postal", "Téléphone", "Email", "Numéro de sécurité sociale", "IBAN"],
            "Pôle Emploi / France Travail": ["Prénom", "Nom", "Date de naissance", "Adresse complète", "Ville", "Code postal", "Téléphone", "Email", "Numéro de sécurité sociale"],
            "CPAM - Ameli (Carte Vitale)": ["Prénom", "Nom", "Date de naissance", "Numéro de sécurité sociale", "Adresse complète", "Ville", "Code postal", "Téléphone", "Email"],
            "DGFiP - Impôts.gouv": ["Prénom", "Nom", "Adresse complète", "Ville", "Code postal", "Date de naissance", "Numéro de sécurité sociale", "Identifiant fiscal"],
            "ANTS (Permis / Titres)": ["Prénom", "Nom", "Date de naissance", "Adresse complète", "Ville", "Code postal", "Numéro de sécurité sociale", "Pays"],
            "SFR / Bouygues Telecom": ["Prénom", "Nom", "Téléphone", "Email", "Adresse complète", "Ville", "Code postal", "IBAN", "Numéro de sécurité sociale", "Mots de passe"],
            "Banque (Crédit Agricole / BNP / Société Générale)": ["Prénom", "Nom", "IBAN", "BIC", "Numéro de carte bancaire", "Date d'expiration carte", "Code CVV", "Adresse complète", "Téléphone"],
            "Assurance (AXA / MAIF / Allianz)": ["Prénom", "Nom", "Téléphone", "Email", "Adresse complète", "Date de naissance", "Numéro de sécurité sociale", "IBAN"],
            "SNCF Voyageurs": ["Prénom", "Nom", "Date de naissance", "Adresse complète", "Ville", "Code postal", "Email", "Téléphone"],
            "EDF / Engie (Énergie)": ["Prénom", "Nom", "Adresse complète", "Ville", "Code postal", "Téléphone", "Email", "IBAN"],
            "La Poste (Colis / Courrier)": ["Prénom", "Nom", "Adresse complète", "Ville", "Code postal", "Téléphone", "Email"],
            "RSA / Aides Sociales": ["Prénom", "Nom", "Date de naissance", "Adresse complète", "Ville", "Code postal", "Téléphone", "Email", "Numéro de sécurité sociale", "IBAN"],
            "Streaming & Services (Netflix, Spotify...)": ["Prénom", "Nom", "Email", "Mots de passe", "Adresse IP", "Pays", "Téléphone"]
        }

        self.available_fields = [
            "Prénom", "Nom", "Email", "Téléphone", "Adresse complète", "Ville", "Code postal", "Pays",
            "Date de naissance", "Âge", "IBAN", "BIC", "SIREN", "SIRET", "Numéro de sécurité sociale",
            "Nom de société", "Métier", "Nom d'utilisateur", "Mots de passe", "Adresse IP",
            "URL de site web", "Avatar URL", "Coordonnées GPS", "Couleur préférée",
            "Numéro de carte bancaire", "Email professionnel", "Date d'expiration carte", "Code CVV",
            "Site web personnel", "Numéro de TVA", "Profession avancée", "Entreprise avancée",
            "Adresse email secondaire", "Coordonnées GPS précises", "Photo de profil HD",
            "Numéro de compte bancaire", "Identifiant fiscal", "Nom de rue seul", "Complément d'adresse",
            "Latitude seule", "Longitude seule", "Code pays ISO", "Langue parlée", "Devise utilisée",
            "Numéro de téléphone fixe", "Numéro de téléphone mobile"
        ]

        self.create_widgets()

    def create_widgets(self):
        # ==================== HEADER ORANGE ====================
        self.header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=110)
        self.header.pack(fill="x", padx=0, pady=0)
        self.header.pack_propagate(False)
        ctk.CTkLabel(self.header, text="2xOneFakeDbGenerator", font=ctk.CTkFont(size=46, weight="bold")).pack(pady=(22, 0))
        ctk.CTkLabel(self.header, text="Le plus rapide • Le plus réaliste", font=ctk.CTkFont(size=18), text_color="#FF8800").pack()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # ==================== LEFT PANEL ====================
        self.left_panel = ctk.CTkFrame(self.main_frame, width=360, corner_radius=20)
        self.left_panel.pack(side="left", fill="y", padx=(0, 20), pady=10)

        ctk.CTkLabel(self.left_panel, text="Langue", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=25, pady=(25, 8))
        self.lang_var = ctk.StringVar(value="fr_FR")
        self.lang_menu = ctk.CTkOptionMenu(self.left_panel, values=["fr_FR", "en_US", "de_DE", "es_ES", "it_IT", "pt_BR", "ru_RU"], variable=self.lang_var, height=42, font=ctk.CTkFont(size=14))
        self.lang_menu.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(self.left_panel, text="Nombre de lignes (max 50M)", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=25, pady=(25, 8))
        self.rows_var = ctk.IntVar(value=100000)
        self.rows_entry = ctk.CTkEntry(self.left_panel, textvariable=self.rows_var, placeholder_text="Ex: 50000000", height=45, font=ctk.CTkFont(size=16))
        self.rows_entry.pack(fill="x", padx=25, pady=5)
        self.rows_slider = ctk.CTkSlider(self.left_panel, from_=1000, to=50000000, number_of_steps=2000, variable=self.rows_var, height=22)
        self.rows_slider.pack(fill="x", padx=25, pady=12)

        ctk.CTkLabel(self.left_panel, text="Format de sortie", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=25, pady=(15, 8))
        self.format_var = ctk.StringVar(value="CSV")
        self.format_menu = ctk.CTkOptionMenu(self.left_panel, values=["CSV", "Excel (.xlsx)", "JSON", "SQLite (.db)", "Parquet"], variable=self.format_var, height=42, font=ctk.CTkFont(size=14))
        self.format_menu.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(self.left_panel, text="Templates DB réalistes", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=25, pady=(30, 8))
        self.template_var = ctk.StringVar(value="Aucun")
        self.template_menu = ctk.CTkOptionMenu(self.left_panel, values=list(self.templates.keys()), variable=self.template_var, height=42, font=ctk.CTkFont(size=14), command=self.load_template)
        self.template_menu.pack(fill="x", padx=25, pady=5)

        # ==================== CENTER ====================
        self.center_panel = ctk.CTkFrame(self.main_frame, corner_radius=20)
        self.center_panel.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(self.center_panel, text="Champs disponibles", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=20, pady=(15, 8))
        self.list_available = ctk.CTkScrollableFrame(self.center_panel, height=380)
        self.list_available.pack(fill="x", padx=20, pady=8)

        for field in self.available_fields:
            btn = ctk.CTkButton(self.list_available, text=field, height=36, anchor="w", font=ctk.CTkFont(size=13), corner_radius=10, command=lambda f=field: self.add_field(f))
            btn.pack(fill="x", padx=10, pady=3)

        ctk.CTkLabel(self.center_panel, text="Champs sélectionnés (dans l'ordre)", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=20, pady=(25, 8))
        self.list_selected_frame = ctk.CTkScrollableFrame(self.center_panel, height=380)
        self.list_selected_frame.pack(fill="x", padx=20, pady=8)

        self.move_frame = ctk.CTkFrame(self.center_panel)
        self.move_frame.pack(pady=12)
        self.btn_up = ctk.CTkButton(self.move_frame, text="↑ Monter", width=130, height=40, font=ctk.CTkFont(size=14), command=self.move_up)
        self.btn_up.pack(side="left", padx=10)
        self.btn_down = ctk.CTkButton(self.move_frame, text="↓ Descendre", width=130, height=40, font=ctk.CTkFont(size=14), command=self.move_down)
        self.btn_down.pack(side="left", padx=10)

        # ==================== RIGHT PANEL (avec crédits intégrés) ====================
        self.right_panel = ctk.CTkFrame(self.main_frame, width=380, corner_radius=20)
        self.right_panel.pack(side="right", fill="y", padx=(15, 0), pady=10)

        self.label_status = ctk.CTkLabel(self.right_panel, text="Prêt à générer", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_status.pack(pady=(30, 10))

        self.progress = ctk.CTkProgressBar(self.right_panel, height=18, corner_radius=10, progress_color="#FF8800")
        self.progress.pack(fill="x", padx=35, pady=12)
        self.progress.set(0)

        self.progress_percent = ctk.CTkLabel(self.right_panel, text="0 %", font=ctk.CTkFont(size=18, weight="bold"))
        self.progress_percent.pack(pady=5)

        self.btn_generate = ctk.CTkButton(self.right_panel, text="GÉNÉRER MAINTENANT", font=ctk.CTkFont(size=22, weight="bold"), height=75, fg_color="#FF8800", hover_color="#FF6600", corner_radius=15, command=self.start_generation)
        self.btn_generate.pack(pady=30, padx=35, fill="x")

        self.label_result = ctk.CTkLabel(self.right_panel, text="", font=ctk.CTkFont(size=14), wraplength=320, justify="left")
        self.label_result.pack(pady=10)

        # CRÉDITS BIEN VISIBLES ICI (plus jamais coupé)
        self.credits_label = ctk.CTkLabel(self.right_panel, text="Owner / Développeur : bsk222", font=ctk.CTkFont(size=16, weight="bold"), text_color="#FF8800", cursor="hand2")
        self.credits_label.pack(side="bottom", pady=20)
        self.credits_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bsk222"))

        self.refresh_selected_list()

    def load_template(self, *args):
        name = self.template_var.get()
        if name != "Aucun":
            self.selected_fields = self.templates[name][:]
            self.refresh_selected_list()

    def add_field(self, field):
        if field not in self.selected_fields:
            self.selected_fields.append(field)
            self.refresh_selected_list()

    def remove_field(self, field):
        if field in self.selected_fields:
            self.selected_fields.remove(field)
            if self.selected_index >= len(self.selected_fields):
                self.selected_index = len(self.selected_fields) - 1
            self.refresh_selected_list()

    def refresh_selected_list(self):
        for w in self.list_selected_frame.winfo_children():
            w.destroy()
        for i, field in enumerate(self.selected_fields):
            frame = ctk.CTkFrame(self.list_selected_frame, corner_radius=12)
            frame.pack(fill="x", padx=12, pady=5)
            label = ctk.CTkLabel(frame, text=field, anchor="w", font=ctk.CTkFont(size=13))
            label.pack(side="left", padx=18, fill="x", expand=True)
            btn_remove = ctk.CTkButton(frame, text="✕", width=34, height=34, fg_color="#ff3333", hover_color="#cc0000", corner_radius=8, command=lambda f=field: self.remove_field(f))
            btn_remove.pack(side="right", padx=10)
            frame.bind("<Button-1>", lambda e, idx=i: self.select_item(idx))
            label.bind("<Button-1>", lambda e, idx=i: self.select_item(idx))

    def select_item(self, index):
        self.selected_index = index
        self.highlight_selection()

    def highlight_selection(self):
        for i, frame in enumerate(self.list_selected_frame.winfo_children()):
            frame.configure(fg_color="#2a6f97" if i == self.selected_index else "transparent")

    def move_up(self):
        if self.selected_index > 0:
            self.selected_fields[self.selected_index], self.selected_fields[self.selected_index-1] = self.selected_fields[self.selected_index-1], self.selected_fields[self.selected_index]
            self.selected_index -= 1
            self.refresh_selected_list()

    def move_down(self):
        if self.selected_index < len(self.selected_fields) - 1:
            self.selected_fields[self.selected_index], self.selected_fields[self.selected_index+1] = self.selected_fields[self.selected_index+1], self.selected_fields[self.selected_index]
            self.selected_index += 1
            self.refresh_selected_list()

    def start_generation(self):
        if not self.selected_fields:
            self.label_status.configure(text="Sélectionne au moins un champ", text_color="red")
            return
        self.btn_generate.configure(state="disabled")
        self.label_status.configure(text="Génération en cours...", text_color="#FF8800")
        self.progress.set(0)
        self.progress_percent.configure(text="0 %")
        thread = threading.Thread(target=self.generate_data, daemon=True)
        thread.start()

    def generate_data(self):
        try:
            self.faker = Faker(self.lang_var.get())
            num_rows = max(1, self.rows_var.get())

            FIELDS_MAP = {
                "Prénom":"first_name","Nom":"last_name","Email":"email","Téléphone":"phone_number",
                "Adresse complète":"address","Ville":"city","Code postal":"postcode","Pays":"country",
                "Date de naissance":"date_of_birth","IBAN":"iban","BIC":"swift","SIREN":"siren",
                "SIRET":"siret","Numéro de sécurité sociale":"ssn","Nom de société":"company",
                "Métier":"job","Nom d'utilisateur":"user_name","Adresse IP":"ipv4","URL de site web":"url",
                "Couleur préférée":"color_name","Numéro de carte bancaire":"credit_card_number",
                "Date d'expiration carte":"credit_card_expire","Code CVV":"credit_card_security_code",
                "Site web personnel":"domain_name","Numéro de TVA":"vat_id","Profession avancée":"job",
                "Entreprise avancée":"company","Nom de rue seul":"street_address","Complément d'adresse":"secondary_address",
                "Code pays ISO":"country_code","Langue parlée":"language_name","Devise utilisée":"currency_name",
                "Numéro de téléphone fixe":"phone_number","Numéro de téléphone mobile":"phone_number"
            }

            data = {}
            for idx, field in enumerate(self.selected_fields):
                if field == "Âge":
                    data[field] = [random.randint(18, 85) for _ in range(num_rows)]
                elif field == "Mots de passe":
                    data[field] = [self.faker.password(length=12) for _ in range(num_rows)]
                elif field in ["Avatar URL", "Photo de profil HD"]:
                    data[field] = [f"https://picsum.photos/id/{random.randint(1,9999)}/800/600" for _ in range(num_rows)]
                elif field in ["Coordonnées GPS", "Coordonnées GPS précises"]:
                    data[field] = [f"{self.faker.location_on_land()[0]}, {self.faker.location_on_land()[1]}" for _ in range(num_rows)]
                elif field == "Latitude seule":
                    data[field] = [self.faker.location_on_land()[0] for _ in range(num_rows)]
                elif field == "Longitude seule":
                    data[field] = [self.faker.location_on_land()[1] for _ in range(num_rows)]
                elif field in ["Email", "Email professionnel", "Adresse email secondaire"]:
                    data[field] = [f"{self.faker.user_name()}@{random.choice(self.real_email_domains)}" for _ in range(num_rows)]
                elif field in ["Téléphone", "Numéro de téléphone fixe", "Numéro de téléphone mobile"]:
                    data[field] = ["0" + random.choice(["6", "7"]) + "".join(random.choices("0123456789", k=8)) for _ in range(num_rows)]
                elif field == "Adresse complète":
                    data[field] = [self.faker.address().replace("\n", ", ") for _ in range(num_rows)]
                else:
                    method = FIELDS_MAP.get(field, "word")
                    data[field] = [getattr(self.faker, method)() for _ in range(num_rows)]

                progress = (idx + 1) / len(self.selected_fields)
                if idx % 3 == 0 or idx == len(self.selected_fields) - 1:
                    self.after(0, lambda p=progress: (self.progress.set(p), self.progress_percent.configure(text=f"{int(p*100)} %")))

            df = pd.DataFrame(data)
            df = df.map(lambda x: str(x).replace("\n", " ").replace("\r", " ") if isinstance(x, str) else x)

            output_dir = "donnees_generees"
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"donnees_factices_{timestamp}"
            filepath = os.path.join(output_dir, filename)

            fmt = self.format_var.get()
            if fmt == "CSV":
                final_path = f"{filepath}.csv"
                df.to_csv(final_path, index=False, encoding="utf-8")
            elif fmt == "Excel (.xlsx)":
                final_path = f"{filepath}.xlsx"
                df.to_excel(final_path, index=False)
            elif fmt == "JSON":
                final_path = f"{filepath}.json"
                df.to_json(final_path, orient="records", force_ascii=False, indent=2)
            elif fmt == "SQLite (.db)":
                import sqlite3
                final_path = f"{filepath}.db"
                conn = sqlite3.connect(final_path)
                df.to_sql("records", conn, if_exists="replace", index=False)
                conn.close()
            else:
                final_path = f"{filepath}.parquet"
                df.to_parquet(final_path, index=False)

            self.after(0, lambda: self.finish_generation(output_dir, final_path, num_rows))

        except Exception as e:
            self.after(0, lambda e=e: (self.label_status.configure(text=f"Erreur : {str(e)}", text_color="red"), self.btn_generate.configure(state="normal")))

    def finish_generation(self, output_dir, final_path, num_rows):
        self.label_status.configure(text="Génération terminée avec succès !", text_color="#FF8800")
        self.label_result.configure(text=f"Fichier créé :\n{os.path.basename(final_path)}\n\n{num_rows:,} lignes (1 ligne = 1 personne)".replace(',', ' '))
        self.progress.set(1)
        self.progress_percent.configure(text="100 %")
        self.btn_generate.configure(state="normal")

        try:
            dir_path = os.path.abspath(output_dir)
            if os.name == "nt":
                subprocess.Popen(['explorer', dir_path])
            elif sys.platform == "darwin":
                subprocess.Popen(['open', dir_path])
            else:
                subprocess.Popen(['xdg-open', dir_path])
        except:
            pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
