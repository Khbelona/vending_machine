import tkinter as tk
from tkinter import messagebox

# Define global variables and arrays
coin = 0
revenue = 0
out = '0'
button = [' ', ' ', ' ', ' ', ' ']
name = ["Juice", "Cola", "Ice Tea", "Water", "Coffee"]
price = [15, 20, 10, 5, 25]
availability = [5, 5, 5, 5, 5]

def update_machine_display():
    for i in range(5):
        if availability[i] > 0:
            if coin >= price[i]:
                button[i] = 'O'
            else:
                button[i] = ' '
        if availability[i] == 0:
            button[i] = 'X'
    display_text = "+-----------------------------------------------+\n"
    display_text += "| Vending Machine                               |\n"
    display_text += "+-----------------------------------------------+\n"
    for i in range(5):
        display_text += f"| {name[i]:<6} Rs{price[i]:<3} [{button[i]}] (Stock: {availability[i]})           |\n"
    display_text += "+-----------------------------------------------+\n"
    display_text += f"| Coins Inserted: Rs{coin:<2}                                 |\n"
    display_text += "|                                               |\n"
    display_text += "| Take Your Product From Here                   |\n"
    display_text += f"|   [={out}=]                                       |\n"
    display_text += "+-----------------------------------------------+\n"
    machine_display.config(state=tk.NORMAL)
    machine_display.delete(1.0, tk.END)
    machine_display.insert(tk.END, display_text)
    machine_display.config(state=tk.DISABLED)

def insert_coin(value):
    global coin
    coin += value
    update_machine_display()

def press_product(index):
    global coin, revenue, out
    if coin >= price[index] and availability[index] > 0:
        coin -= price[index]
        availability[index] -= 1
        revenue += price[index]
        out = str(index + 1)
    else:
        messagebox.showwarning("Warning", "CANNOT BUY THE PRODUCT. INSUFFICIENT AMOUNT OF MONEY OR SOLD OUT!!!")
    update_machine_display()

def service_menu():
    service_window = tk.Toplevel(root)
    service_window.title("Service Menu")
    
    def inspect_machine_status():
        status_text = f"Amount of revenue: Rs{revenue}\nAmount of inserted coins: Rs{coin}\nProduct information:\n"
        for i in range(5):
            status = "(SOLD OUT)" if availability[i] == 0 else f"({availability[i]} left)"
            status_text += f" {name[i]} (Rs{price[i]}) {status}\n"
        messagebox.showinfo("Machine Status", status_text)

    def withdraw_all_money():
        global coin, revenue
        total = coin + revenue
        coin = 0
        revenue = 0
        messagebox.showinfo("Withdraw Money", f"All money is being withdrawn.\nRs{total} is withdrawn.")
        update_machine_display()

    def refill_product():
        def refill(index):
            availability[index] = 10
            messagebox.showinfo("Refill Product", f"You have refilled {name[index]} to full.")
            update_machine_display()
            refill_window.destroy()
        
        refill_window = tk.Toplevel(service_window)
        refill_window.title("Refill Product")
        for i in range(5):
            tk.Button(refill_window, text=name[i], command=lambda i=i: refill(i)).pack()

    def change_product():
        def change(index):
            def apply_changes():
                new_name = new_name_entry.get()
                new_price = int(new_price_entry.get())
                name[index] = new_name
                price[index] = new_price
                availability[index] = 10
                messagebox.showinfo("Change Product", f"The new product {name[index]} has been filled to full.")
                update_machine_display()
                change_window.destroy()
            
            change_window = tk.Toplevel(service_window)
            change_window.title("Change Product")
            tk.Label(change_window, text="Enter new product name:").pack()
            new_name_entry = tk.Entry(change_window)
            new_name_entry.pack()
            tk.Label(change_window, text="Enter new product price:").pack()
            new_price_entry = tk.Entry(change_window)
            new_price_entry.pack()
            tk.Button(change_window, text="Apply Changes", command=apply_changes).pack()

        change_window = tk.Toplevel(service_window)
        change_window.title("Change Product")
        for i in range(5):
            tk.Button(change_window, text=name[i], command=lambda i=i: change(i)).pack()

    tk.Button(service_window, text="Inspect Machine Status", command=inspect_machine_status).pack()
    tk.Button(service_window, text="Withdraw All Money", command=withdraw_all_money).pack()
    tk.Button(service_window, text="Refill Product", command=refill_product).pack()
    tk.Button(service_window, text="Change Product", command=change_product).pack()

def main_menu():
    global root, machine_display
    root = tk.Tk()
    root.title("Vending Machine")

    machine_display = tk.Text(root, height=20, width=50)
    machine_display.pack()

    coin_frame = tk.Frame(root)
    coin_frame.pack()

    tk.Button(coin_frame, text="Insert Coin 1", command=lambda: insert_coin(1)).pack(side=tk.LEFT)
    tk.Button(coin_frame, text="Insert Coin 2", command=lambda: insert_coin(2)).pack(side=tk.LEFT)
    tk.Button(coin_frame, text="Insert Coin 5", command=lambda: insert_coin(5)).pack(side=tk.LEFT)
    tk.Button(coin_frame, text="Insert Coin 10", command=lambda: insert_coin(10)).pack(side=tk.LEFT)

    product_frame = tk.Frame(root)
    product_frame.pack()

    for i in range(5):
        tk.Button(product_frame, text=name[i], command=lambda i=i: press_product(i)).pack(side=tk.LEFT)

    tk.Button(root, text="Service Menu", command=service_menu).pack()
    
    update_machine_display()
    root.mainloop()

if __name__ == "__main__":
    main_menu()
