import { defineStore } from "pinia";
import axios from "axios";

import { router, validatePlan, error_messages } from "@/helpers";

/* 
User related information

> profile
> plan
> history / past meal plans

*/
export const useUsersStore = defineStore({
  id: "users",
  state: () => ({
    profile: {},
    plan: {},
    history: [],
    message: {}
  }),
  actions: {
    async get_profile() {
      await axios.get(`https://localhost/api/profile`)
                  .then((res) => {
                    this.profile = res.data;
                  })
                  .catch((error) => {
                    const status = error.response.status;
                    this.$patch({
                      message: {
                        error: error_messages[status]
                      }
                    });
                  });
    },

    async upload_profile(profile) {
      await axios.post(`https://localhost/api/profile`, profile)
                  .then((res) => {
                    this.message = {};
                    router.push("/profile");
                  })
                  .catch((error) => {
                    let status = error.response.status;
                    this.message.error = error_messages[status]
                  });
    },

    async get_plan(planId) {
      await axios.get(`https://localhost/api/plan`, {params: {planId: planId}})
                  .then((res) => {
                    this.history[planId] = res.data;
                  })
                  .catch((error) => {
                    console.log(error);
                  })
    },

    async post_plan(date) {
        if (validatePlan(this.plan)) {
            const data = {
                breakfast: this.plan["Breakfast"],
                lunch: this.plan["Lunch"],
                dinner: this.plan["Dinner"],
                plannedDate: date
            }
            await axios.post(`https://localhost/api/plan`, data)
                        .then((res) => {
                            console.log(res);
                        })
                        .catch((error) => {
                            let status = error.response.status;
                            this.message = error_messages[status];
                        })
        } else {
            this.message = "Please Fill Your Plan Before Submit"
        }
    },

    async get_history(startDate, endDate) {
      await axios.get(`https://localhost/api/history`, {params: {startDate: startDate, endDate: endDate}})
                  .then((res) => {
                    this.history = res.data.plans;
                  })
                  .catch((error) => {
                    console.log(error);
                  })
    },
  },
});
