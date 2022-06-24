import { defineStore } from "pinia";

import { fetchWrapper } from "@/helpers";
import axios from "axios";

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

export const useUsersStore = defineStore({
  id: "users",
  state: () => ({
    users: {},
  }),
  actions: {
    async getAll() {
      await axios.get(`https://localhost/api/users`).then(
        (res) => (this.users = res.data)
      );
      // this.users = { loading: true };
      // fetchWrapper
      //   .get(baseUrl)
      //   .then((users) => (this.users = users))
      //   .catch((error) => (this.users = { error }));
    },
  },
});
