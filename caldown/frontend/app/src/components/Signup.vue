<script setup>
import { ref, computed } from "vue";
import { useForm } from "vee-validate";
import * as Yup from "yup";
import { storeToRefs } from "pinia";

import { useAuthStore, useUsersStore } from "@/stores";

const schema = Yup.object().shape({
  username: Yup.string()
            .min(8, "Username Must be at least 8 characters and Start with a letter")
            .required("username is required")
            .label("Your User Name"),
  password: Yup.string()
            .min(12, "Password must be at least 12 characters")
            .matches(/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{12,}$/, "Password Must contain at least 1 letter, 1 digit, and 1 special character")
            .required("Password is required")
            .label("Your Password"),
  confirmPassword: Yup.string()
            .oneOf([Yup.ref("password"), null], "Password Must Match")
            .required("Confirm Password is required")
            .label("Confirm Password")
})


const { meta, errors, useFieldModel, handleSubmit, isSubmitting, resetForm, } = useForm({
  validationSchema: schema,
});

const [username, password, confirmPassword] = useFieldModel(["username", "password", "confirmPassword"]);

const authStore = useAuthStore();
const usersStore = useUsersStore();
const { message } = storeToRefs(usersStore);

const onSubmit = handleSubmit( async values => {
  const response = await usersStore.signUp(username.value, password.value, confirmPassword.value);

  // hydrate authetication store
  authStore.$reset();
});
</script>

<template>
  <div class="signup_wrapper">
    <div class="logo">
      <img src="./icons/logoidea2.png" alt="" />
    </div>
    <div class="container">
        <form @submit="onSubmit">
          <div class="form-group input-field">
            <i class="fa fa-user" aria-hidden="true"></i>
            <input name="username" v-model="username" type="text" class="form-control" />
            <span>{{ errors.username }}</span>
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <input name="password" v-model="password" type="password" class="form-control" />
            <span>{{ errors.password }}</span>
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <input name="confirmPassword" v-model="confirmPassword" type="password" class="form-control" />
            <span>{{ errors.confirmPassword }}</span>
          </div>
          <button class="btn solid">Sign Up</button>
          <button @click="resetForm()" type="reset" class="btn btn-secondary">Reset</button>
          <button class="btn clear" @click = "$router.push('login')">Login
          </button>
        </form>

        <!-- Hello Calvin/Lat
        I have moved error message to message.response, just to make it easier to access in Vue.
        All text messages are in the 'message' object, 'error' field
        -->
        <div v-if="message.error">{{ message.error }}</div>
      </div>
    </div>
</template>

<style></style>
