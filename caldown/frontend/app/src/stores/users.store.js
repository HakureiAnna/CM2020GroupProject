import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useUsersStore = defineStore({
  id: "users",
  state: () => ({
    users: {},
    user: {},
    message: {}
  }),
  actions: {
    async signUp(username, password, confirmed_password) {
      if (password !== confirmed_password) {
        console.log("Error: Password Does Not Match");
      }
      const response = await axios.post(`https://localhost/api/signup`, { user:username, pass:password })
        .then(
          (res) => {
            if (res.data.token) {
              router.push("/login");
              return res.data;
            } else {
              return res.data;
            }
          }
        ).catch(error => {
          let status = error.response.status;
          let error_message = {
            400: "invalid data/data types",
            405: "Unknown Error, Please contact customer support"
          };
          return error_message[status];
      });

      this.message.response = response;
      return response;
    },
    async getAll() {
      await axios.get(`https://localhost/api/users`).then(
        (res) => (this.users = res.data)
      );
    },
  },
});
