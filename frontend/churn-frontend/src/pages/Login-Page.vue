<template>
  <div class="login-wrapper">
    <div class="login-container">
      <h2>Inicio de Sesión</h2>

      <form @submit.prevent="loginUser">
        <div class="form-group">
          <label for="username">Usuario</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Ingrese su usuario"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Ingrese su contraseña"
            required
          />
        </div>

        <button type="submit" class="btn-primary">Acceder</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "../api/axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import qs from "qs";
import { useAuthStore } from "../store/auth";

export default {
  name: "LoginPage",
  setup() {
    const router = useRouter();
    const auth = useAuthStore();

    const username = ref("admin");
    const password = ref("admin123");

    const loginUser = async () => {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/token",
          qs.stringify({
            username: username.value,
            password: password.value,
          }),
          { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );

        if (response.data?.access_token) {
          auth.setToken(response.data.access_token);
          router.push("/predictions");
        } else {
          alert("Credenciales inválidas. Favor de verificar.");
        }
      } catch (err) {
        console.error("Error al iniciar sesión:", err.response?.data || err);
        alert("Error de conexión o credenciales inválidas.");
      }
    };

    return { username, password, loginUser };
  },
};
</script>

<style scoped>
/* Fondo general */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
}

/* Contenedor principal */
.login-container {
  background: #ffffff;
  padding: 40px 35px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.4s ease-out;
}

/* Título */
.login-container h2 {
  text-align: center;
  color: #34495e;
  margin-bottom: 30px;
  font-weight: 700;
}

/* Campos del formulario */
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 18px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 6px;
}

input {
  padding: 10px 12px;
  border: 1px solid #ccd1d9;
  border-radius: 6px;
  transition: all 0.2s ease;
}

input:focus {
  border-color: #3498db;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.4);
  outline: none;
}

/* Botón principal */
.btn-primary {
  background: #3498db;
  color: #fff;
  border: none;
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-primary:hover {
  background: #2980b9;
}

/* Animación de entrada */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>





