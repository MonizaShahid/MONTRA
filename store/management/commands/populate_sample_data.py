from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import Profile, Vendor, Customer
from store.models import Category, Item, Delivery
from transactions.models import Sale, SaleDetail, Purchase


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))

        # Create or get users (profile will be auto-created by signal)
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@montra.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        staff_user, created = User.objects.get_or_create(
            username='staff',
            defaults={
                'email': 'staff@montra.com',
                'first_name': 'Staff',
                'last_name': 'Member'
            }
        )
        staff_user.set_password('staff123')
        staff_user.save()

        # Update profiles if they exist
        try:
            admin_profile = admin_user.profile
            admin_profile.email = admin_user.email
            admin_profile.first_name = admin_user.first_name
            admin_profile.last_name = admin_user.last_name
            admin_profile.role = 'AD'
            admin_profile.status = 'A'
            admin_profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(
                user=admin_user,
                email=admin_user.email,
                first_name=admin_user.first_name,
                last_name=admin_user.last_name,
                role='AD',
                status='A'
            )

        try:
            staff_profile = staff_user.profile
            staff_profile.email = staff_user.email
            staff_profile.first_name = staff_user.first_name
            staff_profile.last_name = staff_user.last_name
            staff_profile.role = 'OP'
            staff_profile.status = 'A'
            staff_profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(
                user=staff_user,
                email=staff_user.email,
                first_name=staff_user.first_name,
                last_name=staff_user.last_name,
                role='OP',
                status='A'
            )

        # Create vendors
        vendors_data = [
            {'name': 'Tech Supplies Co.', 'phone_number': 1234567890, 'address': '123 Tech St'},
            {'name': 'Office Depot Pro', 'phone_number': 2345678901, 'address': '456 Business Ave'},
            {'name': 'General Goods Ltd.', 'phone_number': 3456789012, 'address': '789 Commerce Rd'},
            {'name': 'Electronics Inc.', 'phone_number': 4567890123, 'address': '321 Digital Way'},
            {'name': 'Food & More', 'phone_number': 5678901234, 'address': '654 Market St'},
        ]

        vendors = []
        for vendor_data in vendors_data:
            vendor, _ = Vendor.objects.get_or_create(**vendor_data)
            vendors.append(vendor)

        # Create customers
        customers_data = [
            {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'phone': '555-0101', 'loyalty_points': 150},
            {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com', 'phone': '555-0102', 'loyalty_points': 85},
            {'first_name': 'Bob', 'last_name': 'Johnson', 'email': 'bob@example.com', 'phone': '555-0103', 'loyalty_points': 200},
            {'first_name': 'Alice', 'last_name': 'Williams', 'email': 'alice@example.com', 'phone': '555-0104', 'loyalty_points': 50},
            {'first_name': 'Charlie', 'last_name': 'Brown', 'email': 'charlie@example.com', 'phone': '555-0105', 'loyalty_points': 120},
        ]

        customers = []
        for customer_data in customers_data:
            customer, _ = Customer.objects.get_or_create(
                first_name=customer_data['first_name'],
                last_name=customer_data['last_name'],
                defaults=customer_data
            )
            customers.append(customer)

        # Create categories
        categories_data = [
            'Electronics',
            'Office Supplies',
            'Food & Beverages',
            'Clothing',
            'Books',
            'Home & Garden',
            'Sports & Outdoors',
            'Health & Beauty',
        ]

        categories = []
        for category_name in categories_data:
            category, _ = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        # Create items
        items_data = [
            # Electronics
            {'name': 'Laptop', 'category': 'Electronics', 'price': 999.99, 'quantity': 15, 'description': 'High-performance laptop'},
            {'name': 'Wireless Mouse', 'category': 'Electronics', 'price': 29.99, 'quantity': 50, 'description': 'Ergonomic wireless mouse'},
            {'name': 'Keyboard', 'category': 'Electronics', 'price': 79.99, 'quantity': 30, 'description': 'Mechanical keyboard'},
            {'name': 'Monitor', 'category': 'Electronics', 'price': 299.99, 'quantity': 20, 'description': '27-inch 4K monitor'},
            
            # Office Supplies
            {'name': 'Printer Paper', 'category': 'Office Supplies', 'price': 12.99, 'quantity': 100, 'description': 'A4 printer paper'},
            {'name': 'Stapler', 'category': 'Office Supplies', 'price': 15.99, 'quantity': 75, 'description': 'Heavy-duty stapler'},
            {'name': 'Pen Set', 'category': 'Office Supplies', 'price': 8.99, 'quantity': 200, 'description': 'Premium pen set'},
            {'name': 'Notebook', 'category': 'Office Supplies', 'price': 5.99, 'quantity': 150, 'description': 'Spiral-bound notebook'},
            
            # Food & Beverages
            {'name': 'Coffee Beans', 'category': 'Food & Beverages', 'price': 14.99, 'quantity': 40, 'description': 'Premium coffee beans'},
            {'name': 'Bottled Water', 'category': 'Food & Beverages', 'price': 2.99, 'quantity': 300, 'description': 'Spring water'},
            {'name': 'Snacks Pack', 'category': 'Food & Beverages', 'price': 6.99, 'quantity': 80, 'description': 'Assorted snacks'},
            
            # Clothing
            {'name': 'T-Shirt', 'category': 'Clothing', 'price': 19.99, 'quantity': 120, 'description': 'Cotton t-shirt'},
            {'name': 'Jeans', 'category': 'Clothing', 'price': 49.99, 'quantity': 60, 'description': 'Classic denim jeans'},
            
            # Books
            {'name': 'Programming Book', 'category': 'Books', 'price': 39.99, 'quantity': 25, 'description': 'Learn Python programming'},
            {'name': 'Business Guide', 'category': 'Books', 'price': 24.99, 'quantity': 35, 'description': 'Business management guide'},
            
            # Home & Garden
            {'name': 'Garden Tool Set', 'category': 'Home & Garden', 'price': 45.99, 'quantity': 20, 'description': 'Complete garden tool set'},
            
            # Sports & Outdoors
            {'name': 'Yoga Mat', 'category': 'Sports & Outdoors', 'price': 29.99, 'quantity': 45, 'description': 'Non-slip yoga mat'},
            
            # Health & Beauty
            {'name': 'Skincare Set', 'category': 'Health & Beauty', 'price': 34.99, 'quantity': 30, 'description': 'Complete skincare routine'},
        ]

        items = []
        for item_data in items_data:
            category = next(cat for cat in categories if cat.name == item_data['category'])
            vendor = random.choice(vendors)
            
            item, _ = Item.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'category': category,
                    'price': item_data['price'],
                    'quantity': item_data['quantity'],
                    'description': item_data['description'],
                    'vendor': vendor,
                    'expiring_date': timezone.now() + timedelta(days=random.randint(30, 365))
                }
            )
            items.append(item)

        # Create sales
        for _ in range(15):
            customer = random.choice(customers)
            sale = Sale.objects.create(
                customer=customer,
                sub_total=0,
                grand_total=0,
                tax_amount=0,
                tax_percentage=8.0,
                amount_paid=0,
                amount_change=0
            )
            
            # Create sale details
            num_items = random.randint(1, 5)
            selected_items = random.sample(items, min(num_items, len(items)))
            sub_total = 0
            
            for item in selected_items:
                quantity = random.randint(1, 5)
                price = item.price
                total = price * quantity
                
                SaleDetail.objects.create(
                    sale=sale,
                    item=item,
                    price=price,
                    quantity=quantity,
                    total_detail=total
                )
                sub_total += total
            
            tax_amount = sub_total * 0.08
            grand_total = sub_total + tax_amount
            
            sale.sub_total = sub_total
            sale.tax_amount = tax_amount
            sale.grand_total = grand_total
            sale.amount_paid = grand_total
            sale.save()

        # Create purchases
        for _ in range(10):
            item = random.choice(items)
            vendor = random.choice(vendors)
            quantity = random.randint(10, 50)
            price = item.price * 0.7  # Purchase price lower than sale price
            
            Purchase.objects.create(
                item=item,
                vendor=vendor,
                quantity=quantity,
                price=price,
                description=f'Bulk purchase of {item.name}',
                delivery_status='S',
                order_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                delivery_date=timezone.now() - timedelta(days=random.randint(1, 20))
            )

        # Create deliveries
        for _ in range(8):
            item = random.choice(items)
            customer = random.choice(customers)
            
            Delivery.objects.create(
                item=item,
                customer_name=f"{customer.first_name} {customer.last_name}",
                phone_number=customer.phone,
                location=f"Address {random.randint(1, 100)}",
                date=timezone.now() - timedelta(days=random.randint(1, 15)),
                is_delivered=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
        self.stdout.write(self.style.SUCCESS(f'Created:'))
        self.stdout.write(self.style.SUCCESS(f'  - {User.objects.count()} users'))
        self.stdout.write(self.style.SUCCESS(f'  - {Profile.objects.count()} profiles'))
        self.stdout.write(self.style.SUCCESS(f'  - {Vendor.objects.count()} vendors'))
        self.stdout.write(self.style.SUCCESS(f'  - {Customer.objects.count()} customers'))
        self.stdout.write(self.style.SUCCESS(f'  - {Category.objects.count()} categories'))
        self.stdout.write(self.style.SUCCESS(f'  - {Item.objects.count()} items'))
        self.stdout.write(self.style.SUCCESS(f'  - {Sale.objects.count()} sales'))
        self.stdout.write(self.style.SUCCESS(f'  - {Purchase.objects.count()} purchases'))
        self.stdout.write(self.style.SUCCESS(f'  - {Delivery.objects.count()} deliveries'))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write(self.style.SUCCESS('  Admin - username: admin, password: admin123'))
        self.stdout.write(self.style.SUCCESS('  Staff - username: staff, password: staff123'))
