import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")),
  }),
  actions: {
    async login(username, password) {
        await axios.post(`https://localhost/api/login`, { user: username, pass:password }).then(
          (res) => {
            this.user = res.data.token;
          }
        ).then(() => {
          localStorage.setItem("user", JSON.stringify(this.user));
          router.push("/");
        }).catch(error => {
        console.log(error);
      })
    },
    async logout() {
      if (!this.user) {
        console.log(`You are not logged in!`);
        return;
      }
      try {
        const message = await axios.post(`https://localhost/api/logout`).then(
          (res) => {
            console.log(res.data);
          }
        ).then(() => {
          this.user = null;
          localStorage.removeItem("user");
          router.push("/login");
        })
      } catch(error) {
        console.log(error);
      }
    },
  },
});
