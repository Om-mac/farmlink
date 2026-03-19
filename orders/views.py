"""Orders Views - Purchase & Fulfillment"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Order, OrderDispute, PaymentTransaction
from .serializers import OrderSerializer, OrderDetailSerializer, OrderDisputeSerializer
from products.models import AggregatedProductPool


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Orders.
    Integrates with smart contracts for secure payment and trust.
    """
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'total_amount', 'status']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
    def get_queryset(self):
        """Filter orders for current user (buyer or farmer with access)"""
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        try:
            buyer = user.buyer_profile
            return Order.objects.filter(buyer=buyer)
        except:
            return Order.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user.buyer_profile)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def create_order(self, request):
        """
        Create a new order from aggregated pool.
        Automatically initiates smart contract escrow.
        """
        try:
            buyer = request.user.buyer_profile
        except:
            return Response(
                {'error': 'User is not a registered buyer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pool_id = request.data.get('pool_id')
        quantity_kg = request.data.get('quantity_kg')
        
        if not pool_id or not quantity_kg:
            return Response(
                {'error': 'pool_id and quantity_kg required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pool = AggregatedProductPool.objects.get(id=pool_id)
        except AggregatedProductPool.DoesNotExist:
            return Response(
                {'error': 'Pool not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            quantity_kg = float(quantity_kg)
        except (ValueError, TypeError):
            return Response(
                {'error': 'quantity_kg must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if quantity_kg > pool.total_available_kg:
            return Response(
                {'error': f'Requested quantity exceeds available ({pool.total_available_kg}kg)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create order with smart contract preparation
        from decimal import Decimal
        order = Order.objects.create(
            buyer=buyer,
            aggregated_pool=pool,
            quantity_kg=quantity_kg,
            unit_price=pool.average_price_per_kg,
            expected_delivery_date=timezone.now().date(),
            shipping_address=request.data.get('shipping_address', ''),
        )
        order.calculate_costs()
        order.save()
        
        # Note: Smart contract execution would happen here
        # For now, we prepare the contract info
        order.status = 'pending'
        order.save()
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def initiate_payment(self, request, pk=None):
        """
        Initiate smart contract payment (escrow).
        This is where blockchain trust mechanism kicks in.
        """
        order = self.get_object()
        
        if order.status != 'pending':
            return Response(
                {'error': 'Order is not in pending state'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simulate smart contract lock
        order.status = 'escrow_locked'
        order.smart_contract_id = f'0x_demo_{order.id}'
        order.payment_received_at = timezone.now()
        order.save()
        
        return Response({
            'status': 'payment initiated',
            'smart_contract_id': order.smart_contract_id,
            'amount_locked': str(order.total_amount),
            'order_id': order.id
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_shipped(self, request, pk=None):
        """Mark order as shipped by farmer"""
        order = self.get_object()
        
        if order.status != 'escrow_locked':
            return Response(
                {'error': 'Order must have payment locked before shipping'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'shipped'
        order.tracking_number = request.data.get('tracking_number', '')
        order.shipped_at = timezone.now()
        order.save()
        
        return Response({'status': 'order marked as shipped'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm_delivery(self, request, pk=None):
        """Confirm delivery and release smart contract funds"""
        order = self.get_object()
        
        if order.status != 'shipped':
            return Response(
                {'error': 'Order must be shipped first'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()
        
        # Simulate smart contract fund release
        order.status = 'completed'
        order.save()
        
        return Response({
            'status': 'delivery confirmed',
            'message': 'Smart contract funds released to farmers',
            'order_id': order.id
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def raise_dispute(self, request, pk=None):
        """Raise a dispute for an order"""
        order = self.get_object()
        
        reason = request.data.get('reason')
        description = request.data.get('description')
        
        if not reason or not description:
            return Response(
                {'error': 'reason and description required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dispute = OrderDispute.objects.create(
            order=order,
            initiated_by='buyer' if order.buyer.user == request.user else 'farmer',
            reason=reason,
            description=description
        )
        
        order.status = 'disputed'
        order.save()
        
        serializer = OrderDisputeSerializer(dispute)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
