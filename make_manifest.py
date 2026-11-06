from ledger_state import build_state


if __name__ == "__main__":
    result = build_state()
    print({key: result[key] for key in ("discoveredFunctions", "functionMatched", "sourceMatchedBytes", "sourceLinkedBytes", "exactContainerMatchWithScaffolding", "sourceReconstructionComplete")})
