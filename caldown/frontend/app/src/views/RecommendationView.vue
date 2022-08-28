<script setup>
import { defineProps, ref } from "vue";
import { router } from "@/helpers";

import { useRecommendationStore } from "@/stores";
import { storeToRefs } from "pinia";

import RecipeCard from "@/components/RecipeCard.vue";

const props = defineProps({
    mealType: String
});

const picked_recipe = ref(0);

const recommendationStore = useRecommendationStore();
const { recommendations, message } = storeToRefs(recommendationStore);

// Bad! Short for MealType
const mt = router.currentRoute.value.params.mealType;
recommendationStore.get_recommendations(mt, mt);

const submit = () => {
    recommendationStore.save_recommendation(mt, picked_recipe);
}

</script>

<template>
<div class="container">
    <div class="row row-cols-1">
        <div class="col">
            <h2 v-if="recommendations[mealType]" class="meal-type">{{ recommendations[mealType].keyword }}</h2>
            <button @click="submit" type="submit" class="btn btn-primary">Save</button>
            <div v-if="message.error">{{ message.error }}</div>
        </div>
    </div>
    <div v-if="recommendations[mealType]" class="row row-cols-1 row-cols-lg-4 row-cols-md-2 g-4">
        <div class="col" v-for="recipe in recommendations[mealType].recipes">
            <div class="form-check">
                <input v-model="picked_recipe" class="form-check-input" type="radio" id="recipe" :name="recipe.name" :value="recipe">
                <label class="form-check-label" for="recipe">
                    Click Me
                </label>
            </div>
            <RecipeCard :picture_src="recipe.image"
                        :name="recipe.name"
                        :calories="recipe.calories"  />
        </div>
    </div>
</div>
</template>