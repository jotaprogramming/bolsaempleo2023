async function open_modal(url, id='') {
  const resp = await fetch(url);
  const html = await resp.text();
  const defatultModal = document.getElementById("defaultModal");

  defatultModal.innerHTML = html;

  const modalObject = new bootstrap.Modal(defatultModal, {
    keyboard: false,
  });
  modalObject.show();
}
