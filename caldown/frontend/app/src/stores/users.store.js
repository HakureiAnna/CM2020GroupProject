import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useUsersStore = defineStore({
  id: "users",
  state: () => ({
    users: {},
    user: {}
  }),
  actions: {
    async signUp(username, password, confirmed_password) {
      if (password !== confirmed_password) {
        console.log("Error: Password Does Not Match");
      }
      const response = await axios.post(`https://localhost/api/signup`, { user:username, pass:password }).then(
          (res) => {
            if (res.data.token) {
              router.push("/login");
              return res.data;
            } else {
              return res.data;
            }
          }
        ).catch(error => {
          console.log(`from stores ${error}`);

          // Bad Practice to return backend error to frontend page, need to properly handle the error.
          return error;
      });
      return response;
    },
    async getAll() {
      await axios.get(`https://localhost/api/users`).then(
        (res) => (this.users = res.data)
      );
    },
  },
});
