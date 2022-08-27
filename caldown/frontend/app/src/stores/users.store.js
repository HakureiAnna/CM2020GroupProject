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
    },

    async post_plan() {
        if (validatePlan(this.plan)) {
            const data = {
                breakfast: this.plan["Breakfast"],
                lunch: this.plan["Lunch"],
                dinner: this.plan["Dinner"],
                plannedDate: this.plan["plannedDate"]
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
    },
  },
});
