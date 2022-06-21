<script setup>
import { ref } from "vue";
import { useQuestionsStore } from "@/stores";

const age = ref(null);
const weight = ref(null);
const gender = ref("");
const wpa = ref("");
const ng = ref("");

function handleSubmit(event) {
  const questionsStore = useQuestionsStore();

  const answers = {
    age: age.value,
    weight: weight.value,
    gender: gender.value,
    wpa: wpa.value,
    ng: ng.value,
  };

  return questionsStore.upload_answers(answers).catch((err) => {
    console.log(err);
  });
}
</script>

<template>
  <div class="container sm-col-6">
    <div class="row m-3">
      <h2>Let's get started!</h2>
    </div>
    <div class="row ms-3 mb-3">
      We're going to use the following questions to help determine your
      recommended total daily caloric intake.
    </div>
    <form @submit.prevent="handleSubmit">
      <div class="form-floating mb-3 form-group">
        <input
          type="number"
          class="form-control"
          id="floatingAge"
          v-model.number="age"
        />
        <label for="floatingInput">Age</label>
      </div>
      <div class="form-floating mb-3 form-group">
        <input
          type="number"
          class="form-control"
          id="floatingWeight"
          v-model.number="weight"
        />
        <label for="floatingPassword">Weight (in kg)</label>
      </div>
      <select
        class="form-select mb-3 form-group"
        aria-label="Gender"
        v-model="gender"
      >
        <option disabled value="">Gender</option>
        <option value="1">Male</option>
        <option value="2">Female</option>
      </select>
      <select
        class="form-select mb-3 form-group"
        aria-label="Weekly Physical Activity"
        v-model="wpa"
      >
        <option disabled value="">Weekly Physical Activity</option>
        <option value="1">Light (less than twice a week)</option>
        <option value="2">Moderate (2-4 times a week)</option>
        <option value="3">Heavy (more than 3 times a week)</option>
      </select>
      <select
        class="form-select mb-3 form-group"
        aria-label="Nutritional Goal"
        v-model="ng"
      >
        <option disabled value="">Nutritional Goal</option>
        <option value="1">Weight loss</option>
        <option value="2">Weight maintenance</option>
        <option value="3">Weight gain (bulking)</option>
      </select>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<style></style>
3
