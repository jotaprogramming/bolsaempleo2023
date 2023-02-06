async function open_modal(url) {
  const resp = await fetch(url);
  const html = await resp.text();
  const defatultModal = document.getElementById("defaultModal");

  defatultModal.innerHTML = html;

  const modalObject = new bootstrap.Modal(defatultModal, {
    keyboard: false,
  });
  modalObject.show();
}

function elementOpenModal(element) {
  element.addEventListener("click", () => {
    const URL = element.getAttribute("id");
    open_modal(URL);
  });
}

const createButtons = document.getElementsByName("createButtons");
const editButtons = document.getElementsByName("editButtons");
const deleteButtons = document.getElementsByName("deleteButtons");

createButtons.forEach((element) => {
  elementOpenModal(element);
});

editButtons.forEach((element) => {
  elementOpenModal(element);
});

deleteButtons.forEach((element) => {
  elementOpenModal(element);
});
