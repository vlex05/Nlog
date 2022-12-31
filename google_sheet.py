import os
import pandas as pd
import gspread
from src import config

class GoogleSheet:    
    def __init__(self, service_account_file_path = config.SERVICE_ACCOUNT_FILE_PATH, google_sheet_file_name = config.GOOGLE_SHEET_FILE_NAME, google_sheet_tab_name = config.GOOGLE_SHEET_TAB_NAME, want_default_tab = True):
        self.service_account_file_path = service_account_file_path
        self.google_sheet_file_name = google_sheet_file_name
        self.google_sheet_tab_name = google_sheet_tab_name
        self.gspread_service_account = None
        self.google_sheet_file = None
        self.google_sheet_tab = None
        self.dataframe = None
        self.want_default_tab = want_default_tab
        self.connect_google_sheet()
        if self.want_default_tab:
            self.open_google_sheet_dataframe()

    def connect_google_sheet(self):
        if not os.path.exists(self.service_account_file_path):
            print("Le fichier de service fourni n'existe pas. Vérifiez le chemin du fichier.")
            return
        try:
            self.gspread_service_account = gspread.service_account(filename=self.service_account_file_path)
        except Exception as e:
            print("Impossible de se connecter à Google Sheets. Vérifiez votre connexion internet.\n",e)
            return
    
    def open_google_sheet_file(self):
        self.connect_google_sheet()
        try:
            sheets = self.gspread_service_account.openall()
            if self.google_sheet_file_name not in [sheet.title for sheet in sheets]:
                raise Exception("La feuille de calcul n'existe pas")
            self.google_sheet_file = self.gspread_service_account.open(title=self.google_sheet_file_name)
        except Exception as e:
            print(f"La feuille de calcul '{self.google_sheet_file_name}' n'a pas été trouvée dans Google Sheet. "
                  f"Vérifiez votre connexion internet et le nom de la feuille de calcul.")
            print(e)
            return
        
    def open_google_sheet_tab(self, change_tab=False, change_google_sheet_tab_name=None):
        self.open_google_sheet_file()
        try:
            if change_tab:
                self.google_sheet_tab_name = change_google_sheet_tab_name
            tabs = self.google_sheet_file.worksheets()
            if self.google_sheet_tab_name not in [tab.title for tab in tabs]:
                raise Exception("L'onglet n'existe pas")
            self.google_sheet_tab = self.google_sheet_file.worksheet(self.google_sheet_tab_name)
        except Exception as e:
            if change_tab:
                print(f"Impossible de trouver l'onglet '{change_google_sheet_tab_name}' dans le document '{self.google_sheet_file_name}'. "
                      f"Vérifiez le titre de l'onglet.")
            else:
                print(f"Impossible de trouver l'onglet '{self.google_sheet_tab_name}' dans le document '{self.google_sheet_file_name}'. "
                      f"Vérifiez le titre de l'onglet.")
            print(e)
            return
        
    def open_google_sheet_dataframe(self):
        if self.want_default_tab:
            self.open_google_sheet_tab()
        try:
            dataframe = pd.DataFrame(self.google_sheet_tab.get_all_records())
            if dataframe.isnull().values.any():
                raise ValueError("Le DataFrame contient des données manquantes")
            self.dataframe = dataframe
        except ValueError as e:
            print("Le DataFrame contient des données manquantes. Vérifiez que les données de la feuille de calcul sont complètes.")
            print(e)
            return
        except Exception as e:
            print("Impossible de récupérer les données de la feuille de calcul. Vérifiez votre connexion internet et le nom de la feuille de calcul.")
            print(e)
            return




