from django.test import TestCase
from decimal import Decimal
from cart.models import Cart, CartItem
from users.models import CustomUser as User

from store.models import Product, Category


"""
class CartModelTest(TestCase):

    def setUp(self):
        # Create a user, category, and product
        self.user = User.objects.create_user(email='man-of-war@gmail.com', username='testuser', password='12345')
        self.category = Category.objects.create(name='TestCategory')
        self.product1 = Product.objects.create(
            owner=self.user,
            name="Product 1",
            price=Decimal('10.00'),
            stock=100,
            size=1,
            category=self.category
        )
        self.product2 = Product.objects.create(
            owner=self.user,
            name="Product 2",
            price=Decimal('20.00'),
            stock=50,
            size=2,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_item_creation(self):
        # Create a CartItem and check if it's properly linked to the cart and product
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)

        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.product, self.product1)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(str(cart_item), "2 x Product 1")

    def test_cart_item_total_price(self):
        # Test total price calculation for CartItem
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=3)

        self.assertEqual(cart_item.total_price, Decimal('30.00'))  # 3 * 10.00

    def test_cart_total_price(self):
        # Test total price calculation for the entire cart
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)  # 2 * 10.00
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)  # 1 * 20.00

        self.assertEqual(self.cart.total_price, Decimal('40.00'))  # (2 * 10.00) + (1 * 20.00)

    def test_cart_item_count(self):
        # Test item count in the cart
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        self.assertEqual(self.cart.item_count, 2)  # Two distinct items in the cart

    def test_cart_clear(self):
        # Test clearing the cart
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        self.assertEqual(self.cart.item_count, 2)
        self.cart.clear_cart()  # Clear the cart
        self.assertEqual(self.cart.item_count, 0)  # Ensure the cart is empty

    def test_cart_str_representation(self):
        # Test the __str__ method of Cart
        self.assertEqual(str(self.cart), f'Cart of {self.user.username}')
"""

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password="123456/a",
         username="man-in-middle")
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name='TestCategory')
        self.product1 = Product.objects.create(
            owner=self.user,
            name="Product 1",
            price=Decimal('10.00'),
            stock=100,
            size=1,
            category=self.category
        )
        self.product2 = Product.objects.create(
            owner=self.user,
            name="Product 2",
            price=Decimal('20.00'),
            stock=50,
            size=2,
            category=self.category
        )
    def test_cart_item_creation(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=5)
        self.assertEqual(cart_item.quantity, 5)
        self.assertEqual(cart_item.cart.user, self.user)
        self.assertEqual(cart_item.cart, self.cart)
    
    def test_cart_item_total_price(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=10)
        excepted_price = 100.0
        self.assertEqual(cart_item.total_price, excepted_price)
    
    def test_cart_total_price(self):
        cart_item_1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        cart_item_2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=5)
        excepted_price = 120.0
        self.assertEqual(self.cart.total_price, excepted_price)

    def test_cart_clear(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        self.cart.clear_cart()
        self.assertEqual(self.cart.item_count, 0)
    
        
