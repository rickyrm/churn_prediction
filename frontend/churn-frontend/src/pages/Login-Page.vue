<template>
  <div class="login-wrapper">
    <!-- Fondo animado -->
    <div class="bg"></div>
    <div class="bg bg2"></div>
    <div class="bg bg3"></div>

    <!-- Contenedor del login -->
    <div class="container">
      <form @submit.prevent="loginUser" autocomplete="off" id="form">
        <h1 id="message">Inicio de Sesión</h1>
        <small id="smallMessage"></small>

        <div class="field">
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Usuario"
            autocomplete="off"
            required
          />
          <label for="username">Usuario</label>
        </div>

        <div class="field">
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Contraseña"
            autocomplete="new-password"
            required
          />
          <label for="password">Contraseña</label>
        </div>

        <button id="submit" type="submit">
          Acceder
        </button>

        <p>Al acceder, acepta los Términos de Servicio y la Política de Privacidad.</p>
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

    const username = ref("");
    const password = ref("");
    const loading = ref(false);

    const loginUser = async () => {
      if (!username.value || !password.value) {
        alert("Por favor, ingrese usuario y contraseña.");
        return;
      }

      loading.value = true;
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
          alert("Credenciales inválidas. Verifique su usuario y contraseña.");
        }
      } catch (err) {
        console.error("Error al iniciar sesión:", err.response?.data || err);
        const msg =
          err.response?.status === 401
            ? "Credenciales incorrectas."
            : "No se pudo conectar con el servidor.";
        alert(msg);
      } finally {
        loading.value = false;
      }
    };

    return { username, password, loginUser, loading };
  },
};
</script>

<style scoped lang="scss">
/* ----------- Fondo animado (mantiene tu estilo original) ----------- */
.bg {
  animation: slide 10s ease-in-out infinite alternate;
  background-image: linear-gradient(-60deg, rgb(192, 127, 228) 50%, rgb(243, 197, 132) 50%);
  bottom: 0;
  left: -50%;
  opacity: 0.5;
  position: fixed;
  right: -50%;
  top: 0;
  z-index: -1;
}

.bg2 {
  animation-direction: alternate-reverse;
  animation-duration: 10s;
}

.bg3 {
  animation-duration: 15s;
}

@keyframes slide {
  0% {
    transform: translateX(-25%);
  }
  100% {
    transform: translateX(25%);
  }
}

/* ----------- Estructura general ----------- */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  color: white;
  font-family: "Lato", sans-serif;
}

/* ----------- Estilos del formulario (adaptado del template CSS) ----------- */
.container {
  width: 400px;
  z-index: 1;
}

form {
  display: flex;
  flex-direction: column;
  background: transparent;
  max-width: 320px;
  padding: 2rem;
  position: relative;
  color: white;

  &::before,
  &::after {
    position: absolute;
    content: "";
    width: 100%;
    height: 100%;
    transition: all 0.5s ease;
  }

  &::before {
    z-index: -1;
    background: transparent;
    transform: translateX(-3.5rem) translateY(-3.75rem);
    border: 6px solid #570963;
  }

  &::after {
    background: #a228ee;
    z-index: -2;
    transform: translateX(-2rem) translateY(-2.25rem);
  }

  &:focus-within {
    background: #d47af8;
    &::before {
      width: 0%;
      height: 0%;
      transform: translatex(0) translatey(0);
    }
  }

  h1 {
    text-align: center;
    font-size: 1.5rem;
    margin: 0 0 0.25rem 0;
  }

  small {
    display: block;
    margin: 0 auto 1rem;
    font-size: 14px;
  }

  .field {
    display: flex;
    flex-flow: column-reverse;
    margin-bottom: 1em;
  }

  label,
  input {
    transition: all 0.3s ease;
    touch-action: manipulation;
  }

  label {
    opacity: 0;
  }

  input {
    padding: 10px 20px;
    border: 4px solid white;
    margin: 0 1.5rem;
    background-color: transparent !important;
    color: white;

    &::placeholder {
      color: white;
    }

    &:focus {
      color: #262832;
      font-weight: bold;
      outline: 0;
      border: 6px solid #34363e;
    }

    &::-webkit-input-placeholder {
      opacity: 1;
      transition: inherit;
    }

    &:focus::-webkit-input-placeholder {
      opacity: 0;
    }
  }

  button {
    border: none;
    padding: 0.85rem 1rem;
    margin-top: 2rem;
    background-color: #9003b7;
    color: white;
    font-size: 0.75rem;
    text-transform: uppercase;
    width: 65%;
    position: absolute;
    bottom: -20px;
    right: 18%;
    letter-spacing: 0.15em;
    transition: all 0.3s ease;

    &:hover {
      border: 6px solid #c7c8f2;
    }
  }

  p {
    font-size: 0.75rem;
    line-height: 1.125rem;
    margin: 0.5rem 1.5rem 1.75rem 1.5rem;
  }
}
</style>







