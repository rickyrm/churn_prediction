import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || "");

  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem("token", newToken);
  }

  function logout() {
    token.value = "";
    localStorage.removeItem("token");
  }

  return { token, setToken, logout };
});

