from math import log10

from .errors import DomainValidationError

def compute_rsi(cbr: float, thickness_e: float) -> float:
    if cbr <= 0:
        raise DomainValidationError("CBR doit être strictement positif.")
    if thickness_e <= 0:
        raise DomainValidationError("L'épaisseur e doit être strictement positive.")

    log_term = log10(cbr / 0.6)
    denominator = (
        4.231
        - 5.013 * log_term
        + 2.426 * (log_term**2)
        - 0.473 * (log_term**3)
    )

    if denominator == 0:
        raise DomainValidationError(
            "Le dénominateur de la formule RSI est nul pour ces valeurs."
        )

    return (thickness_e**2 / 1000.0) * (6.12 / denominator)


def compute_pcn(h_cbr: float, cbr: float, thickness_e: float) -> float:
    if h_cbr <= 0:
        raise DomainValidationError("H(CBR) doit être strictement positif.")

    rsi_value = compute_rsi(cbr=cbr, thickness_e=thickness_e)
    return h_cbr * rsi_value
