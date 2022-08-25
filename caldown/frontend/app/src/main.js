import { createApp } from "vue";
import { createPinia } from "pinia";

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

import App from "./App.vue";
import { router } from "./helpers";
import { resetStore } from "./stores";
import "./axios";

const app = createApp(App);
app.component('Datepicker', Datepicker);

const pinia = createPinia();
pinia.use(resetStore);

app.use(pinia);
app.use(router);
app.mount("#app");
