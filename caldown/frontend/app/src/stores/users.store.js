import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

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
      await axios.post(`https://localhost/api/signup`, { user:username, pass:password }).then(
          (res) => {
            router.push("/login");
          }
        ).catch(error => {
        console.log(`from stores ${error}`);
      });
    },
    async getAll() {
      await axios.get(`https://localhost/api/users`).then(
        (res) => (this.users = res.data)
      );
    },
  },
});
