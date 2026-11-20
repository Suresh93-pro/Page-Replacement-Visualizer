import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from algorithms import ALGORITHMS, simulate
import csv

BG = "#0b1020"
PANEL = "#151d33"
PANEL2 = "#1d2945"
TEXT = "#e8efff"
MUTED = "#9aa9c7"
CYAN = "#39d9ff"
GREEN = "#35d07f"
RED = "#ff647c"
YELLOW = "#ffd166"

class PageReplacementApp:
    def __init__(self, root):
        self.root = root
        root.title("Page Replacement Algorithm Visualizer")
        root.geometry("1180x780")
        root.minsize(950, 650)
        root.configure(bg=BG)
        self.result = None
        self.index = 0
        self._style()
        self._build()

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox", fieldbackground=PANEL2, background=PANEL2, foreground=TEXT)
        s.configure("Treeview", background=PANEL, foreground=TEXT, fieldbackground=PANEL,
                    rowheight=34, borderwidth=0)
        s.configure("Treeview.Heading", background=PANEL2, foreground=CYAN, font=("Segoe UI", 10, "bold"))
        s.map("Treeview", background=[("selected", "#24506b")])

    def _label(self, parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(parent, text=text, bg=parent["bg"], fg=color,
                        font=("Segoe UI", size, "bold" if bold else "normal"))

    def _button(self, parent, text, command, color=CYAN, fg=BG):
        return tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                         activebackground=color, activeforeground=fg, relief="flat",
                         bd=0, padx=16, pady=10, cursor="hand2",
                         font=("Segoe UI", 10, "bold"))

    def _build(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(18, 8))
        tk.Label(header, text="PAGE REPLACEMENT", bg=BG, fg=CYAN,
                 font=("Segoe UI", 23, "bold")).pack(anchor="w")
        tk.Label(header, text="Interactive Operating Systems lab • step-by-step simulation",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))

        controls = tk.Frame(self.root, bg=PANEL, padx=16, pady=14)
        controls.pack(fill="x", padx=24, pady=10)
        self._label(controls, "REFERENCE STRING", 9, CYAN, True).grid(row=0, column=0, sticky="w")
        self.pages_var = tk.StringVar(value="7 0 1 2 0 3 0 4 2 3 0 3 2")
        self.pages_entry = tk.Entry(controls, textvariable=self.pages_var, bg=PANEL2, fg=TEXT,
                                    insertbackground=TEXT, relief="flat", font=("Consolas", 12), width=48)
        self.pages_entry.grid(row=1, column=0, padx=(0, 16), pady=(7, 0), ipady=9, sticky="w")
        self._label(controls, "FRAME COUNT", 9, CYAN, True).grid(row=0, column=1, sticky="w")
        self.capacity_var = tk.StringVar(value="3")
        tk.Entry(controls, textvariable=self.capacity_var, bg=PANEL2, fg=TEXT,
                 insertbackground=TEXT, relief="flat", font=("Segoe UI", 12), width=8)\
            .grid(row=1, column=1, padx=(0, 16), pady=(7, 0), ipady=8)
        self._label(controls, "ALGORITHM", 9, CYAN, True).grid(row=0, column=2, sticky="w")
        self.algorithm_var = tk.StringVar(value="FIFO")
        ttk.Combobox(controls, textvariable=self.algorithm_var, values=ALGORITHMS,
                     state="readonly", width=18).grid(row=1, column=2, padx=(0, 16), pady=(7, 0), ipady=5)
        self._button(controls, "▶  RUN SIMULATION", self.run).grid(row=1, column=3, padx=4)
        self._button(controls, "COMPARE ALL", self.compare, color=YELLOW).grid(row=1, column=4, padx=4)

        actions = tk.Frame(self.root, bg=BG)
        actions.pack(fill="x", padx=24, pady=(2, 10))
        self._button(actions, "⏮ First", lambda: self.show_step(0), color=PANEL2, fg=TEXT).pack(side="left", padx=(0, 7))
        self._button(actions, "◀ Previous", self.previous, color=PANEL2, fg=TEXT).pack(side="left", padx=7)
        self._button(actions, "Next ▶", self.next, color=PANEL2, fg=TEXT).pack(side="left", padx=7)
        self._button(actions, "Last ⏭", self.last, color=PANEL2, fg=TEXT).pack(side="left", padx=7)
        self._button(actions, "Export CSV", self.export, color=GREEN).pack(side="right")

        self.stats = tk.Frame(self.root, bg=BG)
        self.stats.pack(fill="x", padx=24, pady=4)
        self.stat_labels = {}
        for key, title, color in [("faults","PAGE FAULTS",RED),("hits","PAGE HITS",GREEN),
                                  ("fault_rate","FAULT RATE",YELLOW),("hit_rate","HIT RATE",CYAN)]:
            card = tk.Frame(self.stats, bg=PANEL, padx=15, pady=10)
            card.pack(side="left", fill="x", expand=True, padx=(0, 9))
            tk.Label(card, text=title, bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            v = tk.Label(card, text="—", bg=PANEL, fg=color, font=("Segoe UI", 19, "bold"))
            v.pack(anchor="w", pady=(4, 0))
            self.stat_labels[key] = v

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=10)
        left = tk.Frame(body, bg=PANEL, padx=14, pady=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(left, text="FRAME MEMORY", bg=PANEL, fg=CYAN,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.step_label = tk.Label(left, text="Run a simulation to begin", bg=PANEL, fg=MUTED,
                                   font=("Segoe UI", 10))
        self.step_label.pack(anchor="w", pady=(4, 10))
        self.frame_area = tk.Frame(left, bg=PANEL)
        self.frame_area.pack(fill="x", pady=6)
        self.status_label = tk.Label(left, text="● READY", bg=PANEL, fg=GREEN,
                                      font=("Segoe UI", 12, "bold"))
        self.status_label.pack(anchor="w", pady=12)
        self.detail_label = tk.Label(left, text="Enter a reference string and select an algorithm.",
                                     bg=PANEL, fg=MUTED, font=("Segoe UI", 10), wraplength=500, justify="left")
        self.detail_label.pack(anchor="w")

        right = tk.Frame(body, bg=PANEL, padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="SIMULATION TRACE", bg=PANEL, fg=CYAN,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        cols = ("step","page","frames","result","evicted")
        self.table = ttk.Treeview(right, columns=cols, show="headings")
        for c, title, width in [("step","STEP",55),("page","PAGE",55),("frames","FRAME CONTENTS",180),
                                ("result","STATUS",90),("evicted","REPLACED",90)]:
            self.table.heading(c, text=title)
            self.table.column(c, width=width, anchor="center")
        self.table.tag_configure("hit", foreground=GREEN)
        self.table.tag_configure("fault", foreground=RED)
        self.table.pack(fill="both", expand=True)
        tk.Label(self.root, text="Algorithms: FIFO • LRU • Optimal • LFU • MFU • Second Chance • Clock • MRU • Random",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(pady=(0, 12))

    def _parse(self):
        try:
            pages = [int(x) for x in self.pages_var.get().replace(",", " ").split()]
            cap = int(self.capacity_var.get())
            if not pages: raise ValueError
            if cap < 1: raise ValueError
            return pages, cap
        except Exception:
            messagebox.showerror("Invalid input", "Enter page numbers separated by spaces/commas and a frame count of 1 or more.")
            return None, None

    def run(self):
        pages, cap = self._parse()
        if pages is None: return
        try:
            self.result = simulate(pages, cap, self.algorithm_var.get())
        except Exception as e:
            messagebox.showerror("Simulation error", str(e)); return
        self.index = 0
        self.table.delete(*self.table.get_children())
        for row in self.result["history"]:
            status = "HIT" if row["hit"] else "FAULT"
            evicted = "—" if row["evicted"] is None else str(row["evicted"])
            self.table.insert("", "end", values=(row["step"], row["page"],
                "  ".join(map(str, row["frames"])), status, evicted),
                tags=("hit" if row["hit"] else "fault",))
        self.stat_labels["faults"].config(text=str(self.result["faults"]))
        self.stat_labels["hits"].config(text=str(self.result["hits"]))
        self.stat_labels["fault_rate"].config(text=f'{self.result["fault_rate"]:.1f}%')
        self.stat_labels["hit_rate"].config(text=f'{self.result["hit_rate"]:.1f}%')
        self.show_step(0)

    def show_step(self, index):
        if not self.result: return
        index = max(0, min(index, len(self.result["history"])-1))
        self.index = index
        row = self.result["history"][index]
        self.step_label.config(text=f'Step {row["step"]} of {self.result["total"]}   •   Requested page: {row["page"]}')
        for w in self.frame_area.winfo_children(): w.destroy()
        capacity = int(self.capacity_var.get())
        for slot in range(capacity):
            page = row["frames"][slot] if slot < len(row["frames"]) else "EMPTY"
            bg = GREEN if page == row["page"] and row["hit"] else (RED if page == row["page"] else PANEL2)
            cell = tk.Frame(self.frame_area, bg=bg, padx=12, pady=12, highlightthickness=1, highlightbackground="#34425f")
            cell.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(cell, text=f"FRAME {slot+1}", bg=bg, fg=BG if bg != PANEL2 else MUTED,
                     font=("Segoe UI", 8, "bold")).pack()
            tk.Label(cell, text=str(page), bg=bg, fg=BG if bg != PANEL2 else TEXT,
                     font=("Segoe UI", 18, "bold")).pack(pady=(4,0))
        if row["hit"]:
            self.status_label.config(text="✓ PAGE HIT", fg=GREEN)
            self.detail_label.config(text=f'Page {row["page"]} is already in memory. No replacement is required.')
        else:
            self.status_label.config(text="✕ PAGE FAULT", fg=RED)
            msg = f'Page {row["page"]} was not in memory. '
            msg += "A free frame was used." if row["evicted"] is None else f'Page {row["evicted"]} was replaced.'
            self.detail_label.config(text=msg)
        children = self.table.get_children()
        if children: self.table.selection_set(children[index]); self.table.see(children[index])

    def previous(self): self.show_step(self.index-1)
    def next(self): self.show_step(self.index+1)
    def last(self):
        if self.result: self.show_step(len(self.result["history"])-1)

    def compare(self):
        pages, cap = self._parse()
        if pages is None: return
        rows = []
        for alg in ALGORITHMS:
            r = simulate(pages, cap, alg)
            rows.append((alg, r["faults"], r["hits"], f'{r["fault_rate"]:.1f}%', f'{r["hit_rate"]:.1f}%'))
        win = tk.Toplevel(self.root); win.title("Compare all algorithms"); win.geometry("650x450"); win.configure(bg=BG)
        tk.Label(win, text="ALGORITHM COMPARISON", bg=BG, fg=CYAN,
                 font=("Segoe UI", 16, "bold")).pack(pady=14)
        tree = ttk.Treeview(win, columns=("a","f","h","fr","hr"), show="headings")
        for c,t,w in [("a","ALGORITHM",170),("f","FAULTS",90),("h","HITS",90),("fr","FAULT RATE",110),("hr","HIT RATE",110)]:
            tree.heading(c,text=t); tree.column(c,width=w,anchor="center")
        for row in rows: tree.insert("","end",values=row)
        tree.pack(fill="both",expand=True,padx=18,pady=10)
        best = min(rows, key=lambda x:x[1])
        tk.Label(win, text=f"Lowest faults for this input: {best[0]} ({best[1]} faults)",
                 bg=BG, fg=GREEN, font=("Segoe UI", 11, "bold")).pack(pady=10)

    def export(self):
        if not self.result:
            messagebox.showinfo("Export", "Run a simulation first."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path: return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Step","Page","Frames","Status","Evicted"])
            for r in self.result["history"]:
                writer.writerow([r["step"],r["page"]," ".join(map(str,r["frames"])),
                                 "HIT" if r["hit"] else "FAULT",r["evicted"] if r["evicted"] is not None else ""])
            writer.writerow([])
            writer.writerow(["Total",self.result["total"],"Faults",self.result["faults"],"Hits",self.result["hits"]])
        messagebox.showinfo("Export complete", f"Saved to:\\n{path}")
