from .models import Product, Category

class ProductService:

    @staticmethod
    def get_product_list_by_category(category_id):
        products = Product.objects.filter(category_id=category_id)
        return products
