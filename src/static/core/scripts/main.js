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







// Slider Assets
const slider = document.querySelector("#slider");
let sliderSection = document.querySelectorAll(".slider__section");
let sliderSectionLast = sliderSection[sliderSection.length -1];

const btnLeft = document.querySelector("#btn-left");
const btnRight = document.querySelector("#btn-right");


slider.insertAdjacentElement('afterbegin',sliderSectionLast);

function Next(){
    let sliderSectionFirst = document.querySelectorAll(".slider__section")[0];
    slider.style.marginLeft = "-100%";
    slider.style.transition = "all 0.5s";
    setTimeout(function (){
        slider.style.transition ="none";
        slider.insertAdjacentElement('beforeend',sliderSectionFirst);
        slider.style.marginLeft = "0";

    }, 500);
}
function Prev(){
    let sliderSection= document.querySelectorAll(".slider__section");
    let sliderSectionLast = sliderSection[sliderSection.length -1];
    slider.style.marginLeft = "0";
    slider.style.transition = "all 0.5s";
    setTimeout(function (){
        slider.style.transition ="none";
        slider.insertAdjacentElement('afterbegin',sliderSectionLast);
        slider.style.marginLeft = "-100%";

    }, 500);
}
btnRight.addEventListener('click',function(){
    Next();
});
btnLeft.addEventListener('click',function(){
    Prev();
});


setInterval(() => {
   Next();
}, 4000);









