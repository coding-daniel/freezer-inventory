import csv
import os
import requests

CSV_FILE = 'inventory/inventory.csv'

class InventoryManager:
    def __init__(self, filename=CSV_FILE):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.inventory = self.load_inventory()

    def load_inventory(self):
        inventory = {}
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    inventory[row['barcode']] = {
                        'name': row['name'],
                        'weight': row.get('weight', 'Unknown'),
                        'quantity': int(row['quantity'])
                    }
        return inventory

    def save_inventory(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['barcode', 'name', 'weight', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for barcode, item in self.inventory.items():
                writer.writerow({
                    'barcode': barcode,
                    'name': item['name'],
                    'weight': item['weight'],
                    'quantity': item['quantity']
                })

    def fetch_product_info(self, barcode):
        url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
        try:
            response = requests.get(url)
            data = response.json()
            product = data.get('product', {})
            name = product.get('product_name') or "Unknown product"
            weight = product.get('quantity') or "Unknown"
            return name, weight
        except Exception:
            return "Unknown product", "Unknown"

    def add_item(self, barcode, quantity):
        if barcode in self.inventory:
            self.inventory[barcode]['quantity'] += quantity
        else:
            name, weight = self.fetch_product_info(barcode)
            self.inventory[barcode] = {
                'name': name,
                'weight': weight,
                'quantity': quantity
            }
        self.save_inventory()
        return self.inventory[barcode]

    def remove_quantity(self, barcode, quantity):
        if barcode not in self.inventory:
            return None, "Product not found."
        if quantity >= self.inventory[barcode]['quantity']:
            del self.inventory[barcode]
            self.save_inventory()
            return None, "Product removed completely."
        else:
            self.inventory[barcode]['quantity'] -= quantity
            self.save_inventory()
            return self.inventory[barcode], "Quantity updated."

    def remove_product(self, barcode):
        if barcode in self.inventory:
            del self.inventory[barcode]
            self.save_inventory()
            return True
        return False

    def list_inventory(self):
        return self.inventory


def main():
    print("📦 Barcode Inventory Tracker")
    manager = InventoryManager()

    while True:
        print("\n--- MENU ---")
        print("1. Add product")
        print("2. Remove quantity")
        print("3. Remove product")
        print("4. Show inventory")
        print("q. Quit")
        choice = input("Choose an option: ").strip().lower()

        if choice == '1':
            barcode = input("Enter barcode: ").strip()
            quantity = input("Enter quantity to add: ").strip()
            if not quantity.isdigit():
                print("❌ Invalid quantity.")
                continue
            quantity = int(quantity)
            name, weight = manager.fetch_product_info(barcode)

            # If not found, ask the user
            if name == "Unknown product":
                print("⚠️ Product not found in Open Food Facts.")
                name = input("Enter product name manually: ").strip()
                weight = input("Enter product weight (e.g. 500 g): ").strip()

            item = manager.add_item(barcode, quantity)
            # Inject manual name/weight if needed
            item['name'] = name
            item['weight'] = weight
            manager.save_inventory()

            print(f"✅ Added: {quantity} x {item['name']} ({item['weight']})")


        elif choice == '2':
            barcode = input("Enter barcode to remove quantity from: ").strip()
            quantity = input("Enter quantity to remove: ").strip()
            if not quantity.isdigit():
                print("❌ Invalid quantity.")
                continue
            quantity = int(quantity)
            item, message = manager.remove_quantity(barcode, quantity)
            print(f"ℹ️ {message}")

        elif choice == '3':
            barcode = input("Enter barcode to remove entirely: ").strip()
            success = manager.remove_product(barcode)
            print("✅ Product removed." if success else "❌ Product not found.")

        elif choice == '4':
            inventory = manager.list_inventory()
            if not inventory:
                print("📭 Inventory is empty.")
            else:
                for b, i in inventory.items():
                    print(f"{i['name']} ({i['weight']}) — Barcode: {b} — Quantity: {i['quantity']}")

        elif choice == 'q':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Try again.")


if __name__ == '__main__':
    main()
