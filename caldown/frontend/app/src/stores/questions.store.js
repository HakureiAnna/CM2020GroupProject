import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const useQuestionsStore = defineStore({
  id: "questions",
  state: () => ({
    profile: {},
    message: {}
  }),
  actions: {
    async upload_profile(profile) {
      const response = await axios.post(`https://localhost/api/profile`, profile)
                                  .then(res => {
                                    router.push("/profile");
                                    return res.data;
                                  })
                                  .catch(error => {
                                    let status = error.response.status;
                                    let error_message = {
                                      400: "invalid data/data types",
                                      401: "Unauthorized Access",
                                      405: "Unknown Error, Please contact customer support",
                                      500: "Server Error"
                                    };
                                    this.message.error = error_message[status];
                                  });
      this.message.response = response;
      return response;
    },
    async get_profile() {
      await axios.get(`https://localhost/api/profile`)
                  .then(res => {
                    this.profile = res.data;
                  })
                  .catch(error => {
                    let status = error.response.status;
                    let error_message = {
                      400: "invalid data/data types",
                      401: "Unauthorized Access",
                      405: "Unknown Error, Please contact customer support",
                      500: "Server Error"
                    };
                    this.message.error = error_message[status];
                  });
    }
  },
});
