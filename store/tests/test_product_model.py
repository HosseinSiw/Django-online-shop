from django.test import TestCase
from decimal import Decimal
from ..models import Product, Category
from users.models import CustomUser as User


class ProductModelTest(TestCase):

    def setUp(self):
        # Create a user for the Product owner
        self.user = User.objects.create_user(email='man-of-war@gmail.com', username='testuser', password='12345')
        # Create a category for the Product
        self.category = Category.objects.create(name='TestCategory')

    def test_product_creation(self):
        # Create a Product
        product = Product.objects.create(
            owner=self.user,
            name="Test Product",
            price=Decimal('10.50'),
            stock=10,
            size=1,
            category=self.category
        )
        # Verify that the product was created
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, Decimal('10.50'))
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.category, self.category)

    def test_stock_positive(self):
        # Ensure stock is positive (PositiveIntegerField enforces this)
        product = Product.objects.create(
            owner=self.user,
            name="Positive Stock Product",
            price=Decimal('5.00'),
            stock=5,
            size=1,
            category=self.category
        )
        self.assertGreaterEqual(product.stock, 0)

    def test_slug_generation(self):
        # Create a product and ensure the slug is generated based on the name
        product = Product.objects.create(
            owner=self.user,
            name="Slug Test Product",
            price=Decimal('10.00'),
            stock=10,
            size=1,
            category=self.category
        )
        self.assertEqual(product.slug, 'slug-test-product')

    def test_get_relative_url(self):
        # Test get_relative_url method
        product = Product.objects.create(
            owner=self.user,
            name="Test URL Product",
            price=Decimal('15.00'),
            stock=20,
            size=1,
            category=self.category
        )
        self.assertEqual(product.get_relative_url(), f'/{product.slug}/')

    def test_get_owner_username(self):
        # Test get_owner_username method
        product = Product.objects.create(
            owner=self.user,
            name="Owner Test Product",
            price=Decimal('20.00'),
            stock=30,
            size=1,
            category=self.category
        )
        self.assertEqual(product.get_owner_username(), self.user.username)

    def test_get_owner_id(self):
        # Test get_owner_id method
        product = Product.objects.create(
            owner=self.user,
            name="Owner ID Test Product",
            price=Decimal('25.00'),
            stock=15,
            size=1,
            category=self.category
        )
        self.assertEqual(product.get_owner_id(), self.user.id)

    def test_get_category_name(self):
        # Test get_category_name method
        product = Product.objects.create(
            owner=self.user,
            name="Category Test Product",
            price=Decimal('30.00'),
            stock=25,
            size=1,
            category=self.category
        )
        self.assertEqual(product.get_category_name(), self.category.name)
