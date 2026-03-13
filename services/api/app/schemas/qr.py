from pydantic import BaseModel


class QRTokenResponse(BaseModel):
    event_id: int
    qr_token: str


class QRCheckInRequest(BaseModel):
    qr_token: str
