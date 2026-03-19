"""Smart Contracts Serializers"""

from rest_framework import serializers
from .models import SmartContract, ContractEvent, AWSManagedBlockchainConfig


class ContractEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractEvent
        fields = ['id', 'event_type', 'event_hash', 'block_number', 'transaction_hash', 'data', 'created_at']


class SmartContractSerializer(serializers.ModelSerializer):
    events = ContractEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = SmartContract
        fields = ['id', 'contract_type', 'status', 'contract_address', 'network',
                  'buyer_wallet', 'escrow_amount', 'delivery_deadline', 'events', 'created_at']
        read_only_fields = ['id', 'contract_address', 'created_at']


class SmartContractDetailSerializer(serializers.ModelSerializer):
    events = ContractEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = SmartContract
        fields = ['id', 'order', 'contract_type', 'status', 'contract_address', 'network',
                  'chain_id', 'buyer_wallet', 'seller_wallets', 'escrow_amount',
                  'delivery_deadline', 'dispute_period_days', 'deployment_tx_hash',
                  'activation_tx_hash', 'completion_tx_hash', 'events',
                  'deployed_at', 'activated_at', 'completed_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deployed_at', 'activated_at', 'completed_at']


class AWSBlockchainConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWSManagedBlockchainConfig
        fields = ['id', 'network_name', 'framework', 'region', 'is_active', 'rpc_endpoint', 'updated_at']
        read_only_fields = ['id', 'updated_at']
