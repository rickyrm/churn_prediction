<template>
  <div class="login-container">
    <h2>Inicio de Sesión</h2>
    <form @submit.prevent="loginUser">
      <label>Usuario</label>
      <input v-model="username" type="text" required />

      <label>Contraseña</label>
      <input v-model="password" type="password" required />

      <button type="submit">Acceder</button>
    </form>
  </div>
</template>

<script>
import axios from "../api/axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import qs from "qs";
import { useAuthStore } from "../store/auth";

export default {
  name: "Login-Page",
  setup() {
    const router = useRouter();
    const auth = useAuthStore();

    const username = ref("admin");
    const password = ref("admin123");

    const loginUser = async () => {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/token", // URL completa
          qs.stringify({
            username: username.value,
            password: password.value
          }),
          { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );

        if (response.data && response.data.access_token) {
          console.log("Login correcto:", response.data);
          auth.setToken(response.data.access_token); // guarda token en store
          router.push("/predictions"); // redirige a Predictions
        } else {
          alert("Credenciales inválidas. Favor de verificar.");
        }
      } catch (err) {
        console.error("Error al hacer login:", err.response?.data || err);
        alert("Error de conexión o credenciales inválidas.");
      }
    };

    return { username, password, loginUser };
  },
};
</script>

<style scoped>
.login-container {
  max-width: 360px;
  margin: auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  margin-top: 80px;
  box-shadow: 0px 0px 10px #d0d0d0;
}
button {
  margin-top: 12px;
  width: 100%;
}
</style>




