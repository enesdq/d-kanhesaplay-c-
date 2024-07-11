import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json

class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dükkan Satış Takip")
        self.root.geometry("1024x768")  # Pencere boyutunu ayarla

        # Stil tanımlamaları
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14))
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TEntry", font=("Helvetica", 14))

        # Ürün ve fiyat bilgilerini yükleme
        self.load_products()

        # Ürünleri seçme durumu
        self.selected_products = {product: 0 for product in self.products}

        # Ürünleri ekranda göstermek için bir Notebook (sekme) oluştur
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.category_frames = {}

        # Ürün ekleme bölümü
        self.add_product_frame = ttk.Frame(root, padding="10")
        self.add_product_frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(self.add_product_frame, text="Kategori:").grid(row=0, column=0, sticky="w")
        self.category_entry = ttk.Entry(self.add_product_frame, width=30)
        self.category_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(self.add_product_frame, text="Ürün Adı:").grid(row=1, column=0, sticky="w")
        self.product_name_entry = ttk.Entry(self.add_product_frame, width=30)
        self.product_name_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(self.add_product_frame, text="Ürün Fiyatı:").grid(row=2, column=0, sticky="w")
        self.product_price_entry = ttk.Entry(self.add_product_frame, width=30)
        self.product_price_entry.grid(row=2, column=1, sticky="w")

        self.add_button = ttk.Button(self.add_product_frame, text="Ürün Ekle", command=self.add_product, width=20)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Ürün kutucuklarını oluştur ve ekranda göster
        self.create_product_buttons()

        # Toplam tutar etiketi
        self.total_label = ttk.Label(root, text="Toplam: 0 TL", font=("Helvetica", 24))
        self.total_label.grid(row=2, column=0, pady=20, sticky="w")

        # Sepeti temizle butonu
        self.clear_button = ttk.Button(root, text="Sepeti Temizle", command=self.clear_selection, width=20)
        self.clear_button.grid(row=3, column=0, pady=10, sticky="w")

        # Kategorileri göstermek ve düzenlemek için widget'lar
        ttk.Label(root, text="Kategorileri Yönet", font=("Helvetica", 16)).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.category_listbox = tk.Listbox(root, height=10, width=30, font=("Helvetica", 12))
        self.category_listbox.grid(row=1, column=1, padx=10, sticky="w")
        self.category_listbox.bind("<Double-Button-1>", self.edit_category)

        ttk.Button(root, text="Kategori Ekle", command=self.add_category, width=15).grid(row=2, column=1, padx=10, pady=5, sticky="w")
        ttk.Button(root, text="Kategori Sil", command=self.delete_category, width=15).grid(row=3, column=1, padx=10, pady=5, sticky="w")

    def load_products(self):
        try:
            with open("products.json", "r") as file:
                self.products = json.load(file)
            # Ürünleri yeni formata dönüştürme
            for product, details in self.products.items():
                if isinstance(details, float):
                    self.products[product] = {'category': 'Diğer', 'price': details}
        except FileNotFoundError:
            self.products = {}

    def save_products(self):
        with open("products.json", "w") as file:
            json.dump(self.products, file)

    def create_product_buttons(self):
        # Önce mevcut sekmeleri temizle
        for frame in self.category_frames.values():
            for widget in frame.winfo_children():
                widget.destroy()

        # Kategorileri ve butonları oluştur
        for product, details in self.products.items():
            category = details['category']
            price = details['price']

            if category not in self.category_frames:
                frame = ttk.Frame(self.notebook, padding="10")
                self.notebook.add(frame, text=category)
                self.category_frames[category] = frame

            frame = self.category_frames[category]
            btn_text = f"{product}\n{price} TL\nSeçim Sayısı: {self.selected_products[product]}"
            btn = tk.Button(frame, text=btn_text, command=lambda p=product: self.increment_product(p), height=3, width=20, font=("Helvetica", 18))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

            # Ürünü sil butonu
            del_btn = ttk.Button(frame, text="Sil", command=lambda p=product: self.delete_product(p))
            del_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def increment_product(self, product):
        self.selected_products[product] += 1
        self.create_product_buttons()
        self.calculate_total()

    def calculate_total(self):
        total = 0
        for product, count in self.selected_products.items():
            total += self.products[product]['price'] * count
        self.total_label.config(text=f"Toplam: {total} TL")

    def clear_selection(self):
        for product in self.selected_products:
            self.selected_products[product] = 0
        self.calculate_total()
        self.create_product_buttons()

    def add_product(self):
        category = self.category_entry.get()
        product_name = self.product_name_entry.get()
        try:
            product_price = float(self.product_price_entry.get())
            if category and product_name and product_price > 0:
                self.products[product_name] = {'category': category, 'price': product_price}
                self.selected_products[product_name] = 0
                self.create_product_buttons()
                self.save_products()
                self.category_entry.delete(0, tk.END)
                self.product_name_entry.delete(0, tk.END)
                self.product_price_entry.delete(0, tk.END)
            else:
                print("Geçerli bir kategori, ürün adı ve fiyatı giriniz.")
        except ValueError:
            print("Geçerli bir fiyat giriniz.")

    def add_category(self):
        category = self.category_entry.get()
        if category:
            self.category_listbox.insert(tk.END, category)
            self.category_entry.delete(0, tk.END)
            self.category_frames[category] = ttk.Frame(self.notebook, padding="10")
            self.notebook.add(self.category_frames[category], text=category)

    def edit_category(self, event):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            selected_category = self.category_listbox.get(selected_index)
            new_category = simpledialog.askstring("Kategori Düzenle", f"Yeni adı giriniz:", parent=self.root)
            if new_category:
                self.category_listbox.delete(selected_index)
                self.category_listbox.insert(selected_index, new_category)
                self.category_frames[new_category] = self.category_frames.pop(selected_category)
                self.notebook.tab(self.category_frames[new_category], text=new_category)
                for product, details in self.products.items():
                    if details['category'] == selected_category:
                        details['category'] = new_category
                self.save_products()

    def delete_category(self):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            selected_category = self.category_listbox.get(selected_index)
            confirmation = messagebox.askyesno("Kategori Sil", f"{selected_category} kategorisini silmek istediğinizden emin misiniz?", parent=self.root)
            if confirmation:
                del self.category_frames[selected_category]
                self.category_listbox.delete(selected_index)
                self.notebook.forget(self.category_frames[selected_category])
                for product, details in list(self.products.items()):
                    if details['category'] == selected_category:
                        del self.products[product]
                self.save_products()

    def delete_product(self, product):
        confirmation = messagebox.askyesno("Ürün Sil", f"{product} ürününü silmek istediğinizden emin misiniz?", parent=self.root)
        if confirmation:
            del self.products[product]
            self.selected_products.pop(product)
            self.create_product_buttons()
            self.calculate_total
