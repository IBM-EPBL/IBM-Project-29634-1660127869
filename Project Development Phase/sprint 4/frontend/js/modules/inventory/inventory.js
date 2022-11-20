import { constants } from "../../constants.js";
import { alert, checkForTokenExpiry } from "../../utils.js";


const loader = document.querySelector("#loader");
const inventoriesWrapper = document.querySelector("#inventories");
const formToggleBtn = document.querySelector("#form-toggle-btn");
const addInventoryForm = document.querySelector("#add-inventory-form");
const messageBox = document.querySelector(".message-box");
const productNameInput = document.querySelector('#product-name');
const locationNameInput = document.querySelector('#location-name');
const token = localStorage.getItem("token");
const requestHeaders = {
  headers: {
    Authorization: 'Bearer ' + token
  }
};

window.addEventListener('load', () => {
  loader.classList.remove('d-none');
  getProducts();
  getLocations();
  getInventory();
});

formToggleBtn.addEventListener("click", () => {
  addInventoryForm.classList.toggle("d-none");
});

addInventoryForm.addEventListener("submit", (e) => {
  e.preventDefault();
  loader.classList.remove("d-none");
  const api_body = {
    product_name: e.target[0].value,
    location_name: e.target[1].value,
    quantity: e.target[2].value,
    threshold: e.target[3].value
  }
  addInventory(api_body);
});

const getInventory = async () => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/inventory/all`,
      requestHeaders
    );
    createInventoryCards(data.data);
  }
  catch (error) {
    console.error("Get Inventory Error: ", error);
    checkForTokenExpiry(error.response.status);
  }
  finally {
    loader.classList.add('d-none');
  }
}

const addInventory = async (api_body) => {
  try {
    const { data } = await axios.post(
      `${constants.BASE_URL}/inventory/`,
      api_body, requestHeaders);
    addInventoryForm.classList.add('d-none');
    alert(messageBox, data.message, 'success');
    getInventory();
    resetInventoryForm();
  }
  catch (error) {
    console.error("Add Product Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const editInventory = async (id, api_body) => {
  try {
    const { data } = await axios.put(
      `${constants.BASE_URL}/inventory/${id}`,
      api_body, requestHeaders);
    alert(messageBox, data.message, 'success');
    getInventory();
  }
  catch (error) {
    console.error("Edit Inventory Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const deleteInventory = async (inventoryId) => {
  try {
    const { data } = await axios.delete(
      `${constants.BASE_URL}/inventory/${inventoryId}`,
      requestHeaders);
    alert(messageBox, data.message, 'success');
    getInventory();
  }
  catch (error) {
    console.error("Delete Inventory Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const getProducts = async () => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/products/all`,
      requestHeaders
    );
    createFormOptions(productNameInput, data.data);
  }
  catch (error) {
    console.error("Get Products Error: ", error);
  }
}


const getLocations = async () => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/locations/all`,
      requestHeaders
    );
    createFormOptions(locationNameInput, data.data)
  }
  catch (error) {
    console.error("Get Locations Error: ", error);
  }
}

const createInventoryCards = (inventories) => {
  inventoriesWrapper.innerHTML = '';
  inventories.map((inventory) => {
    inventoriesWrapper.innerHTML +=
      `<div class="item inventory" id='card-${inventory.id}'>
        <div class="item-header inventory-header">
          <h4 class="item-name inventory-product">${inventory.product.name}</h4>
          <div>
            <button class="action-btn edit-btn" data-id=${inventory.id}>
              <i class="fas fa-pen"></i>
            </button>
            <button class="action-btn delete-btn" data-id=${inventory.id}>
              <i class="fas fa-trash"></i>
            </button>
            <button class="action-btn save-edit-btn d-none" data-id=${inventory.id}>
              <i class="fas fa-check"></i>
            </button>
          </div>
        </div>
        <p class="item-des">Location: <span class='inventory-location'>${inventory.location.name}</span></p>
        <p class="item-des pt-0">Quantity: <span class='inventory-quantity'>${inventory.quantity}</span></p>
        <p class="item-des pt-0">Threshold: <span class='inventory-threshold'>${inventory.threshold}</span></p>
      </div>`;
  });

  const deleteBtns = document.querySelectorAll('.delete-btn');
  deleteBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const inventoryId = e.currentTarget.getAttribute('data-id');
      loader.classList.remove('d-none');
      deleteInventory(inventoryId)
    });
  });

  const editBtns = document.querySelectorAll('.edit-btn');
  editBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const inventoryId = e.currentTarget.getAttribute('data-id');
      const inventoryQuantity = document.querySelector(`#card-${inventoryId} .inventory-quantity`);
      const inventoryThreshold = document.querySelector(`#card-${inventoryId} .inventory-threshold`);
      const editBtn = document.querySelector(`#card-${inventoryId} .edit-btn`);
      const deleteBtn = document.querySelector(`#card-${inventoryId} .delete-btn`);
      const saveEditBtn = document.querySelector(`#card-${inventoryId} .save-edit-btn`);
      inventoryQuantity.setAttribute('contenteditable', true);
      inventoryThreshold.setAttribute('contenteditable', true);
      inventoryQuantity.focus();
      editBtn.classList.add('d-none');
      deleteBtn.classList.add('d-none');
      saveEditBtn.classList.remove('d-none');
      saveEditBtn.addEventListener('click', () => {
        loader.classList.remove('d-none');
        editInventory(inventoryId, {
          quantity: inventoryQuantity.textContent,
          threshold: inventoryThreshold.textContent,
        })
      })
    })
  })
}

const createFormOptions = (element, data) => {
  data.map((d) => {
    element.innerHTML +=
      `<option value=${d.name}>${d.name}</option>`
  })
}
const resetInventoryForm = () => {
  const formInputs = document.querySelectorAll('.app-input');
  formInputs.forEach((input) => {
    input.value = '';
  })
}