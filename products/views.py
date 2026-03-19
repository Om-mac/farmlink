"""Products Views - Aggregation Engine"""

from decimal import Decimal

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Avg, Count
from .models import AggregatedProductPool, QualityAssurance
from .serializers import (
    AggregatedProductPoolSerializer,
    AggregatedProductPoolDetailSerializer,
    BuyerRequirementSerializer,
)
from farmers.models import FarmProduct


class AggregatedProductPoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet for aggregated product pools.
    Solves scale mismatch by combining multiple farmer products.
    """
    queryset = AggregatedProductPool.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name']
    ordering_fields = ['created_at', 'total_available_kg', 'average_price_per_kg']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AggregatedProductPoolDetailSerializer
        return AggregatedProductPoolSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def create_aggregation(self, request):
        """
        Admin action to create a new aggregated pool from similar farmer products.
        This is the core of the aggregation engine.
        """
        product_name = request.data.get('product_name')
        target_quantity_kg = request.data.get('target_quantity_kg')
        
        if not product_name or not target_quantity_kg:
            return Response(
                {'error': 'product_name and target_quantity_kg required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            target_quantity_kg = float(target_quantity_kg)
        except (ValueError, TypeError):
            return Response(
                {'error': 'target_quantity_kg must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find verified farmers with this product
        farm_products = FarmProduct.objects.filter(
            product_name__icontains=product_name,
            verified=True,
            farmer__verified=True
        )
        
        if not farm_products.exists():
            return Response(
                {'error': f'No verified farmers found for {product_name}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate aggregation metrics
        total_available = farm_products.aggregate(Sum('daily_capacity_kg'))['daily_capacity_kg__sum'] or 0
        avg_price = farm_products.aggregate(Avg('price_per_kg'))['price_per_kg__avg'] or 0
        
        # Create the aggregated pool
        pool = AggregatedProductPool.objects.create(
            product_name=product_name,
            total_available_kg=total_available,
            target_quantity_kg=target_quantity_kg,
            average_price_per_kg=avg_price,
            status='open'
        )
        pool.source_products.set(farm_products)
        
        # Create quality assurance record
        QualityAssurance.objects.create(pool=pool, status='pending')
        
        serializer = AggregatedProductPoolDetailSerializer(pool)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def search_by_quantity(self, request):
        """Find pools that can fulfill a specific quantity requirement"""
        required_kg = request.query_params.get('quantity_kg')
        
        if not required_kg:
            return Response(
                {'error': 'quantity_kg query parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            required_kg = float(required_kg)
        except (ValueError, TypeError):
            return Response(
                {'error': 'quantity_kg must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find open pools with enough capacity
        pools = AggregatedProductPool.objects.filter(
            status='open',
            total_available_kg__gte=required_kg
        )
        
        serializer = AggregatedProductPoolSerializer(pools, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def participating_farmers(self, request, pk=None):
        """Get list of farmers participating in this pool"""
        pool = self.get_object()
        farmers = pool.source_products.values('farmer').distinct()
        from farmers.models import Farmer
        from farmers.serializers import FarmerSerializer
        
        farmer_objs = Farmer.objects.filter(id__in=[f['farmer'] for f in farmers])
        serializer = FarmerSerializer(farmer_objs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def match_requirement(self, request):
        """
        Buyer submits quantity requirement (e.g. 10 ton).
        API returns merged farmer product list that can fulfill demand.
        """
        serializer = BuyerRequirementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        required_kg = data.get('required_quantity_kg')
        if not required_kg:
            required_kg = float(data['required_quantity_ton']) * 1000

        grade_rank = {'A': 3, 'B': 2, 'C': 1}
        minimum_grade = data.get('minimum_quality_grade', 'C')

        products = FarmProduct.objects.filter(
            product_name__icontains=data['product_name'],
            is_active=True,
            farmer__verified=True,
            verified=True,
            available_quantity_kg__gt=0,
        ).select_related('farmer')

        if data.get('product_category'):
            products = products.filter(product_category=data['product_category'])
        if data.get('max_price_per_kg') is not None:
            products = products.filter(price_per_kg__lte=data['max_price_per_kg'])
        if data.get('require_quality_certificate'):
            products = products.exclude(quality_certificate='')

        products = sorted(
            list(products),
            key=lambda p: (
                -grade_rank.get(p.quality_grade, 0),
                float(p.price_per_kg),
                -float(p.available_quantity_kg),
            )
        )
        products = [p for p in products if grade_rank.get(p.quality_grade, 0) >= grade_rank[minimum_grade]]

        selected = []
        accumulated_kg = 0.0
        total_price_weighted = Decimal("0")

        for product in products:
            if accumulated_kg >= required_kg:
                break
            remaining = required_kg - accumulated_kg
            take_kg = min(float(product.available_quantity_kg), remaining)
            if take_kg <= 0:
                continue

            line_value = Decimal(str(take_kg)) * product.price_per_kg
            total_price_weighted += line_value
            accumulated_kg += take_kg

            selected.append({
                'farm_product_id': product.id,
                'farmer_id': product.farmer.id,
                'farmer_name': product.farmer.farm_name,
                'farmer_location': product.farmer.location,
                'product_name': product.product_name,
                'quality_grade': product.quality_grade,
                'price_per_kg': float(product.price_per_kg),
                'allocated_quantity_kg': round(take_kg, 2),
                'quality_certificate': bool(product.quality_certificate),
                'product_photo': bool(product.product_photo),
            })

        can_fulfill = accumulated_kg >= required_kg
        avg_price = float(total_price_weighted / Decimal(str(accumulated_kg))) if accumulated_kg > 0 else 0.0

        return Response({
            'request': {
                'product_name': data['product_name'],
                'required_quantity_kg': round(required_kg, 2),
                'required_quantity_ton': round(required_kg / 1000, 3),
            },
            'can_fulfill': can_fulfill,
            'selected_farmers_count': len({item['farmer_id'] for item in selected}),
            'allocated_quantity_kg': round(accumulated_kg, 2),
            'allocated_quantity_ton': round(accumulated_kg / 1000, 3),
            'weighted_average_price_per_kg': round(avg_price, 2),
            'selected_products': selected,
            'message': (
                'Requirement fulfilled using merged farmers.'
                if can_fulfill else
                'Insufficient current supply for full requirement.'
            )
        })
