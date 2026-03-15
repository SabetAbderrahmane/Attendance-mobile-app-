
import Axios from "axios";

export const api = Axios.create({
  baseURL: "http://10.0.2.2:8000/api/v1", // use your LAN IP for phone
  headers: {
    "Content-Type": "application/json",
  },
});
