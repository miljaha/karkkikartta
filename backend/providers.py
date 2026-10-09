PROVIDERS = {
    "K-Market": "Candy King",
    "K-Citymarket": "Candy King",
    "K-Supermarket": "Candy King",
    "S-market": "Irtonamuja",
    "Sale": "Irtonamuja",
    "Alepa": "Irtonamuja",
    "Prisma": "Irtonamuja",
    "Lidl": "Sweet Corner",
}

_LOOKUP = {chain.lower(): provider for chain, provider in PROVIDERS.items()}


def default_provider(chain):
    return _LOOKUP.get((chain or "").lower())
