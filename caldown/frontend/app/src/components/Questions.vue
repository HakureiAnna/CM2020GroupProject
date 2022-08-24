<script setup>
import { ref } from "vue";
import { useForm } from "vee-validate";
import * as Yup from "yup";

import { useQuestionsStore } from "@/stores";
import { storeToRefs } from "pinia";

const schema = Yup.object().shape({
  age: Yup.number()
          .typeError("Please enter an integer")
          .min(16, "Must be older than 16")
          .required("Age is required")
          .max(110, "Must be a valid age")
          .label("age"),
  weight: Yup.number()
             .typeError("Please enter a number")
             .min(40, "Must be more than 40")
             .required("Weight is required"),
  height: Yup.number()
             .typeError("Please enter a number")
             .min(120, "Must be more than 120")
             .required("Height is required"),
});

const genders = ref(0);
const genders_options = ref([
  { text: "Male", value: "male" },
  { text: "Female", value: "female" }
]);

const goals = ref(1);
const goals_options = ref([
  { text: "Balanced", value: "balanced" },
  { text: "High-Fiber", value: "high_fiber" },
  { text: "High-Protein", value: "high_protein" },
  { text: "Low-Carbon", value: "low_carbon" },
  { text: "Low-Fat", value: "low_fat" },
  { text: "Low-Sodium", value: "low_sodium" },
]);

const { meta, errors, useFieldModel, handleSubmit, isSubmitting } = useForm({
  validationSchema: schema,
});

const [age, weight, height] = useFieldModel(["age", "weight", "height"]);

const questionsStore = useQuestionsStore();
const { message } = storeToRefs(questionsStore);

const onSubmit = handleSubmit(async values => {
  const profile = {
    age: age.value,
    weight: weight.value,
    height: height.value,
    gender: genders.value,
    goal: goals.value
  }
  const response = await questionsStore.upload_profile(profile);
});
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
    <form @submit="onSubmit">
      <select
        class="form-select"
        aria-label="Gender"
        v-model="genders"
      >
        <option v-for="gender in genders_options" :value="gender.value">{{gender.text}}</option>
      </select>
      <div class="form-group">
        <input name="age" v-model="age" type="number" class="form-control" placeholder="Enter Your Age" />
        <span>{{ errors.age }}</span>
      </div>
      <div class="form-group">
        <input name="weight" v-model="weight" type="number" class="form-control" placeholder="Enter Your Weight" />
        <span>{{ errors.weight }}</span>
      </div>
      <div class="form-group">
        <input name="height" v-model="height" type="number" class="form-control" placeholder="Enter Your Height" />
        <span>{{ errors.height }}</span>
      </div>
      <select
        class="form-select"
        aria-label="Goal"
        v-model="goals"
      >
        <option v-for="goal in goals_options" :value="goal.value">{{goal.text}}</option>
      </select>
      <button :disabled="isSubmitting" type="submit" class="btn btn-primary">Save</button>
    </form>

    <div v-if="message.error">{{ message.error }}</div>
  </div>
</template>

<style></style>
3
