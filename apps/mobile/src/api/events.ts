import { api } from "./client";

export const listEvents = async (token: string) => {
  const response = await api.get("/events", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data; // array of events
};

export const checkInWithQR = async (token: string, qrToken: string) => {
  const response = await api.post(
    "/attendance/check-in",
    { qr_token: qrToken },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};
