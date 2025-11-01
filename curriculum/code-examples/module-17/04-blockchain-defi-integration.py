"""
Module 17.7: Blockchain & DeFi Integration
Complete implementation for on-chain data monitoring and DEX trading

This demonstrates how to connect to blockchain networks, monitor whale wallets,
track DEX prices, and execute trades on decentralized exchanges.

⚠️  SECURITY WARNING: Never commit private keys to version control!
Use environment variables or hardware wallets for production.
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware
import asyncio
import time
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# BLOCKCHAIN CONNECTION
# ============================================================================

def connect_to_blockchain(infura_url: str) -> Web3:
    """
    Connect to Ethereum blockchain via Infura/Alchemy
    
    Args:
        infura_url: Your Infura/Alchemy project URL
        
    Returns:
        Web3 instance connected to blockchain
    """
    w3 = Web3(Web3.HTTPProvider(infura_url))
    
    # For sidechains (Polygon, BSC), inject PoA middleware
    # w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    if w3.is_connected():
        logger.info(f"✅ Connected to Ethereum - Block: {w3.eth.block_number}")
    else:
        logger.error("❌ Failed to connect to blockchain")
    
    return w3


# ============================================================================
# WHALE WALLET MONITORING
# ============================================================================

class WhaleMonitor:
    """Track large wallet movements to detect accumulation/distribution"""
    
    def __init__(self, w3: Web3, whale_wallets: list, min_value_usd: float = 100000):
        self.w3 = w3
        self.whale_wallets = [w.lower() for w in whale_wallets]
        self.min_value_usd = min_value_usd
    
    async def monitor_transfers(self, token_address: str, blocks_back: int = 100) -> list:
        """
        Monitor ERC-20 token transfers from whale wallets
        
        Args:
            token_address: Token contract address
            blocks_back: How many blocks to look back
            
        Returns:
            List of significant whale transfers
        """
        # ERC-20 Transfer event signature
        transfer_topic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        
        latest_block = self.w3.eth.block_number
        from_block = latest_block - blocks_back
        
        logger.info(f"Scanning blocks {from_block} to {latest_block} for whale transfers...")
        
        # Get Transfer events
        logs = self.w3.eth.get_logs({
            'fromBlock': from_block,
            'toBlock': 'latest',
            'address': token_address,
            'topics': [transfer_topic]
        })
        
        whale_transfers = []
        for log in logs:
            # Decode addresses from topics (32 bytes -> 20 bytes address)
            from_address = "0x" + log['topics'][1].hex()[-40:]
            to_address = "0x" + log['topics'][2].hex()[-40:]
            value = int(log['data'].hex(), 16)
            
            if from_address.lower() in self.whale_wallets:
                whale_transfers.append({
                    'from': from_address,
                    'to': to_address,
                    'value': value,
                    'tx_hash': log['transactionHash'].hex(),
                    'block': log['blockNumber'],
                    'direction': 'SELLING' if self._is_exchange(to_address) else 'TRANSFERRING'
                })
        
        logger.info(f"Found {len(whale_transfers)} whale transfers")
        return whale_transfers
    
    def _is_exchange(self, address: str) -> bool:
        """Check if address belongs to a known exchange"""
        # Add known exchange addresses
        known_exchanges = [
            # Binance, Coinbase, Kraken hot wallets, etc.
        ]
        return address.lower() in known_exchanges


# ============================================================================
# DEX PRICE MONITORING (Uniswap V3)
# ============================================================================

class UniswapMonitor:
    """Monitor Uniswap V3 prices and liquidity"""
    
    UNISWAP_V3_FACTORY = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
    
    def __init__(self, w3: Web3):
        self.w3 = w3
        # Load ABIs (you'll need to provide these)
        self.factory_abi = self._load_abi('uniswap_v3_factory.json')
        self.pool_abi = self._load_abi('uniswap_v3_pool.json')
        
        self.factory = w3.eth.contract(
            address=self.UNISWAP_V3_FACTORY,
            abi=self.factory_abi
        )
    
    def get_pool_address(self, token0: str, token1: str, fee: int = 3000) -> str:
        """
        Get Uniswap pool address for token pair
        
        Args:
            token0: First token address
            token1: Second token address
            fee: Fee tier (500 = 0.05%, 3000 = 0.3%, 10000 = 1%)
        """
        return self.factory.functions.getPool(token0, token1, fee).call()
    
    def get_pool_price(self, pool_address: str) -> float:
        """Get current price from Uniswap pool"""
        pool = self.w3.eth.contract(address=pool_address, abi=self.pool_abi)
        
        # Get slot0 (contains sqrtPriceX96)
        slot0 = pool.functions.slot0().call()
        sqrt_price_x96 = slot0[0]
        
        # Convert sqrtPriceX96 to actual price
        price = (sqrt_price_x96 / (2 ** 96)) ** 2
        
        return price
    
    async def watch_pool_price(self, pool_address: str, callback, interval: int = 2):
        """
        Watch pool price and call callback on changes
        
        Args:
            pool_address: Uniswap pool address
            callback: Async function to call with (price, event)
            interval: Polling interval in seconds
        """
        pool = self.w3.eth.contract(address=pool_address, abi=self.pool_abi)
        swap_filter = pool.events.Swap.create_filter(fromBlock='latest')
        
        logger.info(f"👀 Watching pool {pool_address} for price changes...")
        
        while True:
            for event in swap_filter.get_new_entries():
                price = self.get_pool_price(pool_address)
                await callback(price, event)
            
            await asyncio.sleep(interval)
    
    def _load_abi(self, filename: str):
        """Load ABI from file"""
        # Implementation: load JSON ABI file
        pass


# ============================================================================
# DEX TRADING (Uniswap V3)
# ============================================================================

class UniswapTrader:
    """Execute trades on Uniswap V3"""
    
    UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
    
    def __init__(self, w3: Web3, private_key: str):
        """
        ⚠️  WARNING: In production, NEVER pass private keys directly.
        Use environment variables or hardware wallets.
        """
        self.w3 = w3
        self.account = w3.eth.account.from_key(private_key)
        self.router_abi = self._load_abi('uniswap_v3_router.json')
        self.router = w3.eth.contract(
            address=self.UNISWAP_V3_ROUTER,
            abi=self.router_abi
        )
    
    async def swap_exact_input(
        self,
        token_in: str,
        token_out: str,
        amount_in: int,
        amount_out_min: int,
        fee: int = 3000,
        deadline_seconds: int = 300
    ) -> str:
        """
        Execute a swap on Uniswap V3
        
        Args:
            token_in: Input token address
            token_out: Output token address
            amount_in: Amount of input token (in wei/base units)
            amount_out_min: Minimum output amount (slippage protection)
            fee: Fee tier
            deadline_seconds: Transaction deadline from now
            
        Returns:
            Transaction hash
        """
        params = {
            'tokenIn': token_in,
            'tokenOut': token_out,
            'fee': fee,
            'recipient': self.account.address,
            'deadline': int(time.time()) + deadline_seconds,
            'amountIn': amount_in,
            'amountOutMinimum': amount_out_min,
            'sqrtPriceLimitX96': 0
        }
        
        # Build transaction
        swap_txn = self.router.functions.exactInputSingle(params).build_transaction({
            'from': self.account.address,
            'gas': 250000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        
        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(swap_txn, self.account.key)
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"🔄 Swap submitted: {tx_hash.hex()}")
        
        # Wait for confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt['status'] == 1:
            logger.info(f"✅ Swap successful!")
        else:
            logger.error(f"❌ Swap failed!")
        
        return tx_hash.hex()
    
    def _load_abi(self, filename: str):
        """Load ABI from file"""
        pass


# ============================================================================
# GAS PRICE MONITORING
# ============================================================================

class GasMonitor:
    """Monitor gas prices for optimal transaction timing"""
    
    def __init__(self, w3: Web3):
        self.w3 = w3
    
    def get_gas_prices(self) -> dict:
        """Get current gas prices in gwei"""
        latest_block = self.w3.eth.get_block('latest')
        base_fee = latest_block['baseFeePerGas']
        max_priority_fee = self.w3.eth.max_priority_fee
        
        return {
            'base_fee_gwei': self.w3.from_wei(base_fee, 'gwei'),
            'priority_fee_gwei': self.w3.from_wei(max_priority_fee, 'gwei'),
            'total_gwei': self.w3.from_wei(base_fee + max_priority_fee, 'gwei')
        }
    
    async def wait_for_low_gas(self, threshold_gwei: int = 30, check_interval: int = 60):
        """Wait until gas prices drop below threshold"""
        logger.info(f"⏳ Waiting for gas < {threshold_gwei} gwei...")
        
        while True:
            gas = self.get_gas_prices()
            if gas['total_gwei'] < threshold_gwei:
                logger.info(f"✅ Gas price acceptable: {gas['total_gwei']:.2f} gwei")
                return gas
            
            logger.info(f"💸 Gas too high: {gas['total_gwei']:.2f} gwei. Waiting...")
            await asyncio.sleep(check_interval)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of blockchain integration"""
    
    # Connect to blockchain
    infura_url = "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
    w3 = connect_to_blockchain(infura_url)
    
    # Monitor whale wallets
    whale_monitor = WhaleMonitor(
        w3=w3,
        whale_wallets=["0x123...", "0x456..."],
        min_value_usd=100000
    )
    
    # Check for whale transfers
    transfers = await whale_monitor.monitor_transfers(
        token_address="0x...",  # USDC, USDT, etc.
        blocks_back=100
    )
    
    print(f"Found {len(transfers)} whale transfers")
    
    # Monitor gas prices
    gas_monitor = GasMonitor(w3)
    gas_prices = gas_monitor.get_gas_prices()
    print(f"Current gas: {gas_prices['total_gwei']:.2f} gwei")


if __name__ == "__main__":
    asyncio.run(main())

