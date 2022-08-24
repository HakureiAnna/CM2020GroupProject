import { defineStore } from "pinia";
import axios from "axios";

import { router } from "@/helpers";

export const usePlanMealStore = defineStore({
    id: "plan",
    state: () => ({
        plans: [],
        plan: {},
        recommendations: []
    }),
    actions: {
        async get_plan(planId) {
        },

        async post_plan() {
        },

        async get_recommendations(mealType, keyword) {
            const response = await axios.get(`https://localhost/api/recommendations`, {params: {type: mealType, keyword: mealType}})
                                    .then(res => {
                                        console.log(res);
                                        this.recommendations = res.data;
                                    })
                                    .catch(error => {
                                        console.log(error);
                                    })
        }
    }
});