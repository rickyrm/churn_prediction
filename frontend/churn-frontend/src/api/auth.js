import api from "./axios";

export const login = async (username, password) => {
  const form = new FormData();
  form.append("username", username);
  form.append("password", password);

  const res = await api.post("/auth/login/", form);
  return res.data;
};
