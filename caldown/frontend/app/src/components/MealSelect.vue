<script setup>
import { RouterLink } from "vue-router";

import { defineProps } from "vue";
import { storeToRefs } from "pinia";

const props = defineProps({
    mealType: String
});
</script>

<template>
<div class="">
    <div class="card mb-3" style="max-width: 540px;">
        <div class="row g-0">
            <div class="col-md-4">
            <img src="..." class="img-fluid rounded-start" alt="...">
        </div>
        <div class="col-md-8 text-end">
            <div class="card-body">
                <h5 class="card-title">{{ mealType }}</h5>
                <p class="card-text">Start Here!</p>
                <RouterLink :to="{ name: 'recommendation', params: { mealType: mealType }, query: { type: mealType, keyword: mealType } }">
                    {{ mealType }} recommendation
                </RouterLink>
            </div>
        </div>
    </div>
</div>
    
</div>
</template>