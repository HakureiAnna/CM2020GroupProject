import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

const error_message = {
    400: "invalid data/data types",
    401: "Unauthorized Access",
    405: "Unknown Error, Please contact customer support",
    500: "Server Error"
};

const validatePlan = (plan) => {
    return plan["Breakfast"] && plan["Lunch"] && plan["Dinner"]
}

export const usePlanMealStore = defineStore({
    id: "plan",
    state: () => ({
        plans: [],
        plan: {},
        profiles: [],
        message: {}
    }),
    actions: {
        async get_plan(planId) {
        },

        async post_plan(date) {
            if (validatePlan(this.plan)) {
                const data = {
                    breakfast: this.plan["Breakfast"].recipe,
                    lunch: this.plan["Lunch"].recipe,
                    dinner: this.plan["Dinner"].recipe,
                    plannedDate: date
                }
                console.log(data);
                await axios.post(`https://localhost/api/plan`, data)
                            .then((res) => {
                                console.log(res);

                                // reset current plan
                                // this.plan = {};
                            })
                            .catch((error) => {
                                let status = error.response.status;
                                this.message.error = error_message[status];
                            })
            } else {
                this.message.error = "Please Fill Your Plan Before Submit";
                return;
            }
        },

        async get_history(startDate, endDate) {
        },

        async get_recommendations(mealType, keyword) {
            if (this.plan[mealType] && this.plan[mealType].keyword === keyword) {
                return;
            } else {
                await axios.get(`https://localhost/api/recommendations`, {params: {type: mealType, keyword: keyword}})
                            .then((res) => {
                                res.data.recipes.map(el => el.calories=parseInt(el.calories));
                                this.plan[mealType] = {};
                                this.plan[mealType].keyword = keyword;
                                this.plan[mealType].recipes = res.data.recipes;
                            })
                            .catch((error) => {
                                let status = error.response.status;
                                this.message.error = error_message[status];
                            });
            }
        },

        // saves the user selected recipe to the current 'plan'
        save_recommendation(mealType, recipe) {
            if (!this.plan[mealType]) return;
            this.plan[mealType].recipe = recipe;
            router.push("/plan");

            // remove existing error message
            this.message.error = "";
        }
    }
});