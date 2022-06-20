import { defineStore } from "pinia";

import { router } from "@/helpers";

const baseUrl = `${import.meta.env.VITE_API_URL}/questions`;

export const useQuestionsStore = defineStore({
  id: "questions",
  state: () => {},
  actions: {
    async upload_answers(answers) {
      console.log(answers);

      router.push("/");
    },
  },
});
