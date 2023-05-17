const createButtons = document.getElementsByName("createButtons");
const editButtons = document.getElementsByName("editButtons");
const deleteButtons = document.getElementsByName("deleteButtons");
const uploadPic = document.getElementById("uploadPic");
const previewPic = document.getElementById("previewPic");
const goToSimilarOffers = document.getElementById("goToSimilarOffers");

async function openModal(html) {
  const defatultModal = document.getElementById("defaultModal");

  defatultModal.innerHTML = html;

  const modalObject = new bootstrap.Modal(defatultModal, {
    keyboard: false,
  });
  modalObject.show();
}

async function getHTML(url) {
  const resp = await fetch(url);
  const html = await resp.text();
  return html;
}

function elementOpenModal(element) {
  element.addEventListener("click", async () => {
    const URL = element.getAttribute("id");
    const HTML = await getHTML(URL);
    await openModal(HTML);
  });
}

createButtons.forEach((element) => {
  elementOpenModal(element);
});

editButtons.forEach((element) => {
  elementOpenModal(element);
});

deleteButtons.forEach((element) => {
  elementOpenModal(element);
});

if (goToSimilarOffers) {
  goToSimilarOffers.addEventListener("click", () => {
    const similarOffers = document.getElementById("similarOffers");
    const childList = similarOffers.childNodes;
    childList.forEach((element) => {
      if (element.nodeName.toLowerCase() == "div") {
        element.classList.add("click-effect");
        setTimeout(function () {
          element.classList.remove("click-effect");
        }, 1000);
      }
    });
  });
}

if (uploadPic) {
  uploadPic.addEventListener("change", () => {
    const [file] = uploadPic.files;
    if (file) {
      const src = URL.createObjectURL(file);
      const alt = file.name;
      previewPic.innerHTML = `<img src="${src}" alt="${alt}">`;
    }
  });
}

// Slider Assets
const slider = document.querySelector("#slider");
const sliderSection = document.querySelectorAll(".slider__section");

if (slider && sliderSection) {
  let sliderSectionLast = sliderSection[sliderSection.length - 1];

  const btnLeft = document.querySelector("#btn-left");
  const btnRight = document.querySelector("#btn-right");

  slider.insertAdjacentElement("afterbegin", sliderSectionLast);

  /**
   * The function moves the first slide of a slider to the end with a sliding animation.
   */
  function Next() {
    let sliderSectionFirst = document.querySelectorAll(".slider__section")[0];
    slider.style.marginLeft = "-100%";
    slider.style.transition = "all 0.5s";
    setTimeout(function () {
      slider.style.transition = "none";
      slider.insertAdjacentElement("beforeend", sliderSectionFirst);
      slider.style.marginLeft = "0";
    }, 500);
  }
  /**
   * The function moves the last element of a slider to the beginning with a sliding animation.
   */
  function Prev() {
    let sliderSection = document.querySelectorAll(".slider__section");
    let sliderSectionLast = sliderSection[sliderSection.length - 1];
    slider.style.marginLeft = "0";
    slider.style.transition = "all 0.5s";
    setTimeout(function () {
      slider.style.transition = "none";
      slider.insertAdjacentElement("afterbegin", sliderSectionLast);
      slider.style.marginLeft = "-100%";
    }, 500);
  }
  btnRight.addEventListener("click", function () {
    Next();
  });
  btnLeft.addEventListener("click", function () {
    Prev();
  });

  setInterval(() => {
    Next();
  }, 4000);
}

function setPopUpAlert(type = "danger", msg = "Error") {
  const div = document.createElement("div");
  const template = `
			<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
			${msg}
			`;
  div.classList.add(
    "alert",
    `alert-${type}`,
    "alert-dismissible",
    "fade",
    "show"
  );
  div.setAttribute("id", "alert");
  div.setAttribute("role", "alert");
  div.innerHTML = template;
  popupAlert.appendChild(div);
}

function setAlertDelay(idElement = "alert", delay = 1000) {
  const vAlert = document.getElementById(idElement);
  if (vAlert) {
    setTimeout(() => {
      const alert = bootstrap.Alert.getOrCreateInstance(`#${idElement}`);
      alert.close();
    }, delay);
  }
}
