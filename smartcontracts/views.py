"""Smart Contracts Views - Blockchain Integration"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SmartContract, AWSManagedBlockchainConfig
from .serializers import SmartContractSerializer, SmartContractDetailSerializer, AWSBlockchainConfigSerializer
from .blockchain_service import AWSManagedBlockchainService


class SmartContractViewSet(viewsets.ModelViewSet):
    """ViewSet for Smart Contracts - Blockchain Escrow System"""
    queryset = SmartContract.objects.all()
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SmartContractDetailSerializer
        return SmartContractSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def create_escrow(self, request):
        """Create escrow contract for an order"""
        order_id = request.data.get('order_id')
        buyer_wallet = request.data.get('buyer_wallet')
        seller_wallets = request.data.get('seller_wallets', [])
        delivery_days = request.data.get('delivery_days', 30)
        
        if not all([order_id, buyer_wallet, seller_wallets]):
            return Response(
                {'error': 'order_id, buyer_wallet, and seller_wallets required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from orders.models import Order
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Use blockchain service
        service = AWSManagedBlockchainService()
        result = service.create_escrow_contract(
            order_id=order_id,
            buyer_wallet=buyer_wallet,
            seller_wallets=seller_wallets,
            escrow_amount=order.total_amount,
            delivery_deadline_days=delivery_days
        )
        
        if result['success']:
            contract = SmartContract.objects.get(id=result['contract_id'])
            serializer = SmartContractDetailSerializer(contract)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def activate(self, request, pk=None):
        """Activate contract after payment"""
        service = AWSManagedBlockchainService()
        result = service.activate_contract(pk)
        
        if result['success']:
            contract = SmartContract.objects.get(id=pk)
            serializer = SmartContractDetailSerializer(contract)
            return Response(serializer.data)
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def release_funds(self, request, pk=None):
        """Release escrow funds after delivery confirmation"""
        recipient_wallets = request.data.get('recipient_wallets', {})
        
        if not recipient_wallets:
            return Response(
                {'error': 'recipient_wallets required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert to Decimal
        from decimal import Decimal
        recipient_wallets = {k: Decimal(str(v)) for k, v in recipient_wallets.items()}
        
        service = AWSManagedBlockchainService()
        result = service.release_escrow(pk, recipient_wallets)
        
        if result['success']:
            contract = SmartContract.objects.get(id=pk)
            serializer = SmartContractDetailSerializer(contract)
            return Response(serializer.data)
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def file_dispute(self, request, pk=None):
        """File dispute on contract"""
        reason = request.data.get('reason')
        
        if not reason:
            return Response(
                {'error': 'reason required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = AWSManagedBlockchainService()
        result = service.dispute_contract(pk, reason)
        
        if result['success']:
            contract = SmartContract.objects.get(id=pk)
            serializer = SmartContractDetailSerializer(contract)
            return Response(serializer.data)
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def status(self, request, pk=None):
        """Get contract status and events"""
        service = AWSManagedBlockchainService()
        result = service.get_contract_status(pk)
        return Response(result)


class AWSBlockchainConfigViewSet(viewsets.ModelViewSet):
    """ViewSet for AWS Managed Blockchain Configuration"""
    queryset = AWSManagedBlockchainConfig.objects.all()
    serializer_class = AWSBlockchainConfigSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def activate_config(self, request, pk=None):
        """Activate a blockchain configuration"""
        try:
            config = AWSManagedBlockchainConfig.objects.get(id=pk)
            # Deactivate others
            AWSManagedBlockchainConfig.objects.exclude(id=pk).update(is_active=False)
            config.is_active = True
            config.save()
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        except AWSManagedBlockchainConfig.DoesNotExist:
            return Response({'error': 'Config not found'}, status=status.HTTP_404_NOT_FOUND)
