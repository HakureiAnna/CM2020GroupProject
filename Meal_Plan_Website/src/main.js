import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import { router } from "./helpers";
import "./axios";

// Set up testing backend
import { fakeBackend } from "./helpers";
fakeBackend();

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);

app.use(router);

app.mount("#app");
