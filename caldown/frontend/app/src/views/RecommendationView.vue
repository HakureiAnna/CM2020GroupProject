<script setup>
import { defineProps, ref, onMounted } from "vue";
import { storeToRefs } from "pinia";

import { usePlanMealStore } from "@/stores";
import { router } from "@/helpers";

const props = defineProps({
    mealType: String
});

const planMealStore = usePlanMealStore();
const { plan } = storeToRefs(planMealStore);

// Bad! Short for MealType
let mt = router.currentRoute.value.params.mealType;
const response = planMealStore.get_recommendations(mt, mt);

</script>

<template>
<div class="container">
    
</div>
</template>