import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ---------------- Custom MinHeap Class ----------------
class MinHeap:
    def __init__(self):
        self.heap = []

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i): return 2 * i + 1
    def _right(self, i): return 2 * i + 2

    def insert(self, priority, task, due_date_str):
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date Format", "Please use YYYY-MM-DD format for due date.")
            return
        self.heap.append((priority, due_date, task))
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        while i > 0 and self._compare(self.heap[i], self.heap[self._parent(i)]):
            self.heap[i], self.heap[self._parent(i)] = self.heap[self._parent(i)], self.heap[i]
            i = self._parent(i)

    def _heapify_down(self, i):
        smallest = i
        left = self._left(i)
        right = self._right(i)

        if left < len(self.heap) and self._compare(self.heap[left], self.heap[smallest]):
            smallest = left
        if right < len(self.heap) and self._compare(self.heap[right], self.heap[smallest]):
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)

    def _compare(self, a, b):
        # Compare priority first, then due date
        if a[0] != b[0]:
            return a[0] < b[0]
        return a[1] < b[1]  # earlier date comes first

    def extract_min(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)
        return root

    def view(self):
        return sorted(self.heap, key=lambda x: (x[0], x[1]))

    def peek(self):
        return self.heap[0] if self.heap else None

# ---------------- GUI Code ----------------
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List: Priority + Due Date Sorting")
        self.todo_heap = MinHeap()

        # Input Fields
        tk.Label(root, text="Task:").grid(row=0, column=0)
        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Priority (1 = High):").grid(row=1, column=0)
        self.priority_entry = tk.Entry(root)
        self.priority_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.due_date_entry = tk.Entry(root)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Remove Highest Priority Task", command=self.remove_task).grid(row=4, column=0, columnspan=2, pady=5)

        # Task List Display
        self.task_listbox = tk.Listbox(root, width=60)
        self.task_listbox.grid(row=5, column=0, columnspan=2, pady=10)

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()
        try:
            priority = int(self.priority_entry.get())
            if not task:
                messagebox.showwarning("Input Error", "Task description cannot be empty.")
                return
            self.todo_heap.insert(priority, task, due_date)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Priority must be a number.")

    def remove_task(self):
        removed = self.todo_heap.extract_min()
        if removed:
            messagebox.showinfo("Task Completed", f"Removed: {removed[2]} (Priority {removed[0]}, Due: {removed[1].strftime('%Y-%m-%d')})")
            self.update_task_list()
        else:
            messagebox.showinfo("No Tasks", "There are no tasks to remove.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for p, d, t in self.todo_heap.view():
            self.task_listbox.insert(tk.END, f"Priority {p} → {t} (Due: {d.strftime('%Y-%m-%d')})")

# ---------------- Run the App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
