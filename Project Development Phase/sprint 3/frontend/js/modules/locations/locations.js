import { constants } from "../../constants.js";
import { alert, checkForTokenExpiry } from "../../utils.js";

const locationsWrapper = document.querySelector("#locations");
const loader = document.querySelector("#loader");
const formToggleBtn = document.querySelector("#form-toggle-btn");
const addLocationForm = document.querySelector("#add-location-form");
const messageBox = document.querySelector(".message-box");

const token = localStorage.getItem("token");
const requestHeaders = {
  headers: {
    Authorization: 'Bearer ' + token
  }
};

window.addEventListener('load', () => {
  loader.classList.remove('d-none');
  getLocations();
});

formToggleBtn.addEventListener("click", () => {
  addLocationForm.classList.toggle("d-none");
});

addLocationForm.addEventListener("submit", (e) => {
  e.preventDefault();
  loader.classList.remove("d-none");
  const api_body = {
    name: e.target[0].value,
    address: e.target[1].value
  }
  addLocation(api_body);
});

const getLocations = async () => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/locations/all`,
      requestHeaders
    );
    createLocationCards(data.data);
  }
  catch (error) {
    console.error("Get Locations Error: ", error);
    checkForTokenExpiry(error.response.status);
  }
  finally {
    loader.classList.add('d-none');
  }
}

const addLocation = async (api_body) => {
  try {
    const { data } = await axios.post(
      `${constants.BASE_URL}/locations/`,
      api_body, requestHeaders);
    addLocationForm.classList.add('d-none');
    alert(messageBox, data.message, 'success');
    getLocations();
    resetLocationForm();
  }
  catch (error) {
    console.error("Add Location Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const editLocation = async (id, api_body) => {
  try {
    const { data } = await axios.put(
      `${constants.BASE_URL}/locations/${id}`,
      api_body, requestHeaders);
    alert(messageBox, data.message, 'success');
    getLocations();
  }
  catch (error) {
    console.error("Edit Location Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const deleteLocation = async (locationId) => {
  try {
    const { data } = await axios.delete(
      `${constants.BASE_URL}/locations/${locationId}`,
      requestHeaders);
    alert(messageBox, data.message, 'success');
    getLocations();
  }
  catch (error) {
    console.error("Delete Location Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const createLocationCards = (locations) => {
  locationsWrapper.innerHTML = '';
  locations.map((location) => {
    locationsWrapper.innerHTML +=
      `<div class="item location" id='card-${location.id}'>
      <div class="item-header location-header">
        <h4 class="item-name location-name">${location.name}</h4>
        <div>
          <button class="action-btn edit-btn" data-id=${location.id}>
            <i class="fas fa-pen"></i>
          </button>
          <button class="action-btn delete-btn" data-id=${location.id}>
            <i class="fas fa-trash"></i>
          </button>
          <button class="action-btn save-edit-btn d-none" data-id=${location.id}>
            <i class="fas fa-check"></i>
          </button>
        </div>
      </div>
      <p class="item-des location-add">${location.address}</p>
    </div>`;
  });

  const deleteBtns = document.querySelectorAll('.delete-btn');
  deleteBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const locationId = e.currentTarget.getAttribute('data-id');
      loader.classList.remove('d-none');
      deleteLocation(locationId)
    });
  });

  const editBtns = document.querySelectorAll('.edit-btn');
  editBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const locationId = e.currentTarget.getAttribute('data-id');
      const locationAddress = document.querySelector(`#card-${locationId} .location-add`);
      const editBtn = document.querySelector(`#card-${locationId} .edit-btn`);
      const deleteBtn = document.querySelector(`#card-${locationId} .delete-btn`);
      const saveEditBtn = document.querySelector(`#card-${locationId} .save-edit-btn`);
      locationAddress.setAttribute('contenteditable', true);
      locationAddress.focus();
      editBtn.classList.add('d-none');
      deleteBtn.classList.add('d-none');
      saveEditBtn.classList.remove('d-none');
      saveEditBtn.addEventListener('click', () => {
        loader.classList.remove('d-none');
        editLocation(locationId, {
          address: locationAddress.textContent
        })
      })
    })
  })
}

const resetLocationForm = () => {
  const formInputs = document.querySelectorAll('input');
  formInputs.forEach((input) => {
    input.value = '';
  })
}