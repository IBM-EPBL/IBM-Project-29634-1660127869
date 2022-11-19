import { constants } from "../../constants.js";
import { alert } from "../../utils.js";

const loginForm = document.querySelector("#login-form");
const messageBox = document.querySelector(".message-box");
const loader = document.querySelector("#loader");

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  loader.classList.remove("d-none");
  const api_body = {
    email: e.target[0].value,
    password: e.target[1].value
  }
  login(api_body);
})

const login = async (api_body) => {
  try {
    const { data } = await axios.post(
      `${constants.BASE_URL}/auth/login`,
      api_body);
    loader.classList.add("d-none");
    alert(messageBox, data.message, 'success');
    localStorage.setItem("token", data.data.jwt_token);
    window.location.href = 'index.html';
  } catch (error) {
    console.error("Login Error: ", error);
    loader.classList.add("d-none");
    alert(messageBox, error.response.data.message, 'failed');
  }
}
