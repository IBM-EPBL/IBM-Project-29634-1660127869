import { constants } from "./constants.js";
import { alert } from "./utils.js";

const loader = document.querySelector("#loader");
const purchaseForm = document.querySelector("#purchase-form");
const messageBox = document.querySelector(".message-box");

const retailerNameInput = document.querySelector("#retailer-name");
const locationInput = document.querySelector("#location-name");
const productInput = document.querySelector("#product-name");

window.addEventListener('load', () => {
  loader.classList.remove('d-none');
  getAllRetailers();
});

purchaseForm.addEventListener("submit", (e) => {
  e.preventDefault();
  loader.classList.remove("d-none");
  const api_body = {
    location_name: e.target[1].value,
    product_name: e.target[2].value,
    quantity: e.target[3].value
  }
  const retailerId = retailerNameInput.options[retailerNameInput.selectedIndex].getAttribute('data-id')
  purchaseProduct(api_body, retailerId);
});


const purchaseProduct = async (api_body, retailerId) => {
  try {
    const { data } = await axios.post(
      `${constants.BASE_URL}/marketplace/order/${retailerId}`,
      api_body);
    alert(messageBox, data.message, 'success');
  }
  catch (error) {
    console.error("Purchase Product Error: ", error);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const getAllRetailers = async () => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/marketplace/retailers`,
    );
    createFormOptions(retailerNameInput, data.data);
  }
  catch (error) {
    console.error("Get All Retailers Error: ", error);
  }
  finally {
    loader.classList.add('d-none');
  }
}

const getLocationsByRetailer = async (retailerId) => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/marketplace/locations/${retailerId}`,
    );
    createFormOptions(locationInput, data.data);
  }
  catch (error) {
    console.error("Get Locations By Retailer Error: ", error);
  }
  finally {
    loader.classList.add('d-none');
  }
}


const getAllProductsByLocation = async (locationId) => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/marketplace/products/${locationId}`,
    );
    createFormOptions(productInput, data.data);
  }
  catch (error) {
    console.error("Get All Products By Location Error: ", error);
  }
  finally {
    loader.classList.add('d-none');
  }
}

const createFormOptions = (element, data) => {
  const option = element.options[0]
  element.innerHTML = '';
  element.appendChild(option);
  element.options.selectedIndex = 0
  data.map((d) => {
    element.innerHTML +=
      `<option value=${d.name} data-id=${d.id}>${d.name}</option>`
  })
}

retailerNameInput.addEventListener('change', () => {
  loader.classList.remove('d-none');
  const selectedOption = retailerNameInput.options[retailerNameInput.selectedIndex];
  getLocationsByRetailer(selectedOption.getAttribute('data-id'));
  createFormOptions(productInput, '')
});


locationInput.addEventListener('change', () => {
  loader.classList.remove('d-none');
  const selectedOption = locationInput.options[locationInput.selectedIndex];
  getAllProductsByLocation(selectedOption.getAttribute('data-id'));
}); 
