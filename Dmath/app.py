"""Team & Access Planner — a practical discrete-math desktop tool."""

import math
import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk

NAVY, BLUE, INK, MUTED = "#102a43", "#2563eb", "#172033", "#5b6475"
WHITE, PALE_BLUE, PALE_GREEN = "#ffffff", "#eaf2ff", "#e8f7ef"


class Planner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Team & Access Planner")
        self.geometry("1050x720")
        self.minsize(880, 620)
        self.configure(bg="#f6f8fc")
        self._styles()
        self._header()
        self._tabs()

    def _styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#f6f8fc", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 10), background="#e7edf5", foreground=INK)
        style.map("TNotebook.Tab", background=[("selected", WHITE)], foreground=[("selected", BLUE)])
        style.configure("Card.TFrame", background=WHITE)
        style.configure("Title.TLabel", background=WHITE, foreground=NAVY, font=("Segoe UI", 18, "bold"))
        style.configure("Text.TLabel", background=WHITE, foreground=INK, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=WHITE, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Result.TLabel", background=PALE_BLUE, foreground=NAVY, font=("Segoe UI", 11, "bold"), padding=14)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(13, 8))

    def _header(self):
        box = tk.Frame(self, bg=NAVY, height=94)
        box.pack(fill="x")
        box.pack_propagate(False)
        tk.Label(box, text="Team & Access Planner", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=30, pady=(15, 0))
        tk.Label(box, text="Useful planning tools that show the counting logic behind each decision.",
                 bg=NAVY, fg="#cbd5e1", font=("Segoe UI", 11)).pack(anchor="w", padx=31, pady=(3, 0))

    def _tabs(self):
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True, padx=24, pady=22)
        self._team_tab(tabs)
        self._roles_tab(tabs)
        self._access_tab(tabs)

    def _card(self, parent, row=0, col=0):
        card = ttk.Frame(parent, style="Card.TFrame", padding=22)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        return card

    @staticmethod
    def _names(text):
        return list(dict.fromkeys(name.strip() for name in text.replace("\n", ",").split(",") if name.strip()))

    def _people_input(self, parent, label="People (separate names with commas)"):
        ttk.Label(parent, text=label, style="Text.TLabel").pack(anchor="w")
        field = tk.Text(parent, height=5, font=("Segoe UI", 10), relief="solid", borderwidth=1)
        field.pack(fill="x", pady=(6, 14))
        field.insert("1.0", "Aisha, Ben, Carla, Diego, Emiko, Farah")
        return field

    def _team_tab(self, tabs):
        page = ttk.Frame(tabs)
        tabs.add(page, text="Fair team picker")
        page.columnconfigure((0, 1), weight=1, uniform="columns")
        picker = self._card(page, 0, 0)
        ttk.Label(picker, text="Pick a project team fairly", style="Title.TLabel").pack(anchor="w")
        ttk.Label(picker, text="Use this when everyone has an equal chance to be selected for a committee, peer review, or project group.", style="Muted.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(5, 18))
        self.team_people = self._people_input(picker)
        line = ttk.Frame(picker, style="Card.TFrame")
        line.pack(fill="x")
        ttk.Label(line, text="Team size", style="Text.TLabel").pack(side="left")
        self.team_size = tk.StringVar(value="3")
        ttk.Spinbox(line, from_=1, to=100, textvariable=self.team_size, width=7, justify="center").pack(side="right")
        ttk.Button(picker, text="Pick a team", style="Accent.TButton", command=self.pick_team).pack(anchor="w", pady=(18, 0))
        self.team_result = ttk.Label(picker, text="Your selected team will appear here.", style="Result.TLabel", wraplength=390, justify="left")
        self.team_result.pack(fill="x", pady=(14, 0))
        why = self._card(page, 0, 1)
        ttk.Label(why, text="Why this is a combination", style="Title.TLabel").pack(anchor="w")
        ttk.Label(why, text="A team has no internal ranking: the group {Aisha, Ben, Carla} is the same selection in every order. The app selects from combinations, making every possible group equally likely.", style="Text.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(8, 18))
        self.team_math = ttk.Label(why, text="Enter names and a team size to see the number of possible teams.", style="Result.TLabel", wraplength=390, justify="left")
        self.team_math.pack(fill="x")
        ttk.Label(why, text="Practical use: publish the candidate list and use the result as a transparent record of a random, unbiased selection.", style="Muted.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(20, 0))

    def pick_team(self):
        people = self._names(self.team_people.get("1.0", "end"))
        try:
            size = int(self.team_size.get())
            if not 1 <= size <= len(people): raise ValueError
        except ValueError:
            messagebox.showerror("Check the team", "Enter at least as many people as the requested team size.")
            return
        selected = sorted(secrets.SystemRandom().sample(people, size), key=str.casefold)
        total = math.comb(len(people), size)
        self.team_result.config(text="Selected team: " + ", ".join(selected))
        self.team_math.config(text=f"{len(people)}C{size} = {total:,} possible teams\nEach team had a 1 in {total:,} chance of being chosen.")

    def _roles_tab(self, tabs):
        page = ttk.Frame(tabs)
        tabs.add(page, text="Role assignment")
        page.columnconfigure((0, 1), weight=1, uniform="columns")
        assign = self._card(page, 0, 0)
        ttk.Label(assign, text="Assign distinct responsibilities", style="Title.TLabel").pack(anchor="w")
        ttk.Label(assign, text="Randomly assign named roles after a team forms. This helps distribute meeting roles or event duties without favoritism.", style="Muted.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(5, 18))
        self.role_people = self._people_input(assign, "Eligible people")
        ttk.Label(assign, text="Roles (separate with commas)", style="Text.TLabel").pack(anchor="w")
        self.roles = tk.StringVar(value="Facilitator, Note taker, Timekeeper")
        ttk.Entry(assign, textvariable=self.roles, font=("Segoe UI", 10)).pack(fill="x", pady=(6, 14))
        ttk.Button(assign, text="Assign roles", style="Accent.TButton", command=self.assign_roles).pack(anchor="w")
        self.role_result = ttk.Label(assign, text="Assignments will appear here.", style="Result.TLabel", wraplength=390, justify="left")
        self.role_result.pack(fill="x", pady=(14, 0))
        why = self._card(page, 0, 1)
        ttk.Label(why, text="Why this is a permutation", style="Title.TLabel").pack(anchor="w")
        ttk.Label(why, text="The roles are different. Aisha as facilitator and Ben as timekeeper is different from Ben as facilitator and Aisha as timekeeper. Role position matters.", style="Text.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(8, 18))
        self.role_math = ttk.Label(why, text="Enter eligible people and roles to see the number of possible assignments.", style="Result.TLabel", wraplength=390, justify="left")
        self.role_math.pack(fill="x")
        ttk.Label(why, text="This supports rotating responsibilities in clubs, classes, volunteer groups, and workshops.", style="Muted.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(20, 0))

    def assign_roles(self):
        people = self._names(self.role_people.get("1.0", "end"))
        roles = self._names(self.roles.get())
        if not roles or len(roles) > len(people):
            messagebox.showerror("Check roles", "Add at least one role, with no more roles than eligible people.")
            return
        chosen = secrets.SystemRandom().sample(people, len(roles))
        self.role_result.config(text="\n".join(f"{role}: {person}" for role, person in zip(roles, chosen)))
        total = math.perm(len(people), len(roles))
        self.role_math.config(text=f"{len(people)}P{len(roles)} = {total:,} possible assignments\nEvery valid role assignment had the same chance.")

    def _access_tab(self, tabs):
        page = ttk.Frame(tabs)
        tabs.add(page, text="Access code planner")
        page.columnconfigure((0, 1), weight=1, uniform="columns")
        plan = self._card(page, 0, 0)
        ttk.Label(plan, text="Plan an access code", style="Title.TLabel").pack(anchor="w")
        ttk.Label(plan, text="Compare code designs before setting a PIN for a shared lock, Wi-Fi guest account, or private device.", style="Muted.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(5, 18))
        self.code_type = tk.StringVar(value="Digits (0–9)")
        ttk.Label(plan, text="Allowed characters", style="Text.TLabel").pack(anchor="w")
        ttk.Combobox(plan, values=["Digits (0–9)", "Letters and digits", "Letters, digits, and symbols"], textvariable=self.code_type, state="readonly").pack(fill="x", pady=(6, 14))
        row = ttk.Frame(plan, style="Card.TFrame")
        row.pack(fill="x")
        ttk.Label(row, text="Code length", style="Text.TLabel").pack(side="left")
        self.code_length = tk.StringVar(value="6")
        ttk.Spinbox(row, from_=4, to=32, textvariable=self.code_length, width=7, justify="center").pack(side="right")
        ttk.Button(plan, text="Calculate and generate", style="Accent.TButton", command=self.plan_code).pack(anchor="w", pady=(18, 0))
        self.code_result = ttk.Label(plan, text="Choose a format and length to generate an example code.", style="Result.TLabel", wraplength=390, justify="left")
        self.code_result.pack(fill="x", pady=(14, 0))
        lesson = self._card(page, 0, 1)
        ttk.Label(lesson, text="The multiplication principle", style="Title.TLabel").pack(anchor="w")
        ttk.Label(lesson, text="If each position can use n characters and the code has r positions, there are nʳ possible codes. Every added position multiplies the number of guesses an attacker needs.", style="Text.TLabel", wraplength=390, justify="left").pack(anchor="w", pady=(8, 18))
        self.code_math = ttk.Label(lesson, text="Example: a six digit code has 10⁶ = 1,000,000 possible values.", style="Result.TLabel", wraplength=390, justify="left")
        self.code_math.pack(fill="x")
        note = tk.Frame(lesson, bg=PALE_GREEN, padx=13, pady=11)
        note.pack(fill="x", pady=(20, 0))
        tk.Label(note, text="Use a password manager for account passwords. This tool is most appropriate for short codes you must enter yourself.", bg=PALE_GREEN, fg="#166534", font=("Segoe UI", 10), wraplength=355, justify="left").pack(anchor="w")

    def plan_code(self):
        sets = {"Digits (0–9)": string.digits, "Letters and digits": string.ascii_letters + string.digits, "Letters, digits, and symbols": string.ascii_letters + string.digits + "!@#$%&*?"}
        try:
            length = int(self.code_length.get())
            if not 4 <= length <= 32: raise ValueError
        except ValueError:
            messagebox.showerror("Check length", "Choose a code length from 4 to 32.")
            return
        chars = sets[self.code_type.get()]
        possible = len(chars) ** length
        example = "".join(secrets.choice(chars) for _ in range(length))
        self.code_result.config(text=f"Generated example: {example}\nPossible codes: {possible:,}")
        self.code_math.config(text=f"{len(chars)}^{length} = {possible:,} possible codes\nA single random guess succeeds with probability {100 / possible:.5g}%.")


if __name__ == "__main__":
    Planner().mainloop()
