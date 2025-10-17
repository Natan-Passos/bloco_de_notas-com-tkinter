import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Button, Toplevel, colorchooser, font
import json
import os

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Editor de Texto")
        self.master.geometry("700x500")
        self.master.resizable(True, True)

        # Definir o arquivo de configurações
        self.config_file = "config.json"

        # Carregar configurações
        self.load_config()

        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = Menu(self.master)

        # Menu Arquivo
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Novo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Salvar", command=self.save_file)
        file_menu.add_command(label="Salvar como...", command=self.save_as_file)
        file_menu.add_command(label="Fechar", command=self.close_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.master.quit)

        # Menu opcao
        option_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opcao", menu=option_menu)
        option_menu.add_command(label="Fonte do Texto", command=self.change_font)
        option_menu.add_command(label="Cor de Texto", command=self.change_text_color)
        option_menu.add_command(label="Cor de Fundo", command=self.change_bg_color)

        # Menu AJUDA
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Ajuda", command=self.help)
        help_menu.add_command(label="Sobre", command=self.about)

        self.master.config(menu=menubar)

    def create_widgets(self):
        # Criar área de texto para o usuário escrever
        self.text_area = tk.Text(self, wrap='word', font=(self.font_family, self.font_size), bd=1, relief='solid', fg=self.text_color, bg=self.bg_color)
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)


    def save_file(self):
        """Salva o conteúdo da área de texto em um arquivo de texto."""
        try:
            if not hasattr(self, 'current_file') or not self.current_file:
                self.save_as_file()
            else:
                with open(self.current_file, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))  # Salva o conteúdo do Text widget
                messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")

    def save_as_file(self):
        """Abre um diálogo para salvar o conteúdo em um novo arquivo."""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))  # Salva o conteúdo do Text widget
                self.current_file = file_path  # Armazena o caminho do arquivo atual
                messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")

    def open_file(self):
        """Abre um arquivo de texto e carrega seu conteúdo na área de texto."""
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)  # Limpa a área de texto antes de carregar o novo conteúdo
                    self.text_area.insert(tk.END, content)  # Insere o conteúdo do arquivo na área de texto
                self.current_file = file_path  # Armazena o caminho do arquivo atual
                messagebox.showinfo("Sucesso", "Arquivo aberto com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {str(e)}")

    def new_file(self):
        """Cria um novo arquivo em branco."""
        if self.text_area.get(1.0, tk.END).strip():
            # Pergunta se deseja salvar antes de criar um novo arquivo
            response = messagebox.askyesnocancel("Novo Arquivo", "Deseja salvar o arquivo atual?")
            if response:
                self.save_file()
            elif response is None:
                return
        self.text_area.delete(1.0, tk.END)  # Limpa a área de texto para novo arquivo
        self.current_file = None  # Reseta o arquivo atual

    def close_file(self):
        """Fecha o editor de texto."""
        self.master.quit()

    def help(self):
        messagebox.showinfo("Ajuda", "É um bloco de notas, faça história")

    def about(self):
        messagebox.showinfo("Informação", "Programa feito por Natan Passos")

    def load_config(self):
        """Carrega as configurações de arquivo (fonte, cor, fundo)"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as config_file:
                    config = json.load(config_file)
                    self.font_family = config.get('font_family', 'Arial')
                    self.font_size = config.get('font_size', 12)
                    self.text_color = config.get('text_color', 'black')
                    self.bg_color = config.get('bg_color', 'white')
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")
                self.font_family, self.font_size, self.text_color, self.bg_color = 'Arial', 12, 'black', 'white'
        else:
            self.font_family, self.font_size, self.text_color, self.bg_color = 'Arial', 12, 'black', 'white'

    def save_config(self):
        """Salva as configurações em um arquivo JSON."""
        config = {
            'font_family': self.font_family,
            'font_size': self.font_size,
            'text_color': self.text_color,
            'bg_color': self.bg_color
        }
        try:
            with open(self.config_file, 'w') as config_file:
                json.dump(config, config_file)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def change_font(self):
        """Altera a fonte do texto."""
        # Obtém a lista de fontes disponíveis no sistema
        available_fonts = font.families()

        # Cria uma janela com a lista de fontes para o usuário escolher
        font_win = Toplevel(self.master)
        font_win.title("Escolher Fonte")

        font_listbox = tk.Listbox(font_win, height=15, width=30)
        for f in available_fonts:
            font_listbox.insert(tk.END, f)

        # Adiciona uma label para mostrar a visualização da fonte selecionada
        preview_label = tk.Label(font_win, text="Visualização", font=(self.font_family, self.font_size))
        preview_label.pack(pady=10)

        # Função para atualizar a visualização da fonte
        def update_preview(event):
            selected_font = font_listbox.get(tk.ACTIVE)
            preview_label.config(font=(selected_font, 12))  # Aplica a fonte no preview

        font_listbox.bind('<<ListboxSelect>>', update_preview)
        font_listbox.pack(padx=10, pady=10)

        # Função para aplicar a fonte escolhida
        def apply_font():
            selected_font = font_listbox.get(tk.ACTIVE)
            if selected_font:
                self.font_family = selected_font
                self.text_area.config(font=(self.font_family, self.font_size))
                self.save_config()  # Salva as novas configurações
            font_win.destroy()

        # Botão para aplicar a fonte
        apply_button = tk.Button(font_win, text="Aplicar", command=apply_font)
        apply_button.pack(pady=10)

    def change_text_color(self):
        #Alterar a cor do texto.
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color
            self.text_area.config(fg=self.text_color)
            self.save_config()

    def change_bg_color(self):
        #Altera a cor de fundo da área de texto.
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.text_area.config(bg=self.bg_color)
            self.save_config()

root = tk.Tk()
app = App(root)
app.pack(expand=True, fill='both')
root.mainloop()