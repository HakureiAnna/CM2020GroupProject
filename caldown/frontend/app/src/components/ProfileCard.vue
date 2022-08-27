<script setup>
import { onMounted } from "vue";
import { storeToRefs } from "pinia";

import { useUsersStore } from "@/stores";

const usersStore = useUsersStore();
const { profile, message } = storeToRefs(usersStore);

onMounted(() => {
  usersStore.get_profile();
});

</script>

<template>
<div class="profile-card container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-lg-6 mb-4 mb-lg-0">
        <div class="card mb-3" style="border-radius: .5rem;">
          <div class="row g-0">
            <div class="col-md-4 gradient-custom text-center text-white"
              style="border-top-left-radius: .5rem; border-bottom-left-radius: .5rem;">
              <img src="../public/img/profile.jpg"
                alt="Avatar" class="img-fluid my-5" />
            </div>
            <div v-if="!message.error" class="col-md-8">
              <div class="card-body p-4">
                <h6>Information</h6>
                <hr class="mt-0 mb-4">
                <div class="row pt-1">
                  <div class="col-6 mb-3">
                    <h6>Age</h6>
                    <p class="text-muted">{{ profile.age }}</p>
                  </div>
                  <div class="col-6 mb-3">
                    <h6>Gender</h6>
                    <p class="text-muted">{{ profile.gender }}</p>
                  </div>
                  <div class="col-6 mb-3">
                    <h6>Height</h6>
                    <p class="text-muted">{{ profile.height }}</p>
                  </div>
                  <div class="col-6 mb-3">
                    <h6>Weight</h6>
                    <p class="text-muted">{{ profile.weight }}</p>
                  </div>
                </div>
                <h6>Goals</h6>
                <hr class="mt-0 mb-4">
                <div class="row pt-1">
                  <div class="col-12 mb-3">
                    <h6>Goal</h6>
                    <p class="text-muted">{{ profile.goal }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="message.error" class="col-md-8">
              <div class="card-body p-4">
                <h6>Information</h6>
                <hr class="mt-0 mb-4">
                <div class="row pt-1">
                  <div class="col-12 mb-3">
                    <h6>Error</h6>
                    <p class="text-muted">{{ message.error }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
</template>

<style>
.profile-card img {
  margin: 0;
}
</style>