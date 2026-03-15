import { makeAutoObservable } from "mobx";
import AsyncStorage from "@react-native-async-storage/async-storage";

class AuthStore {
  token: string | null = null;
  user: any = null;

  constructor() {
    makeAutoObservable(this);
    this.loadToken();
  }

  async loadToken() {
    const token = await AsyncStorage.getItem("token");
    if (token) this.token = token;
  }

  async setToken(token: string) {
    this.token = token;
    await AsyncStorage.setItem("token", token);
  }

  async logout() {
    this.token = null;
    this.user = null;
    await AsyncStorage.removeItem("token");
  }
}

export const authStore = new AuthStore();
