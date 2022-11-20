import { constants } from "../../constants.js"
import { alert } from "../../utils.js";

const registerForm = document.querySelector('#register-form');
const messageBox = document.querySelector(".message-box");
const loader = document.querySelector("#loader");

registerForm.addEventListener("submit", (e) => {
  e.preventDefault()
  const api_body = {
    name: e.target[0].value,
    email: e.target[1].value,
    password: e.target[2].value,
    repeat_password: e.target[3].value,
    address: e.target[4].value,
  }
  loader.classList.remove("d-none");
  registerAcc(api_body);
})

const registerAcc = async (api_body) => {
  try {
    const { data } = await axios.post(
      `${constants.BASE_URL}/auth/register`,
      api_body);
    loader.classList.add("d-none");
    alert(messageBox, data.message, 'success');
  }
  catch (error) {
    console.error("Account registration Error: ", error);
    loader.classList.add("d-none");
    alert(messageBox, JSON.stringify(error.response.data.data), 'failed');
  }
}