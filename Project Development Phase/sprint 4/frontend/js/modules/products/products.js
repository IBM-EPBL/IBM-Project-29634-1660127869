import { constants } from "../../constants.js";
import { alert, checkForTokenExpiry } from "../../utils.js";

const productsWrapper = document.querySelector("#products");
const loader = document.querySelector("#loader");
const formToggleBtn = document.querySelector("#form-toggle-btn");
const addProductForm = document.querySelector("#add-product-form");
const messageBox = document.querySelector(".message-box");

const token = localStorage.getItem("token");
const requestHeaders = {
  headers: {
    Authorization: 'Bearer ' + token
  }
};

window.addEventListener('load', () => {
  loader.classList.remove('d-none');
  getProducts();
});

formToggleBtn.addEventListener("click", () => {
  addProductForm.classList.toggle("d-none");
});

addProductForm.addEventListener("submit", (e) => {
  e.preventDefault();
  loader.classList.remove("d-none");
  const api_body = {
    name: e.target[0].value,
    description: e.target[1].value
  }
  addProduct(api_body);
});

const getProducts = async () => {
  try {
    const { data } = await axios.get(
      `${constants.BASE_URL}/products/all`,
      requestHeaders
    );
    createProductCards(data.data);
  }
  catch (error) {
    console.error("Get Products Error: ", error);
    checkForTokenExpiry(error.response.status);
  }
  finally {
    loader.classList.add('d-none');
  }
}

const addProduct = async (api_body) => {
  try {
    const { data } = await axios.post(
      `${constants.BASE_URL}/products/`,
      api_body, requestHeaders);
    addProductForm.classList.add('d-none');
    alert(messageBox, data.message, 'success');
    getProducts();
    resetProductForm();
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

const editProduct = async (id, api_body) => {
  try {
    const { data } = await axios.put(
      `${constants.BASE_URL}/products/${id}`,
      api_body, requestHeaders);
    alert(messageBox, data.message, 'success');
    getProducts();
  }
  catch (error) {
    console.error("Edit Product Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const deleteProduct = async (productId) => {
  try {
    const { data } = await axios.delete(
      `${constants.BASE_URL}/products/${productId}`,
      requestHeaders);
    alert(messageBox, data.message, 'success');
    getProducts();
  }
  catch (error) {
    console.error("Delete Product Error: ", error);
    checkForTokenExpiry(error.response.status);
    alert(messageBox, error.response.data.message, 'failed');
  }
  finally {
    loader.classList.add("d-none");
  }
}

const createProductCards = (products) => {
  productsWrapper.innerHTML = '';
  products.map((product) => {
    productsWrapper.innerHTML +=
      `<div class="item product" id='card-${product.id}'>
      <div class="item-header product-header">
        <h4 class="item-name product-name">${product.name}</h4>
        <div>
          <button class="action-btn edit-btn" data-id=${product.id}>
            <i class="fas fa-pen"></i>
          </button>
          <button class="action-btn delete-btn" data-id=${product.id}>
            <i class="fas fa-trash"></i>
          </button>
          <button class="action-btn save-edit-btn d-none" data-id=${product.id}>
            <i class="fas fa-check"></i>
          </button>
        </div>
      </div>
      <p class="item-des product-des">${product.description}</p>
    </div>`;
  });

  const deleteBtns = document.querySelectorAll('.delete-btn');
  deleteBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const productId = e.currentTarget.getAttribute('data-id');
      loader.classList.remove('d-none');
      deleteProduct(productId)
    });
  });

  const editBtns = document.querySelectorAll('.edit-btn');
  editBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const productId = e.currentTarget.getAttribute('data-id');
      const productDes = document.querySelector(`#card-${productId} .product-des`);
      const editBtn = document.querySelector(`#card-${productId} .edit-btn`);
      const deleteBtn = document.querySelector(`#card-${productId} .delete-btn`);
      const saveEditBtn = document.querySelector(`#card-${productId} .save-edit-btn`);
      productDes.setAttribute('contenteditable', true);
      productDes.focus();
      editBtn.classList.add('d-none');
      deleteBtn.classList.add('d-none');
      saveEditBtn.classList.remove('d-none');
      saveEditBtn.addEventListener('click', () => {
        loader.classList.remove('d-none');
        editProduct(productId, {
          description: productDes.textContent
        })
      })
    })
  })
}

const resetProductForm = () => {
  const formInputs = document.querySelectorAll('input');
  formInputs.forEach((input) => {
    input.value = '';
  })
}