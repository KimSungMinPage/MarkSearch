from tkinter import messagebox
def show_error(message: str) -> None: messagebox.showerror("오류", message)
def show_info(message: str) -> None: messagebox.showinfo("안내", message)
