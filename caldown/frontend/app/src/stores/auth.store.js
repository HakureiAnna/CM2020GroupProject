import { defineStore } from "pinia";

import { fetchWrapper, router } from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem("user")),
  }),
  actions: {
    async login(username, password) {
      const user = await fetchWrapper.post(`${baseUrl}/authenticate`, {
        username,
        password,
      });

      // update pinia state
      this.user = user;

      // store user details and jwt in local storage to keep user logged in between page refreshes
      localStorage.setItem("user", JSON.stringify(user));

      // redirect to previous url or default to home page
      router.push("/");
    },
    async signup(username, password, confirmed_password) {
      if (password !== confirmed_password) {
        console.log("Error: Password Does Not Match");
        return;
      }
      router.push("/login");
    },
    logout() {
      this.user = null;
      localStorage.removeItem("user");
      router.push("/login");
    },
  },
});