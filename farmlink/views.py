"""Root views for FarmLink API"""

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint providing available endpoints"""
    return JsonResponse({
        "message": "Welcome to FarmLink API",
        "version": "1.0",
        "endpoints": {
            "admin": "/admin/",
            "farmers": "/api/farmers/",
            "buyers": "/api/buyers/",
            "product_pools": "/api/products/pools/",
            "orders": "/api/orders/",
            "smart_contracts": "/api/smartcontracts/contracts/",
        },
        "documentation": "See ARCHITECTURE.md for API documentation"
    })


@require_http_methods(["GET"])
def home(request):
    """Frontend landing page showing API information"""
    context = {
        "message": "Welcome to FarmLink API",
        "version": "1.0",
        "endpoints": {
            "Admin": "/admin/",
            "Farmers": "/api/farmers/",
            "Buyers": "/api/buyers/",
            "Products": "/api/products/pools/",
            "Orders": "/api/orders/",
            "Smart Contracts": "/api/smartcontracts/contracts/",
        },
        "documentation_url": "/ARCHITECTURE.md",
    }
    return render(request, "index.html", context)
