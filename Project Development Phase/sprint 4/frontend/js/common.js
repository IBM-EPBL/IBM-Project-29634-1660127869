const logoutBtn = document.querySelector('#logout-btn');

const logoutUser = () => {
  localStorage.removeItem('token');
  window.location.href = '/login.html';
}

logoutBtn.addEventListener('click', logoutUser);
