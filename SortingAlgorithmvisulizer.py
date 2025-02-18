import tkinter as tk
import time

class SortingVisualizer:
    def __init__(self, canvas, output_text, delay=500):
        self.canvas = canvas
        self.output_text = output_text
        self.delay = delay
        self.step = 1

    def draw_step(self, arr, label, swaps=None, y_offset=100):
        self.canvas.delete("all")  
        x_start = 50
        gap = 80

        for i, val in enumerate(arr):
            x = x_start + i * gap
            color = "lightblue"
            if swaps and i in swaps:
                color = "lightcoral"
            
            self.canvas.create_rectangle(x, y_offset, x + 50, y_offset + 40, fill=color)
            self.canvas.create_text(x + 25, y_offset + 20, text=str(val), font=("Arial", 14, "bold"))

        self.canvas.create_text(400, y_offset - 30, text=label, font=("Arial", 14, "bold"), fill="black")
        self.canvas.update()
        time.sleep(self.delay / 1000)

        # Display the current state of the array in the Text widget
        self.output_text.insert(tk.END, f"Step {self.step}: {arr}\n")
        self.output_text.see(tk.END)  # Scroll to the bottom
        self.step += 1

    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.draw_step(arr, f"Step {self.step}: Bubble Sort", swaps=[j, j+1])

    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self.draw_step(arr, f"Step {self.step}: Selection Sort", swaps=[i, min_idx])

    def insertion_sort(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
                self.draw_step(arr, f"Step {self.step}: Insertion Sort", swaps=[j+1, j])
            arr[j + 1] = key
            self.draw_step(arr, f"Step {self.step}: Insertion Sort", swaps=[j+1, i])

    def quick_sort(self, arr, low=0, high=None):
        if high is None:
            high = len(arr) - 1

        if low < high:
            pivot_index = self.partition(arr, low, high)
            self.quick_sort(arr, low, pivot_index - 1)
            self.quick_sort(arr, pivot_index + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.draw_step(arr, f"Step {self.step}: Quick Sort", swaps=[i, j])
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.draw_step(arr, f"Step {self.step}: Pivot Placement", swaps=[i+1, high])
        return i + 1

    def merge_sort(self, arr, l=0, r=None):
        if r is None:
            r = len(arr) - 1
        if l < r:
            m = (l + r) // 2
            self.merge_sort(arr, l, m)
            self.merge_sort(arr, m + 1, r)
            self.merge(arr, l, m, r)

    def merge(self, arr, l, m, r):
        left_half = arr[l:m + 1]
        right_half = arr[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            self.draw_step(arr, f"Step {self.step}: Merging", swaps=[k-1])
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            self.draw_step(arr, f"Step {self.step}: Merging", swaps=[k-1])
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            self.draw_step(arr, f"Step {self.step}: Merging", swaps=[k-1])

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x700")

        self.label = tk.Label(root, text="Enter numbers separated by commas:", font=("Arial", 14))
        self.label.pack()

        self.entry = tk.Entry(root, width=50, font=("Arial", 14))
        self.entry.pack()

        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        self.algorithm_menu = tk.OptionMenu(root, self.algorithm_var, "Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort")
        self.algorithm_menu.pack()

        self.sort_button = tk.Button(root, text="Sort", font=("Arial", 14), command=self.sort_numbers)
        self.sort_button.pack()

        self.canvas = tk.Canvas(root, width=850, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Add a Text widget to display the steps
        self.output_text = tk.Text(root, height=10, width=100, font=("Arial", 12))
        self.output_text.pack(pady=10)

    def sort_numbers(self):
        try:
            numbers = [int(num) for num in self.entry.get().split(",")]
            visualizer = SortingVisualizer(self.canvas, self.output_text, delay=1000)
            selected_algorithm = self.algorithm_var.get()

            if selected_algorithm == "Bubble Sort":
                visualizer.bubble_sort(numbers)
            elif selected_algorithm == "Selection Sort":
                visualizer.selection_sort(numbers)
            elif selected_algorithm == "Insertion Sort":
                visualizer.insertion_sort(numbers)
            elif selected_algorithm == "Quick Sort":
                visualizer.quick_sort(numbers)
            elif selected_algorithm == "Merge Sort":
                visualizer.merge_sort(numbers)

            visualizer.draw_step(numbers, "Final Sorted Output", y_offset=300)
        except ValueError:
            tk.messagebox.showerror("Error", "Enter valid numbers separated by commas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()