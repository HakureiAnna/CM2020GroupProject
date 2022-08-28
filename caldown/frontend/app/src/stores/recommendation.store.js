import { defineStore } from "pinia";
import axios from "axios";

import { router, error_messages } from "@/helpers";
import { useUsersStore } from "./users.store";

export const useRecommendationStore = defineStore({
    id: "plan",
    state: () => ({
        recommendations: {},
        message: {}
    }),
    actions: {
        async get_recommendations(mealType, keyword) {
            if (this.recommendations[mealType] && this.recommendations[mealType].keyword === keyword) {
                return;
            } else {
                await axios.get(`https://localhost/api/recommendations`, {params: {type: mealType, keyword: keyword}})
                            .then((res) => {
                                res.data.recipes.map(el => el.calories=parseInt(el.calories));
                                this.recommendations[mealType] = {};
                                this.recommendations[mealType].keyword = keyword;
                                this.recommendations[mealType].recipes = res.data.recipes;
                            })
                            .catch((error) => {
                                const status = error.response.status;
                                this.message.error = error_messages[status];
                            });
            }
        },

        // saves the selected recipe to the 'plan' state in users.store
        save_recommendation(mealType, recipe) {
            if (!this.recommendations[mealType]) return;
            const usersStore = useUsersStore();
            usersStore.plan[mealType] = recipe;
            router.push("/plan");

            // remove existing error message
            this.message.error = "";
        }
    }
});