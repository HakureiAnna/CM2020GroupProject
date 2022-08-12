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
    <form @submit.prevent="handleSubmit">
      <div class="questions form-floating mb-3 form-group">
        <input
          type="number"
          class="form-control"
          id="floatingAge"
          v-model.number="age"
        />
        <label for="floatingInput">Age</label>
      </div>
      <div class="questions form-floating mb-3 form-group">
        <input
          type="number"
          class="form-control"
          id="floatingWeight"
          v-model.number="weight"
        />
        <label for="floatingPassword">Weight (in kg)</label>
      </div>

      <select
        class="questions form-select mb-3 form-group"
        aria-label="Gender"
        v-model="gender"
      >
        <option disabled value="">Gender</option>
        <option value="1">Male</option>
        <option value="2">Female</option>
      </select>
      <select
        class="questions form-select mb-3 form-group"
        aria-label="Weekly Physical Activity"
        v-model="wpa"
      >
        <option disabled value="">Weekly Physical Activity</option>
        <option value="1">Light (less than twice a week)</option>
        <option value="2">Moderate (2-4 times a week)</option>
        <option value="3">Heavy (more than 3 times a week)</option>
      </select>
      <select
        class="questions form-select mb-3 form-group"
        aria-label="Nutritional Goal"
        v-model="ng"
      >
        <option disabled value="">Nutritional Goal</option>
        <option value="1">Weight loss</option>
        <option value="2">Weight maintenance</option>
        <option value="3">Weight gain (bulking)</option>
      </select>
      <button type="submit" class="questions btn btn-primary">Submit</button>
    </form>
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
