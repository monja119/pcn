from dataclasses import dataclass

from pcn_app.domain.formulas import compute_pcn, compute_rsi


@dataclass(frozen=True)
class ComputePcnRequest:
    h_cbr: float
    cbr: float
    thickness_e: float


@dataclass(frozen=True)
class ComputePcnResponse:
    pcn: float
    rsi: float


class ComputePcnUseCase:
    def execute(self, request: ComputePcnRequest) -> ComputePcnResponse:
        rsi_value = compute_rsi(cbr=request.cbr, thickness_e=request.thickness_e)
        pcn_value = compute_pcn(
            h_cbr=request.h_cbr,
            cbr=request.cbr,
            thickness_e=request.thickness_e,
        )
        return ComputePcnResponse(pcn=pcn_value, rsi=rsi_value)
