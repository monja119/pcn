import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from pcn_app.application.use_cases import ComputePcnRequest, ComputePcnUseCase
from pcn_app.domain.errors import DomainValidationError


class PcnCalculatorWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Calculateur PCN - Chaussée souple")
        self.geometry("820x540")
        self.minsize(820, 540)
        self.resizable(False, False)

        self.use_case = ComputePcnUseCase()

        self.h_cbr_var = tk.StringVar()
        self.cbr_var = tk.StringVar()
        self.e_var = tk.StringVar()
        self.rsi_result_var = tk.StringVar(value="-")
        self.pcn_result_var = tk.StringVar(value="-")

        self._configure_style()
        self._build_ui()
        self.bind("<Return>", lambda _event: self._on_compute_clicked())

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.configure(bg="#efefef")

        style.configure("App.TFrame", background="#efefef")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Section.TLabelframe", background="#ffffff", bordercolor="#d6d6d6")
        style.configure(
            "Section.TLabelframe.Label",
            background="#ffffff",
            foreground="#111111",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Title.TLabel",
            background="#ffffff",
            foreground="#111111",
            font=("Segoe UI", 19, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#ffffff",
            foreground="#5c5c5c",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Field.TLabel",
            background="#ffffff",
            foreground="#111111",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Field.TEntry",
            fieldbackground="#ffffff",
            foreground="#111111",
            bordercolor="#c8c8c8",
            insertcolor="#111111",
            lightcolor="#c8c8c8",
            darkcolor="#c8c8c8",
            padding=(10, 9),
        )
        style.map(
            "Field.TEntry",
            bordercolor=[("focus", "#111111")],
            lightcolor=[("focus", "#111111")],
            darkcolor=[("focus", "#111111")],
        )
        style.configure(
            "Compute.TButton",
            background="#111111",
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=0,
            font=("Segoe UI", 11, "bold"),
            padding=(14, 11),
        )
        style.map(
            "Compute.TButton",
            background=[("active", "#2a2a2a"), ("pressed", "#000000")],
        )
        style.configure(
            "ResultName.TLabel",
            background="#ffffff",
            foreground="#555555",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "ResultValue.TLabel",
            background="#ffffff",
            foreground="#111111",
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "ResultFormula.TLabel",
            background="#ffffff",
            foreground="#666666",
            font=("Segoe UI", 9),
        )

    def _build_ui(self) -> None:
        outer = ttk.Frame(self, style="App.TFrame", padding=22)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)

        container = ttk.Frame(outer, style="Card.TFrame", padding=24)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(2, weight=1)

        title_label = ttk.Label(
            container,
            text="Détermination du PCN d'une chaussée souple",
            style="Title.TLabel",
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        subtitle_label = ttk.Label(
            container,
            text="Interface de calcul PCN (méthode RSI) — style professionnel monochrome",
            style="Subtitle.TLabel",
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))

        form_panel = ttk.LabelFrame(container, text="Entrées", style="Section.TLabelframe", padding=16)
        form_panel.grid(row=2, column=0, sticky="nsew", padx=(0, 14))
        form_panel.columnconfigure(0, weight=0)
        form_panel.columnconfigure(1, weight=1)

        self._add_input_row(form_panel, row=0, label="H(CBR)", variable=self.h_cbr_var)
        self._add_input_row(form_panel, row=1, label="CBR", variable=self.cbr_var)
        self._add_input_row(form_panel, row=2, label="Épaisseur e", variable=self.e_var)

        compute_button = ttk.Button(form_panel, text="Calculer le PCN", command=self._on_compute_clicked, style="Compute.TButton")
        compute_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(18, 4))

        results_panel = ttk.LabelFrame(container, text="Résultats", style="Section.TLabelframe", padding=16)
        results_panel.grid(row=2, column=1, sticky="nsew")
        results_panel.columnconfigure(0, weight=1)

        self._create_result_block(results_panel, row=0, label="RSI", value_var=self.rsi_result_var)
        self._create_result_block(results_panel, row=1, label="PCN", value_var=self.pcn_result_var)

    @staticmethod
    def _add_input_row(parent: tk.Widget, row: int, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=f"{label} :", style="Field.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
            pady=10,
            padx=(0, 14),
        )
        ttk.Entry(parent, textvariable=variable, style="Field.TEntry").grid(
            row=row,
            column=1,
            sticky="ew",
            pady=10,
        )

    @staticmethod
    def _create_result_block(parent: tk.Widget, row: int, label: str, value_var: tk.StringVar) -> None:
        card = tk.Frame(
            parent,
            bg="#ffffff",
            padx=12,
            pady=12,
            highlightthickness=1,
            highlightbackground="#dcdcdc",
        )
        card.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text=label, style="ResultName.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(card, textvariable=value_var, style="ResultValue.TLabel").grid(row=1, column=0, sticky="w", pady=(5, 0))

    def _on_compute_clicked(self) -> None:
        try:
            request = ComputePcnRequest(
                h_cbr=self._parse_float(self.h_cbr_var.get(), "H(CBR)"),
                cbr=self._parse_float(self.cbr_var.get(), "CBR"),
                thickness_e=self._parse_float(self.e_var.get(), "Épaisseur e"),
            )

            response = self.use_case.execute(request)
            self.rsi_result_var.set(f"{response.rsi:.4f}")
            self.pcn_result_var.set(f"{response.pcn:.4f}")

        except DomainValidationError as error:
            messagebox.showerror("Validation", str(error))
        except ValueError as error:
            messagebox.showerror("Saisie invalide", str(error))
        except Exception as error:
            messagebox.showerror("Erreur", f"Une erreur inattendue est survenue : {error}")

    @staticmethod
    def _parse_float(raw_value: str, field_name: str) -> float:
        cleaned = raw_value.strip().replace(",", ".")
        if not cleaned:
            raise ValueError(f"Le champ {field_name} est obligatoire.")
        try:
            return float(cleaned)
        except ValueError as error:
            raise ValueError(f"Le champ {field_name} doit être numérique.") from error


def run_app() -> None:
    app = PcnCalculatorWindow()
    app.mainloop()
