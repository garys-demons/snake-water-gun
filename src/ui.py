import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
from src.constants import ASSETS, FONT
from src.game_logic import get_random_choice, determine_result
from src.utils import load_top_score, save_top_score, append_history

class SnakeWaterGunApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🐍 Snake Water Gun 🔫")
        self.geometry("900x800")
        self.configure(bg='#1a1a2e')
        self.resizable(False, False)
        
        # Game variables
        self.score = tk.IntVar(value=0)
        self.top_score = load_top_score()
        self.game_history = []
        self.animation_running = False
        
        # Colors and styling
        self.colors = {
            'bg': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f4c75',
            'win': '#2ecc71',
            'lose': '#e74c3c',
            'tie': '#f39c12',
            'text': '#ecf0f1',
            'button': '#3498db',
            'button_hover': '#2980b9'
        }
        
        self._setup_fonts()
        self._setup_ui()
        self._setup_styles()

    def _setup_fonts(self):
        """Setup custom fonts for different UI elements"""
        self.title_font = tkFont.Font(family="Arial", size=24, weight="bold")
        self.score_font = tkFont.Font(family="Arial", size=16, weight="bold")
        self.button_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.result_font = tkFont.Font(family="Arial", size=14)

    def _setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('Game.TButton',
                       background=self.colors['button'],
                       foreground='white',
                       borderwidth=2,
                       focuscolor='none',
                       font=self.button_font)
        
        style.map('Game.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('pressed', self.colors['accent'])])

    def _load_image(self, path, size=(180, 180)):
        """Load and resize image with error handling"""
        try:
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Create a placeholder colored rectangle
            placeholder = Image.new('RGB', size, color='#3498db')
            return ImageTk.PhotoImage(placeholder)

    def _setup_ui(self):
        """Setup the main user interface"""
        # Title
        title_frame = tk.Frame(self, bg=self.colors['bg'])
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, 
                              text="🐍 SNAKE WATER GUN 🔫",
                              font=self.title_font,
                              bg=self.colors['bg'],
                              fg=self.colors['text'])
        title_label.pack()
        
        # Score section
        self._create_score_section()
        
        # Game buttons
        self._create_game_buttons()
        
        # Result display
        self._create_result_section()
        
        # Game history
        self._create_history_section()
        
        # Control buttons
        self._create_control_buttons()

    def _create_score_section(self):
        """Create the score display section"""
        score_frame = tk.Frame(self, bg=self.colors['secondary'], relief='raised', bd=2)
        score_frame.pack(pady=15, padx=20, fill='x')
        
        # Current score
        current_score_frame = tk.Frame(score_frame, bg=self.colors['secondary'])
        current_score_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(current_score_frame, 
                text="Current Score:",
                font=self.score_font,
                bg=self.colors['secondary'],
                fg=self.colors['text']).pack()
        
        self.score_display = tk.Label(current_score_frame,
                                     textvariable=self.score,
                                     font=self.title_font,
                                     bg=self.colors['secondary'],
                                     fg=self.colors['win'])
        self.score_display.pack()
        
        # Top score
        top_score_frame = tk.Frame(score_frame, bg=self.colors['secondary'])
        top_score_frame.pack(side='right', padx=20, pady=10)
        
        tk.Label(top_score_frame,
                text="Best Score:",
                font=self.score_font,
                bg=self.colors['secondary'],
                fg=self.colors['text']).pack()
        
        self.top_score_display = tk.Label(top_score_frame,
                                         text=str(self.top_score),
                                         font=self.title_font,
                                         bg=self.colors['secondary'],
                                         fg=self.colors['tie'])
        self.top_score_display.pack()

    def _create_game_buttons(self):
        """Create the main game choice buttons"""
        button_frame = tk.Frame(self, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(button_frame,
                                   text="Choose your weapon:",
                                   font=self.result_font,
                                   bg=self.colors['bg'],
                                   fg=self.colors['text'])
        instruction_label.pack(pady=10)
        
        # Game buttons in a grid
        game_grid = tk.Frame(button_frame, bg=self.colors['bg'])
        game_grid.pack()
        
        self.choice_buttons = {}
        choices = [
            ("snake", "🐍 Snake", 0, 0),
            ("water", "💧 Water", 0, 1),
            ("gun", "🔫 Gun", 0, 2)
        ]
        
        for choice, label, row, col in choices:
            btn_frame = tk.Frame(game_grid, bg=self.colors['accent'], relief='raised', bd=3)
            btn_frame.grid(row=row, column=col, padx=15, pady=10)
            
            # Load image
            img = self._load_image(ASSETS[choice])
            
            # Create button
            btn = tk.Button(btn_frame,
                           image=img,
                           text=label,
                           compound='top',
                           command=lambda c=choice: self._handle_choice(c),
                           bg=self.colors['button'],
                           fg='white',
                           font=self.button_font,
                           relief='flat',
                           bd=0,
                           padx=10,
                           pady=10,
                           cursor='hand2')
            btn.image = img  # Keep reference
            btn.pack(padx=5, pady=5)
            
            self.choice_buttons[choice] = btn
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['button_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['button']))

    def _create_result_section(self):
        """Create the result display section"""
        result_frame = tk.Frame(self, bg=self.colors['secondary'], relief='raised', bd=2)
        result_frame.pack(pady=15, padx=20, fill='x')
        
        tk.Label(result_frame,
                text="Last Game Result:",
                font=self.score_font,
                bg=self.colors['secondary'],
                fg=self.colors['text']).pack(pady=5)
        
        self.result_display = tk.Label(result_frame,
                                      text="Make your first move!",
                                      font=self.result_font,
                                      bg=self.colors['secondary'],
                                      fg=self.colors['text'],
                                      wraplength=400)
        self.result_display.pack(pady=10)

    def _create_history_section(self):
        """Create game history display"""
        history_frame = tk.Frame(self, bg=self.colors['bg'])
        history_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(history_frame,
                text="Game History:",
                font=self.score_font,
                bg=self.colors['bg'],
                fg=self.colors['text']).pack()
        
        # History listbox with scrollbar
        history_container = tk.Frame(history_frame, bg=self.colors['bg'])
        history_container.pack(fill='both', expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(history_container)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(history_container,
                                         yscrollcommand=scrollbar.set,
                                         bg=self.colors['secondary'],
                                         fg=self.colors['text'],
                                         font=('Arial', 10),
                                         height=8)
        self.history_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)

    def _create_control_buttons(self):
        """Create control buttons (reset, help, etc.)"""
        control_frame = tk.Frame(self, bg=self.colors['bg'])
        control_frame.pack(pady=10)
        
        # Reset button
        reset_btn = ttk.Button(control_frame,
                              text="🔄 Reset Score",
                              command=self._reset_score,
                              style='Game.TButton')
        reset_btn.pack(side='left', padx=10)
        
        # Help button
        help_btn = ttk.Button(control_frame,
                             text="❓ Help",
                             command=self._show_help,
                             style='Game.TButton')
        help_btn.pack(side='left', padx=10)
        
        # Clear history button
        clear_btn = ttk.Button(control_frame,
                              text="🗑️ Clear History",
                              command=self._clear_history,
                              style='Game.TButton')
        clear_btn.pack(side='left', padx=10)

    def _handle_choice(self, choice):
        """Handle player's choice and game logic"""
        if self.animation_running:
            return
            
        computer = get_random_choice()
        result = determine_result(choice, computer)
        
        # Add to history
        history_entry = f"{choice.capitalize()} vs {computer.capitalize()}: {result.upper()}"
        self.game_history.append(history_entry)
        self.history_listbox.insert(tk.END, history_entry)
        self.history_listbox.see(tk.END)
        
        # Append to file
        append_history(choice, computer, result)
        
        # Update score
        old_score = self.score.get()
        if result == "win":
            self.score.set(old_score + 1)
            self._animate_button(self.choice_buttons[choice], 'win')
        elif result == "lose":
            self.score.set(old_score - 1)
            self._animate_button(self.choice_buttons[choice], 'lose')
        else:
            self._animate_button(self.choice_buttons[choice], 'tie')
        
        # Update top score
        if self.score.get() > self.top_score:
            self.top_score = self.score.get()
            save_top_score(self.top_score)
            self.top_score_display.config(text=str(self.top_score))
            self._celebrate_new_record()
        
        # Update result display
        result_text = f"You: {choice.capitalize()} | Computer: {computer.capitalize()}\n"
        result_text += f"Result: {result.upper()}"
        
        result_colors = {
            'win': self.colors['win'],
            'lose': self.colors['lose'],
            'tie': self.colors['tie']
        }
        
        self.result_display.config(text=result_text, fg=result_colors[result])

    def _animate_button(self, button, result_type):
        """Animate button based on result"""
        self.animation_running = True
        original_bg = button.cget('background')
        
        colors = {
            'win': self.colors['win'],
            'lose': self.colors['lose'],
            'tie': self.colors['tie']
        }
        
        # Flash animation
        def flash(count=0):
            if count < 6:
                color = colors[result_type] if count % 2 == 0 else original_bg
                button.config(background=color)
                self.after(150, lambda: flash(count + 1))
            else:
                button.config(background=original_bg)
                self.animation_running = False
        
        flash()

    def _celebrate_new_record(self):
        """Celebrate new high score"""
        messagebox.showinfo("🎉 New Record!", 
                          f"Congratulations! New high score: {self.top_score}")

    def _reset_score(self):
        """Reset the current score"""
        if messagebox.askyesno("Reset Score", "Are you sure you want to reset your score?"):
            self.score.set(0)
            self.result_display.config(text="Score reset! Make your next move.", 
                                     fg=self.colors['text'])

    def _clear_history(self):
        """Clear the game history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the game history?"):
            self.history_listbox.delete(0, tk.END)
            self.game_history.clear()

    def _show_help(self):
        """Show help dialog with game rules"""
        help_text = """
🎮 SNAKE WATER GUN RULES:

🐍 Snake drinks 💧 Water (Snake wins)
💧 Water ruins 🔫 Gun (Water wins)  
🔫 Gun kills 🐍 Snake (Gun wins)

🏆 SCORING:
• Win: +1 point
• Lose: -1 point
• Tie: No change

🎯 TIP: Try to beat your high score!
        """
        
        messagebox.showinfo("Game Rules", help_text)