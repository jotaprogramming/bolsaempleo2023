let currentPage = 1;
let clickPDFUpBtn = false;
const pdfUpBtn = document.getElementById("pdfUpBtn");
const pdfThumbnail = document.getElementById("pdfThumbnail");

/**
 * This function loads a PDF document and displays its first page as a thumbnail.
 * @param url - The URL of the PDF file to be loaded and rendered as a thumbnail.
 */
async function loadPDFThumbnail(url) {
  const loadingTask = pdfjsLib.getDocument(url);

  const pdfDoc = await loadingTask.promise;
  pdfThumbnail.innerHTML = "";

  const page = await pdfDoc.getPage(1);
  const viewport = page.getViewport({ scale: 0.2 });
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  canvas.className = "pdf-thumbnail-page";
  canvas.height = viewport.height;
  canvas.width = viewport.width;
  pdfThumbnail.appendChild(canvas);

  await page.render({ canvasContext: context, viewport: viewport }).promise;

  const pdfPages = document.querySelectorAll(".pdf-thumbnail-page");
  pdfPages[0].style.display = "block"; // Mostrar la primera página inicialmente
  pdfUpBtn.classList.remove("pdf-thumbnail-hover-hidden");
  pdfUpBtn.classList.add("pdf-thumbnail-hover");
}

/**
 * The function loads a PDF document and displays it in a modal with navigation buttons.
 * @param url - The URL of the PDF file to be loaded and displayed.
 */
async function loadPDF(url) {
  const loadingTask = pdfjsLib.getDocument(url);
  const pdfDoc = await loadingTask.promise;
  const container = document.createElement("div");

  container.classList.add("modal-dialog", "modal-dialog-centered", "modal-lg");
  container.innerHTML = `
  <div class="modal-content">
    <div class="modal-header">
      <h5 class="modal-title" id="pdfModalLabel">Visor de PDF</h5>
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
      <div class="d-flex justify-content-center">
        <div class="spinner-border" style="width: 2rem; height: 2rem;" role="status" id="spinnerPdf">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div id="pdfViewer" class="overflow-hidden rounded-4">
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <div class="w-100 d-flex justify-content-center align-items-center gap-2">
        <button type="button" class="btn btn-secondary" onclick="previousPage()">Anterior</button>
        <span id="currentPage"></span>
        <button type="button" class="btn btn-secondary" onclick="nextPage()">Siguiente</button>
      </div>
    </div>
  </div>`;

  await openModal(container.outerHTML);

  const pdfViewer = document.getElementById("pdfViewer");

  pdfViewer.innerHTML = "";

  for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
    const page = await pdfDoc.getPage(pageNum);
    const viewport = page.getViewport({ scale: 1.0 });
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    canvas.className = "pdf-page";
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    pdfViewer.appendChild(canvas);

    await page.render({ canvasContext: context, viewport: viewport }).promise;
  }
  document.getElementById("spinnerPdf").classList.add("d-none");
  clickPDFUpBtn = false;
  showPage(currentPage);
}

/**
 * The function shows a specific page of a PDF document and updates the current page number.
 * @param pageNum - The page number that needs to be displayed.
 */
function showPage(pageNum) {
  const pdfPages = document.querySelectorAll(".pdf-page");
  const currentPageElement = document.getElementById("currentPage");
  if (pageNum < 1) {
    pageNum = 1;
  } else if (pageNum > pdfPages.length) {
    pageNum = pdfPages.length;
  }

  currentPage = pageNum;
  pdfPages.forEach(function (page) {
    page.style.display = "none";
  });

  pdfPages[currentPage - 1].style.display = "block";
  currentPageElement.textContent = currentPage + " / " + pdfPages.length;
}

/**
 * The function "previousPage()" is used to show the previous page by calling the "showPage()" function
 * with the current page number minus one as its argument.
 */
function previousPage() {
  showPage(currentPage - 1);
}

/**
 * The function nextPage() shows the next page.
 */
function nextPage() {
  showPage(currentPage + 1);
}

/* This code block is checking if the variable `pdfUpBtn` exists and is not null. If it is not null, it
gets the URL attribute of the `pdfUpBtn` element and adds a click event listener to it. When the
button is clicked, it checks if `clickPDFUpBtn` is false, and if it is, it sets it to true and calls
the `loadPDF()` function with the URL as its argument. It also adds a window load event listener
that calls the `loadPDFThumbnail()` function with the URL as its argument. */
if (pdfUpBtn) {
  const url = pdfUpBtn.getAttribute("url");
  pdfUpBtn.addEventListener("click", () => {
    if (!clickPDFUpBtn) {
      clickPDFUpBtn = true;
      loadPDF(url);
    }
  });
  window.addEventListener("load", () => {
    loadPDFThumbnail(url);
  });
}
