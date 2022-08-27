import { defineStore } from "pinia";
import axios from "axios";

import { router, error_messages } from "@/helpers";

// handles basic user authentication
// login
// logout
// signup
export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")),
    message: {}
  }),
  actions: {
    async login(username, password) {
        await axios.post(`https://localhost/api/login`, { user: username, pass:password })
        .then((res) => {
            this.user = res.data.token;
            localStorage.setItem("user", JSON.stringify(res.data.token));
            router.push("/");
          })
        .catch((error) => {
          const status = error.response.status;
          this.message["login_error"] = error_messages[status];
      });
    },
    async logout() {
      if (!this.user) return;

      // Update headers.
      axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem("user").replace(/["]/g, '')}`;

      await axios.post(`https://localhost/api/logout`)
      .then((res) => {
          localStorage.removeItem("user");
          router.push("/login");
        })
      .catch((error) => {
        const status = error.response.status;
        this.message["logout_error"] = error_messages[status];
      });
    },
    async signUp(username, password, confirmed_password) {
      if (password !== confirmed_password) {
        return;
      }
      await axios.post(`https://localhost/api/signup`, { user:username, pass:password })
        .then((res) => {
            this.user = res.data.token;
            router.push("/");
          })
        .catch((error) => {
          const status = error.response.status;
          this.message["signup_error"] = error_messages[status];
      });
  }},
});
