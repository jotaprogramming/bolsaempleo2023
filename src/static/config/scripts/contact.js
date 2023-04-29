const contactCity = document.getElementById("contactCity");

async function getContactAttributes() {
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  const formUrl = document.getElementById("formUrl").value;
  const contactEmail = document.getElementById("contactEmail");
  const contactPhone = document.getElementById("contactPhone");
  const contactMsg = document.getElementById("contactMsg");
  const popupAlert = document.getElementById("popupAlert");

  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  headers.append("X-CSRFToken", csrfToken);

  const RAW = JSON.stringify({
    city: contactCity.value,
  });

  const METHOD = "POST";
  const REDIRECT = "follow";

  const requestOptions = {
    method: METHOD,
    headers: headers,
    body: RAW,
    redirect: REDIRECT,
  };

  const promise = await fetch(formUrl, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status == 200) {
        contactEmail.innerHTML = result.data.email;
        contactPhone.innerHTML = result.data.phone;
        contactMsg.innerHTML = result.data.msg_app_number;
        return result;
      }
      setPopUpAlert(result.type, result.msg);
      return result;
    });

  setAlertDelay();
}

if (contactCity) {
  contactCity.addEventListener("change", () => {
    getContactAttributes();
  });
} else {
  setPopUpAlert("warning", "Esta opción no está habilitada por el momento");
  setAlertDelay("alert", 2000);
}
