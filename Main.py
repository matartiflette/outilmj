import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random
import os
from datetime import datetime

class JDRTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Outil Maître du Jeu - JDR")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Fichier de sauvegarde
        self.save_file = "jdr_data.json"
        
        # Données du jeu
        self.data = {
            'players': {},
            'story': '',
            'stuffs': []
        }
        
        # Charger les données existantes
        self.load_data()
        
        # Créer l'interface
        self.create_widgets()
        
        # Sauvegarder automatiquement à la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Style pour les onglets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#34495e')
        style.configure('TNotebook.Tab', background='#34495e', foreground='white', padding=[10, 8])
        style.map('TNotebook.Tab', background=[('selected', '#3498db')])
        
        # Création du notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Onglet 1: Stats des joueurs
        self.create_players_tab()
        
        # Onglet 2: Dés
        self.create_dice_tab()
        
        # Onglet 3: Stuffs
        self.create_stuffs_tab()
        
        # Onglet 4: Histoire
        self.create_story_tab()

    def create_players_tab(self):
        self.players_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.players_frame, text='Joueurs & Stats')
        
        # Frame pour les boutons
        btn_frame = ttk.Frame(self.players_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Ajouter Joueur", command=self.add_player).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Modifier Joueur", command=self.modify_player).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Supprimer Joueur", command=self.delete_player).pack(side='left', padx=5)
        
        # Treeview pour afficher les joueurs
        columns = ('Nom', 'Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme', 'PV', 'Niveau')
        self.players_tree = ttk.Treeview(self.players_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        for col in columns:
            self.players_tree.heading(col, text=col)
            self.players_tree.column(col, width=90)
        
        # Scrollbar pour la treeview
        scrollbar_players = ttk.Scrollbar(self.players_frame, orient='vertical', command=self.players_tree.yview)
        self.players_tree.configure(yscrollcommand=scrollbar_players.set)
        
        # Menu contextuel pour copier
        self.players_context_menu = tk.Menu(self.root, tearoff=0)
        self.players_context_menu.add_command(label="Copier les stats", command=self.copy_player_stats)
        self.players_context_menu.add_command(label="Copier tout le joueur", command=self.copy_full_player)
        
        # Bind du clic droit
        self.players_tree.bind("<Button-3>", self.show_players_context_menu)
        
        # Placement
        self.players_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar_players.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Charger les joueurs existants
        self.refresh_players_tree()

    def create_dice_tab(self):
        self.dice_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dice_frame, text='Dés')
        
        # Frame principal avec style
        main_dice_frame = tk.Frame(self.dice_frame, bg='#ecf0f1')
        main_dice_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(main_dice_frame, text="🎲 Lanceur de Dés 🎲", font=('Arial', 20, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Frame pour les boutons de dés
        dice_buttons_frame = tk.Frame(main_dice_frame, bg='#ecf0f1')
        dice_buttons_frame.pack(pady=20)
        
        # Boutons pour différents types de dés
        dice_types = [4, 6, 8, 10, 12, 20, 100]
        for i, dice in enumerate(dice_types):
            row = i // 4
            col = i % 4
            btn = tk.Button(dice_buttons_frame, text=f"D{dice}", font=('Arial', 12, 'bold'),
                           bg='#3498db', fg='white', width=8, height=2,
                           command=lambda d=dice: self.roll_dice(d))
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Frame pour lancer plusieurs dés
        multi_dice_frame = tk.Frame(main_dice_frame, bg='#ecf0f1')
        multi_dice_frame.pack(pady=20)
        
        tk.Label(multi_dice_frame, text="Nombre de dés:", bg='#ecf0f1', font=('Arial', 12)).grid(row=0, column=0, padx=5)
        self.num_dice_var = tk.StringVar(value="1")
        num_dice_entry = tk.Entry(multi_dice_frame, textvariable=self.num_dice_var, width=5, font=('Arial', 12))
        num_dice_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(multi_dice_frame, text="Type de dé:", bg='#ecf0f1', font=('Arial', 12)).grid(row=0, column=2, padx=5)
        self.dice_type_var = tk.StringVar(value="20")
        dice_combo = ttk.Combobox(multi_dice_frame, textvariable=self.dice_type_var, 
                                 values=[str(d) for d in dice_types], width=5)
        dice_combo.grid(row=0, column=3, padx=5)
        
        tk.Button(multi_dice_frame, text="Lancer", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=self.roll_multiple_dice).grid(row=0, column=4, padx=10)
        
        # Zone d'affichage des résultats
        result_frame = tk.Frame(main_dice_frame, bg='#ecf0f1')
        result_frame.pack(fill='both', expand=True, pady=20)
        
        tk.Label(result_frame, text="Résultats:", font=('Arial', 14, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack()
        
        self.dice_result = tk.Text(result_frame, height=10, font=('Arial', 11), 
                                  bg='white', fg='#2c3e50', wrap='word')
        self.dice_result.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar pour les résultats
        scrollbar_dice = ttk.Scrollbar(result_frame, command=self.dice_result.yview)
        self.dice_result.config(yscrollcommand=scrollbar_dice.set)

    def create_stuffs_tab(self):
        self.stuffs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stuffs_frame, text='Équipements')
        
        # Frame pour les boutons
        btn_frame = ttk.Frame(self.stuffs_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Ajouter Équipement", command=self.add_stuff).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Modifier Équipement", command=self.modify_stuff).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Supprimer Équipement", command=self.delete_stuff).pack(side='left', padx=5)
        
        # Listbox pour afficher les équipements
        list_frame = ttk.Frame(self.stuffs_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview pour les équipements
        columns = ('Nom', 'Type', 'Propriétaire', 'Description')
        self.stuffs_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.stuffs_tree.heading(col, text=col)
            if col == 'Description':
                self.stuffs_tree.column(col, width=300)
            else:
                self.stuffs_tree.column(col, width=120)
        
        scrollbar_stuffs = ttk.Scrollbar(list_frame, orient='vertical', command=self.stuffs_tree.yview)
        self.stuffs_tree.configure(yscrollcommand=scrollbar_stuffs.set)
        
        self.stuffs_tree.pack(side='left', fill='both', expand=True)
        scrollbar_stuffs.pack(side='right', fill='y')
        
        self.refresh_stuffs_tree()

    def create_story_tab(self):
        self.story_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.story_frame, text='Histoire')
        
        # Frame pour le titre
        title_frame = ttk.Frame(self.story_frame)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(title_frame, text="📖 Journal de Campagne", font=('Arial', 16, 'bold')).pack()
        
        # Boutons
        btn_frame = ttk.Frame(self.story_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Ajouter Entrée", command=self.add_story_entry).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Sauvegarder Histoire", command=self.save_story).pack(side='left', padx=5)
        
        # Zone de texte pour l'histoire
        text_frame = ttk.Frame(self.story_frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.story_text = tk.Text(text_frame, wrap='word', font=('Arial', 11))
        scrollbar_story = ttk.Scrollbar(text_frame, command=self.story_text.yview)
        self.story_text.config(yscrollcommand=scrollbar_story.set)
        
        self.story_text.pack(side='left', fill='both', expand=True)
        scrollbar_story.pack(side='right', fill='y')
        
        # Charger l'histoire existante
        if hasattr(self, 'story_text'):
            self.story_text.insert('1.0', self.data.get('story', ''))

    # Méthodes pour gérer les joueurs
    def add_player(self):
        dialog = PlayerDialog(self.root, "Ajouter Joueur")
        if dialog.result:
            player_data = dialog.result
            self.data['players'][player_data['name']] = player_data
            self.refresh_players_tree()
            self.save_data()

    def modify_player(self):
        selected = self.players_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un joueur à modifier.")
            return
        
        item = self.players_tree.item(selected[0])
        player_name = item['values'][0]
        
        dialog = PlayerDialog(self.root, "Modifier Joueur", self.data['players'][player_name])
        if dialog.result:
            # Supprimer l'ancien nom si changé
            if dialog.result['name'] != player_name:
                del self.data['players'][player_name]
            self.data['players'][dialog.result['name']] = dialog.result
            self.refresh_players_tree()
            self.save_data()

    def delete_player(self):
        selected = self.players_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un joueur à supprimer.")
            return
        
        item = self.players_tree.item(selected[0])
        player_name = item['values'][0]
        
        if messagebox.askyesno("Confirmer", f"Êtes-vous sûr de vouloir supprimer {player_name} ?"):
            del self.data['players'][player_name]
            self.refresh_players_tree()
            self.save_data()

    def refresh_players_tree(self):
        # Vider la treeview
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)
        
        # Ajouter tous les joueurs
        for name, player in self.data['players'].items():
            self.players_tree.insert('', 'end', values=(
                player['name'], player['force'], player['dexterite'], 
                player['constitution'], player['intelligence'], 
                player['sagesse'], player['charisme'], player['pv'], player['niveau']
            ))

    # Méthodes pour le menu contextuel
    def show_players_context_menu(self, event):
        # Sélectionner l'item sous le curseur
        item = self.players_tree.identify_row(event.y)
        if item:
            self.players_tree.selection_set(item)
            self.players_context_menu.post(event.x_root, event.y_root)

    def copy_player_stats(self):
        selected = self.players_tree.selection()
        if not selected:
            return
        
        item = self.players_tree.item(selected[0])
        values = item['values']
        
        # Copier seulement les stats (Force à Charisme)
        stats_text = f"Force: {values[1]}, Dextérité: {values[2]}, Constitution: {values[3]}, Intelligence: {values[4]}, Sagesse: {values[5]}, Charisme: {values[6]}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(stats_text)
        messagebox.showinfo("Copié", "Stats copiées dans le presse-papier !")

    def copy_full_player(self):
        selected = self.players_tree.selection()
        if not selected:
            return
        
        item = self.players_tree.item(selected[0])
        values = item['values']
        
        # Copier toutes les informations du joueur
        full_text = f"Nom: {values[0]}\nForce: {values[1]}\nDextérité: {values[2]}\nConstitution: {values[3]}\nIntelligence: {values[4]}\nSagesse: {values[5]}\nCharisme: {values[6]}\nPV: {values[7]}\nNiveau: {values[8]}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(full_text)
        messagebox.showinfo("Copié", "Informations complètes du joueur copiées dans le presse-papier !")

    # Méthodes pour les dés
    def roll_dice(self, sides):
        result = random.randint(1, sides)
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] D{sides}: {result}\n"
        self.dice_result.insert('end', message)
        self.dice_result.see('end')

    def roll_multiple_dice(self):
        try:
            num_dice = int(self.num_dice_var.get())
            dice_type = int(self.dice_type_var.get())
            
            if num_dice <= 0 or num_dice > 100:
                messagebox.showerror("Erreur", "Le nombre de dés doit être entre 1 et 100.")
                return
            
            results = [random.randint(1, dice_type) for _ in range(num_dice)]
            total = sum(results)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            message = f"[{timestamp}] {num_dice}D{dice_type}: {results} = Total: {total}\n"
            self.dice_result.insert('end', message)
            self.dice_result.see('end')
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides.")

    # Méthodes pour les équipements
    def add_stuff(self):
        dialog = StuffDialog(self.root, "Ajouter Équipement", list(self.data['players'].keys()))
        if dialog.result:
            self.data['stuffs'].append(dialog.result)
            self.refresh_stuffs_tree()
            self.save_data()

    def modify_stuff(self):
        selected = self.stuffs_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un équipement à modifier.")
            return
        
        item_index = self.stuffs_tree.index(selected[0])
        current_stuff = self.data['stuffs'][item_index]
        
        dialog = StuffDialog(self.root, "Modifier Équipement", 
                           list(self.data['players'].keys()), current_stuff)
        if dialog.result:
            self.data['stuffs'][item_index] = dialog.result
            self.refresh_stuffs_tree()
            self.save_data()

    def delete_stuff(self):
        selected = self.stuffs_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un équipement à supprimer.")
            return
        
        item_index = self.stuffs_tree.index(selected[0])
        stuff_name = self.data['stuffs'][item_index]['name']
        
        if messagebox.askyesno("Confirmer", f"Êtes-vous sûr de vouloir supprimer {stuff_name} ?"):
            del self.data['stuffs'][item_index]
            self.refresh_stuffs_tree()
            self.save_data()

    def refresh_stuffs_tree(self):
        for item in self.stuffs_tree.get_children():
            self.stuffs_tree.delete(item)
        
        for stuff in self.data['stuffs']:
            self.stuffs_tree.insert('', 'end', values=(
                stuff['name'], stuff['type'], stuff['owner'], stuff['description']
            ))

    # Méthodes pour l'histoire
    def add_story_entry(self):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        entry = f"\n--- {timestamp} ---\n"
        self.story_text.insert('end', entry)
        self.story_text.see('end')
        self.story_text.focus_set()

    def save_story(self):
        self.data['story'] = self.story_text.get('1.0', 'end-1c')
        self.save_data()
        messagebox.showinfo("Sauvegarde", "Histoire sauvegardée avec succès !")

    # Sauvegarde et chargement
    def save_data(self):
        try:
            # Sauvegarder aussi l'histoire actuelle
            self.data['story'] = self.story_text.get('1.0', 'end-1c')
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erreur de sauvegarde", f"Impossible de sauvegarder: {e}")

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception as e:
                messagebox.showerror("Erreur de chargement", f"Impossible de charger les données: {e}")

    def on_closing(self):
        self.save_data()
        self.root.destroy()


class PlayerDialog:
    def __init__(self, parent, title, initial_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Centrer la fenêtre
        self.dialog.transient(parent)
        
        # Variables
        self.name_var = tk.StringVar(value=initial_data['name'] if initial_data else '')
        self.force_var = tk.IntVar(value=initial_data['force'] if initial_data else 10)
        self.dex_var = tk.IntVar(value=initial_data['dexterite'] if initial_data else 10)
        self.con_var = tk.IntVar(value=initial_data['constitution'] if initial_data else 10)
        self.int_var = tk.IntVar(value=initial_data['intelligence'] if initial_data else 10)
        self.sag_var = tk.IntVar(value=initial_data['sagesse'] if initial_data else 10)
        self.cha_var = tk.IntVar(value=initial_data['charisme'] if initial_data else 10)
        self.pv_var = tk.IntVar(value=initial_data['pv'] if initial_data else 10)
        self.niveau_var = tk.IntVar(value=initial_data['niveau'] if initial_data else 1)
        
        self.create_widgets()
        
        # Attendre que la fenêtre se ferme
        self.dialog.wait_window()

    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Nom
        ttk.Label(main_frame, text="Nom du joueur:").grid(row=0, column=0, sticky='w', pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        name_entry.focus_set()  # Focus sur le premier champ
        
        # Stats
        stats = [
            ("Force:", self.force_var),
            ("Dextérité:", self.dex_var),
            ("Constitution:", self.con_var),
            ("Intelligence:", self.int_var),
            ("Sagesse:", self.sag_var),
            ("Charisme:", self.cha_var),
            ("Points de Vie:", self.pv_var),
            ("Niveau:", self.niveau_var)
        ]
        
        for i, (label, var) in enumerate(stats, 1):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            spin = ttk.Spinbox(main_frame, from_=1, to=100, textvariable=var, width=28)
            spin.grid(row=i, column=1, pady=5)
        
        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(stats)+1, column=0, columnspan=2, pady=20)
        
        ok_btn = ttk.Button(btn_frame, text="OK", command=self.ok_clicked)
        ok_btn.pack(side='left', padx=5)
        cancel_btn = ttk.Button(btn_frame, text="Annuler", command=self.cancel_clicked)
        cancel_btn.pack(side='left', padx=5)
        
        # Permettre d'utiliser Entrée pour valider
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())

    def ok_clicked(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide.")
            return
        
        self.result = {
            'name': self.name_var.get().strip(),
            'force': self.force_var.get(),
            'dexterite': self.dex_var.get(),
            'constitution': self.con_var.get(),
            'intelligence': self.int_var.get(),
            'sagesse': self.sag_var.get(),
            'charisme': self.cha_var.get(),
            'pv': self.pv_var.get(),
            'niveau': self.niveau_var.get()
        }
        self.dialog.destroy()

    def cancel_clicked(self):
        self.dialog.destroy()


class StuffDialog:
    def __init__(self, parent, title, players_list, initial_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.transient(parent)
        
        # Variables
        self.name_var = tk.StringVar(value=initial_data['name'] if initial_data else '')
        self.type_var = tk.StringVar(value=initial_data['type'] if initial_data else '')
        self.owner_var = tk.StringVar(value=initial_data['owner'] if initial_data else 'Aucun')
        self.desc_var = tk.StringVar(value=initial_data['description'] if initial_data else '')
        
        self.players_list = ['Aucun'] + players_list
        
        self.create_widgets()
        
        # Attendre que la fenêtre se ferme
        self.dialog.wait_window()

    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Nom
        ttk.Label(main_frame, text="Nom:").grid(row=0, column=0, sticky='w', pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        name_entry.focus_set()  # Focus sur le premier champ
        
        # Type
        ttk.Label(main_frame, text="Type:").grid(row=1, column=0, sticky='w', pady=5)
        type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, width=27)
        type_combo['values'] = ['Arme', 'Armure', 'Bouclier', 'Accessoire', 'Consommable', 'Autre']
        type_combo.grid(row=1, column=1, pady=5)
        
        # Propriétaire
        ttk.Label(main_frame, text="Propriétaire:").grid(row=2, column=0, sticky='w', pady=5)
        owner_combo = ttk.Combobox(main_frame, textvariable=self.owner_var, width=27)
        owner_combo['values'] = self.players_list
        owner_combo.grid(row=2, column=1, pady=5)
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=3, column=0, sticky='nw', pady=5)
        desc_text = tk.Text(main_frame, width=30, height=6)
        desc_text.insert('1.0', self.desc_var.get())
        desc_text.grid(row=3, column=1, pady=5)
        self.desc_text = desc_text
        
        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ok_btn = ttk.Button(btn_frame, text="OK", command=self.ok_clicked)
        ok_btn.pack(side='left', padx=5)
        cancel_btn = ttk.Button(btn_frame, text="Annuler", command=self.cancel_clicked)
        cancel_btn.pack(side='left', padx=5)
        
        # Raccourcis clavier
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())

    def ok_clicked(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide.")
            return
        
        self.result = {
            'name': self.name_var.get().strip(),
            'type': self.type_var.get(),
            'owner': self.owner_var.get(),
            'description': self.desc_text.get('1.0', 'end-1c')
        }
        self.dialog.destroy()

    def cancel_clicked(self):
        self.dialog.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = JDRTool(root)
    root.mainloop()