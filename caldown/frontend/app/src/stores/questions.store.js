import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useQuestionsStore = defineStore({
  id: "questions",
  state: () => ({
    profile: {}
  }),
  actions: {
    async upload_profile(profile) {
      const response = await axios.post(`https://localhost/api/profile`, profile)
                                  .then(res => {
                                    console.log(res.data);
                                    router.push("/profile");
                                    return res.data;
                                  })
                                  .catch(error => {
                                    console.log(error);
                                  });
      return response;
    },
    async get_profile() {
      this.profile = await axios.get(`https://localhost/api/profile`)
                                  .then(res => {
                                    return res.data;
                                  })
                                  .catch(error => {
                                    return error;
                                  });
    }
  },
});
