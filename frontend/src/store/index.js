import { defineStore } from "pinia";
import api from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null
  }),

  actions: {
    async login(identifier, password) {
      const resp = await api.post("/auth/login", { identifier, password });

      if (resp.data.user) {
        this.user = resp.data.user;
      }

      return resp;
    },

    async logout() {
      await api.post("/auth/logout");
      this.user = null;
    },

    setUser(u) {
      this.user = u;
    }
  }
});
