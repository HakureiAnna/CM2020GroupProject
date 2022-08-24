import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")),
  }),
  actions: {
    async login(username, password) {
        const response = await axios.post(`https://localhost/api/login`, { user: username, pass:password }).then(
          (res) => {
            this.user = res.data.token;
            localStorage.setItem("user", JSON.stringify(this.user));
            router.push("/");
          }
        ).catch(error => {
          console.log(error);
          return {
            error: "Username / Password is incorrect / does not exist"
          }
      });
      this.message = response;
      return response;
    },
    async logout() {
      if (!this.user) return;

      // Update headers.
      axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem("user").replace(/["]/g, '')}`;

      const response = await axios.post(`https://localhost/api/logout`).then(
        (res) => {
          const response = res.data;
          console.log(response);
        }
      ).then(() => {
        this.user = null;
        localStorage.removeItem("user");
        router.push("/login");
      }).catch(error => {
        console.log(error);
      });
      this.message = response;
      return response;
    }
  },
});
