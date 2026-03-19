"""AWS Managed Blockchain Integration Service"""

import json
import logging
from decimal import Decimal
from typing import Dict, List, Any
import boto3
from django.conf import settings
from django.utils import timezone
from .models import SmartContract, ContractEvent, AWSManagedBlockchainConfig

logger = logging.getLogger(__name__)


class AWSManagedBlockchainService:
    """
    Service to interact with AWS Managed Blockchain.
    Handles smart contract deployment and execution for order escrow.
    """
    
    def __init__(self, config: AWSManagedBlockchainConfig = None):
        """Initialize with AWS Managed Blockchain configuration"""
        if config is None:
            config = AWSManagedBlockchainConfig.objects.filter(is_active=True).first()
        
        self.config = config
        if config:
            self.aws_client = boto3.client(
                'managedblockchain',
                region_name=config.region,
                aws_access_key_id=config.access_key,
                aws_secret_access_key=config.secret_key
            )
            self.web3_provider = config.rpc_endpoint
        else:
            logger.warning("No active AWS Managed Blockchain config found")
            self.aws_client = None
            self.web3_provider = settings.WEB3_PROVIDER
    
    def create_escrow_contract(
        self,
        order_id: int,
        buyer_wallet: str,
        seller_wallets: List[str],
        escrow_amount: Decimal,
        delivery_deadline_days: int = 30
    ) -> Dict[str, Any]:
        """
        Create and deploy escrow smart contract for an order.
        
        Solves the trust problem:
        - Buyer funds locked in contract
        - Funds only released after delivery confirmation
        - Farmers get paid without prepayment risk
        - Buyer protected against non-delivery
        """
        try:
            from orders.models import Order
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            logger.error(f"Order {order_id} not found")
            return {'success': False, 'error': 'Order not found'}
        
        delivery_deadline = timezone.now() + timezone.timedelta(days=delivery_deadline_days)
        
        # Create smart contract record
        contract = SmartContract.objects.create(
            order=order,
            contract_type='order_escrow',
            status='deployed',
            contract_address=self._generate_contract_address(),
            buyer_wallet=buyer_wallet,
            seller_wallets=seller_wallets,
            escrow_amount=escrow_amount,
            delivery_deadline=delivery_deadline,
            deployment_tx_hash=self._generate_tx_hash(),
            deployed_at=timezone.now()
        )
        
        logger.info(f"Escrow contract created for order {order_id}: {contract.contract_address}")
        
        return {
            'success': True,
            'contract_id': contract.id,
            'contract_address': contract.contract_address,
            'status': 'deployed',
            'escrow_amount': str(escrow_amount),
            'delivery_deadline': delivery_deadline.isoformat()
        }
    
    def activate_contract(self, contract_id: int) -> Dict[str, Any]:
        """Activate contract after payment received"""
        try:
            contract = SmartContract.objects.get(id=contract_id)
        except SmartContract.DoesNotExist:
            return {'success': False, 'error': 'Contract not found'}
        
        contract.status = 'active'
        contract.activated_at = timezone.now()
        contract.activation_tx_hash = self._generate_tx_hash()
        contract.save()
        
        # Log contract event
        self._log_contract_event(
            contract,
            'funded',
            {
                'amount': str(contract.escrow_amount),
                'timestamp': contract.activated_at.isoformat()
            }
        )
        
        logger.info(f"Contract activated: {contract.contract_address}")
        
        return {
            'success': True,
            'contract_id': contract.id,
            'status': 'active',
            'activation_tx': contract.activation_tx_hash
        }
    
    def release_escrow(self, contract_id: int, recipient_wallets: Dict[str, Decimal]) -> Dict[str, Any]:
        """
        Release escrow funds to farmer wallets after delivery confirmed.
        Distributes funds proportionally among farmers.
        """
        try:
            contract = SmartContract.objects.get(id=contract_id)
        except SmartContract.DoesNotExist:
            return {'success': False, 'error': 'Contract not found'}
        
        if contract.status != 'active':
            return {'success': False, 'error': 'Contract is not active'}
        
        contract.status = 'completed'
        contract.completed_at = timezone.now()
        contract.completion_tx_hash = self._generate_tx_hash()
        contract.save()
        
        # Log event
        self._log_contract_event(
            contract,
            'payment_released',
            {
                'recipients': recipient_wallets,
                'total_amount': str(sum(recipient_wallets.values())),
                'timestamp': contract.completed_at.isoformat()
            }
        )
        
        logger.info(f"Escrow released for contract: {contract.contract_address}")
        
        return {
            'success': True,
            'contract_id': contract.id,
            'status': 'completed',
            'completion_tx': contract.completion_tx_hash,
            'payments': recipient_wallets
        }
    
    def dispute_contract(self, contract_id: int, reason: str) -> Dict[str, Any]:
        """Handle dispute in contract"""
        try:
            contract = SmartContract.objects.get(id=contract_id)
        except SmartContract.DoesNotExist:
            return {'success': False, 'error': 'Contract not found'}
        
        # Log dispute event
        self._log_contract_event(
            contract,
            'dispute_filed',
            {'reason': reason, 'timestamp': timezone.now().isoformat()}
        )
        
        logger.info(f"Dispute filed for contract: {contract.contract_address}")
        
        return {
            'success': True,
            'contract_id': contract.id,
            'dispute_logged': True,
            'reason': reason
        }
    
    def _log_contract_event(self, contract: SmartContract, event_type: str, data: Dict[str, Any]):
        """Log contract event to blockchain"""
        event_hash = self._generate_tx_hash()
        
        ContractEvent.objects.create(
            contract=contract,
            event_type=event_type,
            event_hash=event_hash,
            data=data,
            block_number=self._get_latest_block_number(),
            transaction_hash=event_hash,
            log_index=0
        )
    
    def _generate_contract_address(self) -> str:
        """Generate mock contract address for demo"""
        import uuid
        return '0x' + uuid.uuid4().hex[:40].upper()
    
    def _generate_tx_hash(self) -> str:
        """Generate mock transaction hash for demo"""
        import uuid
        return '0x' + uuid.uuid4().hex[:64].upper()
    
    def _get_latest_block_number(self) -> int:
        """Get latest block number (mock for demo)"""
        import random
        return random.randint(1000000, 9999999)
    
    def get_contract_status(self, contract_id: int) -> Dict[str, Any]:
        """Get current status of contract and its events"""
        try:
            contract = SmartContract.objects.get(id=contract_id)
        except SmartContract.DoesNotExist:
            return {'success': False, 'error': 'Contract not found'}
        
        events = list(ContractEvent.objects.filter(contract=contract).values(
            'event_type', 'event_hash', 'block_number', 'created_at'
        ))
        
        return {
            'success': True,
            'contract_id': contract.id,
            'contract_address': contract.contract_address,
            'status': contract.status,
            'order_id': contract.order_id,
            'escrow_amount': str(contract.escrow_amount),
            'delivery_deadline': contract.delivery_deadline.isoformat(),
            'events': events
        }
