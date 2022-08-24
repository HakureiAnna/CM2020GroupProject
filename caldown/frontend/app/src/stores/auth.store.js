import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")),
    message: {}
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
          let status = error.response.status;
          let error_message = {
            400: "invalid data/data types",
            401: "Non-existing/Wrong Username or Password",
            405: "Unknown Error, Please contact customer support"
          };
          this.message.error = error_message[status];
      });
      this.message.response = response;
      return response;
    },
    async logout() {
      if (!this.user) return;

      // Update headers.
      axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem("user").replace(/["]/g, '')}`;

      const response = await axios.post(`https://localhost/api/logout`).then(
        (res) => {
          const response = res.data;
          return response;
        }
      ).then(() => {
        this.user = null;
        localStorage.removeItem("user");
        router.push("/login");
      }).catch(error => {
        let status = error.response.status;
        let error_message = {
          401: "invalid token",
          405: "Unknown Error, Please contact customer support"
        };
        this.message.error = error_message[status];
      });
      this.message.response = response;
      return response;
    }
  },
});
