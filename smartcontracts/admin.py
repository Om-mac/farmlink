from django.contrib import admin
from .models import SmartContract, ContractEvent, AWSManagedBlockchainConfig


@admin.register(SmartContract)
class SmartContractAdmin(admin.ModelAdmin):
    list_display = ('contract_address', 'contract_type', 'status', 'escrow_amount', 'created_at')
    list_filter = ('status', 'contract_type', 'network')
    search_fields = ('contract_address', 'order__id')
    fieldsets = (
        ('Basic Info', {'fields': ('contract_type', 'status', 'order')}),
        ('Blockchain', {'fields': ('contract_address', 'network', 'chain_id')}),
        ('Participants', {'fields': ('buyer_wallet', 'seller_wallets')}),
        ('Contract Terms', {'fields': ('escrow_amount', 'delivery_deadline', 'dispute_period_days')}),
        ('Transactions', {'fields': ('deployment_tx_hash', 'activation_tx_hash', 'completion_tx_hash')}),
        ('Timeline', {'fields': ('deployed_at', 'activated_at', 'completed_at')}),
    )
    readonly_fields = ('deployed_at', 'activated_at', 'completed_at')


@admin.register(ContractEvent)
class ContractEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'contract', 'event_hash', 'block_number', 'created_at')
    list_filter = ('event_type', 'created_at', 'contract__network')
    search_fields = ('event_hash', 'contract__contract_address')


@admin.register(AWSManagedBlockchainConfig)
class AWSManagedBlockchainConfigAdmin(admin.ModelAdmin):
    list_display = ('network_name', 'framework', 'region', 'is_active', 'updated_at')
    list_filter = ('framework', 'region', 'is_active')
    fieldsets = (
        ('Network', {'fields': ('network_name', 'framework', 'network_id', 'member_id')}),
        ('RPC Endpoint', {'fields': ('rpc_endpoint', 'rpc_username', 'rpc_password')}),
        ('AWS Credentials', {'fields': ('access_key', 'secret_key', 'region')}),
        ('Smart Contract', {'fields': ('smart_contract_arn', 'contract_deployed_address')}),
        ('Status', {'fields': ('is_active',)}),
    )
