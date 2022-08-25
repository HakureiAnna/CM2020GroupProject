import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useUsersStore = defineStore({
  id: "users",
  state: () => ({
    message: {}
  }),
  actions: {
    async signUp(username, password, confirmed_password) {
      if (password !== confirmed_password) {
        return;
      }
      await axios.post(`https://localhost/api/signup`, { user:username, pass:password })
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
          this.message.error = error_message[status];
      });
    },
  },
});
