<script setup>
import { ref, computed } from "vue";
import { useForm } from "vee-validate";
import * as Yup from "yup";

import { useQuestionsStore } from "@/stores";

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
})

const genders = ref("gender");
const genders_options = ref([
  { text: "Male", value: "male" },
  { text: "Female", value: "female" }
])

const { meta, errors, useFieldModel, handleSubmit, isSubmitting } = useForm({
  validationSchema: schema,
});

const [age, weight, height] = useFieldModel(["age", "weight", "height"]);

const questionsStore = useQuestionsStore();

const onSubmit = handleSubmit(async values => {
  const profile = {
    age: age.value,
    weight: weight.value,
    height: height.value,
    gender: genders.value === "male" ? 0 : 1
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
      <!-- <div class="form-floating mb-3 form-group">
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
      </select> -->
      <button :disabled="isSubmitting" type="submit" class="btn btn-primary">Save</button>
    </form>
  </div>
</template>

<style></style>
3
