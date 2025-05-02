import requests
from enum import Enum
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

BASE_URL = "https://api.dexscreener.com/token-pairs/v1"

app = FastAPI(title="Token Pool API", version="1.0.0")

class Chain(str, Enum):
    SOLANA = "solana"
    ETHEREUM = "ethereum"

class Token(BaseModel):
    chain: Chain
    address: str

class PoolInfo(BaseModel):
    pool_address: str
    url: str
    liquidity_usd: float
    volume_24h: float
    dex_id: str
    price_usd: float

class TokenPoolResponse(BaseModel):
    chain: Chain
    token_address: str
    largest_pool: PoolInfo
    total_liquidity_usd: float
    number_of_pools: int

class TokenPoolsBatchResponse(BaseModel):
    results: List[TokenPoolResponse]

def get_token_pools(chain: Chain, token_address: str) -> TokenPoolResponse:
    url = f"{BASE_URL}/{chain.value}/{token_address}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    pairs = response.json()
    if not pairs:
        raise HTTPException(status_code=404, detail="No pools found for token")
    
    # Find largest pool by USD liquidity
    largest_pool = max(pairs, key=lambda x: float(x.get("liquidity", {}).get("usd", 0)))
    
    # Calculate total liquidity
    total_liquidity = sum(float(pool.get("liquidity", {}).get("usd", 0)) for pool in pairs)
    
    return TokenPoolResponse(
        chain=chain,
        token_address=token_address,
        largest_pool=PoolInfo(
            pool_address=largest_pool["pairAddress"],
            url=largest_pool["url"],
            liquidity_usd=float(largest_pool.get("liquidity", {}).get("usd", 0)),
            volume_24h=float(largest_pool.get("volume", {}).get("h24", 0)),
            dex_id=largest_pool["dexId"],
            price_usd=float(largest_pool.get("priceUsd", 0))
        ),
        total_liquidity_usd=total_liquidity,
        number_of_pools=len(pairs)
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/token/{chain}/{token_address}", response_model=TokenPoolResponse)
async def get_token_pool_info(chain: Chain, token_address: str):
    print(f"Getting token pool info for {chain} {token_address}")
    return get_token_pools(chain, token_address)

@app.post("/tokens/batch", response_model=TokenPoolsBatchResponse)
async def get_token_pools_batch(tokens: List[Token]):
    results = []
    for token in tokens:
        try:
            result = get_token_pools(token.chain, token.address)
            results.append(result)
        except HTTPException:
            continue
    return TokenPoolsBatchResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
