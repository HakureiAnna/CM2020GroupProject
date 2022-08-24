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

function show(){
  document.getElementById('getStarted').style.cssText = "display: none";
  // document.getElementById('form-age').style.cssText = "display: block";
  // document.getElementById('form-weight').style.cssText = "display: block";
  let questions = document.getElementsByClassName('questions');
  for(var i=0; i<questions.length; i++){
    questions[i].style.cssText = "display: block";
  }
}

</script>

<template>
  <div class="container sm-col-6">
    <div class="title row m-3">
      <h2>Let's get started!</h2>
    </div>
    <div class="welcome row m-3">
      <p>We're going to use the following questions to help determine your
      recommended total daily caloric intake.</p>
      <button @click = "show" type="submit" id = "getStarted" class="btn btn-primary">Let's Go!</button>
    </div>
    <form @submit="onSubmit">
      <select
        class="questions form-select"
        aria-label="Gender"
        v-model="genders" >
        <option v-for="gender in genders_options" :value="gender.value">{{gender.text}}</option>
      </select>
      <div class=" questions form-floating mb-3 form-group">
        <input 
          name="age" 
          v-model="age" 
          type="number" 
          class="form-control" 
          id="floatingAge" 
          placeholder="Enter Your Age" />
        <label for="floatingInput">Age</label>
        <span>{{ errors.age }}</span>
      </div>
      <div class="questions form-floating mb-3 form-group">
        <input 
          name="weight" 
          v-model="weight" 
          type="number" 
          class="form-control" 
          id="floatingWeight" 
          placeholder="Enter Your Weight" />
        <label for="floatingPassword">Weight (in kg)</label>
        <span>{{ errors.weight }}</span>
      </div>
      <div class="questions form-floating mb-3 form-group">
        <input 
          name="height" 
          v-model="height" 
          type="number" 
          class="form-control" 
          id="floatingHeight" 
          placeholder="Enter Your Height" />
        <label for="floatingPassword">Height (in cm)</label>
        <span>{{ errors.height }}</span>
      </div>
      <select
        class="questions form-select"
        aria-label="Goal"
        v-model="goals"
      >
        <option v-for="goal in goals_options" :value="goal.value">{{goal.text}}</option>
      </select>
      <button type="submit" class="questions btn btn-primary">Submit</button>
    </form>

    <div v-if="message.error">{{ message.error }}</div>
  </div>
</template>


<style>
.btn {
  background-color: #e68a35;
}

.btn:hover{
  background-color: #e68a35; 
}

.title{
  height: 8vh;
  position: relative;
}
.title h2{
  justify-content: center;
  display: flex;
  align-items: center;
}

.welcome{
  padding: none;
  position: relative;
  justify-content: center
}
.welcome p{
  text-align: center;
}

.questions{
  display: none;
}

</style>