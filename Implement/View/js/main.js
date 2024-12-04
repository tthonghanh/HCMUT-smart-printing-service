document.querySelectorAll(".file-input").forEach((inputElement) => {
  const dropSection = inputElement.closest(".upload-section");
  initializeUploadArea(dropSection, inputElement);
});

function updateThumbnail(dropSection, inputElement, file) {
  const uploadArea = dropSection.querySelector(".upload-area");

  // Save the initial state
  if (!dropSection.dataset.initialState) {
    dropSection.dataset.initialState = uploadArea.innerHTML;
  }

  const fileName = file.name;
  const fileSize = (file.size / 1024).toFixed(2); // Size in KB
  const fileType = file.type;

  let filePreview = "";
  let fileIcon = "";

  if (fileType === "application/pdf") {
    const fileURL = URL.createObjectURL(file);
    filePreview = `
      <iframe src="${fileURL}" class="file-preview-frame" frameborder="0"></iframe>
    `;
    fileIcon = "../image/pdf.png";
  } else if (fileName.endsWith(".docx")) {
    filePreview = `
      <div class="file-preview-docx">
        <p><strong>${fileName}</strong></p>
        <p>Preview is not supported. You can download or open it.</p>
      </div>
    `;
    fileIcon = "../image/docx.png";
  } else if (fileName.endsWith(".xlsx")) {
    filePreview = `
      <div class="file-preview-xlsx">
        <p><strong>${fileName}</strong></p>
        <p>Preview is not supported. You can download or open it.</p>
      </div>
    `;
    fileIcon = "../image/xlsx.png";
  } else {
    filePreview = `
      <div class="file-preview-unsupported">
        <p><strong>${fileName}</strong></p>
        <p>File type not supported for preview.</p>
      </div>
    `;
  }

  const fileData = `
    <div class="document-section">
      <div class="upload-preview">
        <div class="upload-card">
          <img src="${fileIcon}" alt="File icon" class="document-icon" />
          <div class="document-info">
            <p class="document-name">${fileName}</p>
            <p class="document-size">${fileSize} KB</p>
          </div>
        </div>
      </div>

      <div class="document-preview">
        <div class="preview-container">
          <h2 class="preview-title">Bản xem trước</h2>
          <div class="preview-file">${filePreview}</div>
        </div>
      </div>
    </div>
  `;

  uploadArea.innerHTML = fileData;

  const cancelButton = dropSection.querySelector(".small-button-light");
  cancelButton.addEventListener("click", () => {
    resetUploadArea(dropSection, inputElement);
  });
}

function resetUploadArea(dropSection, inputElement) {
  const uploadArea = dropSection.querySelector(".upload-area");

  if (dropSection.dataset.initialState) {
    uploadArea.innerHTML = dropSection.dataset.initialState;
  }
}

function initializeUploadArea(dropSection, inputElement) {
  const uploadArea = dropSection.querySelector(".upload-area");

  uploadArea.addEventListener("click", () => {
    inputElement.click();
  });

  inputElement.addEventListener("change", () => {
    if (inputElement.files.length) {
      updateThumbnail(dropSection, inputElement, inputElement.files[0]);
    }
  });

  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropSection.classList.add("drop-zone-over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropSection.addEventListener(type, () => {
      dropSection.classList.remove("drop-zone-over");
    });
  });

  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      updateThumbnail(dropSection, inputElement, e.dataTransfer.files[0]);
    }

    dropSection.classList.remove("drop-zone-over");
  });
}

// Select printer
document.querySelectorAll(".printer-item").forEach((item) => {
  item.addEventListener("click", (e) => {
    const radioButton = item.querySelector(".printer-checkbox");
    if (radioButton) {
      radioButton.checked = true;
    }
  })
});

// Select number of buying pages
const minusButton = document.querySelector(".minus");
const plusButton = document.querySelector(".plus");
const quantityInput = document.querySelector("#quantity");
const totalAmount = document.querySelector(".total-amount");
const paymentForm = document.querySelector(".payment-form");
const errorMessage = document.querySelector("#error-message");

const MIN_QUANTITY = 50;
const MAX_QUANTITY = 2000;
const PRICE_PER_PAGE = 200;

function makeEven(number) {
  return number % 2 === 0 ? number : number + 1;
}

function handleErrorMessage(isValid) {
  if (!isValid) {
    errorMessage.textContent = "Số lượng phải là số chẵn trong khoảng từ 50 đến 2000.";
    errorMessage.style.display = "block";
  } else {
    errorMessage.style.display = "none";
  }
}

function validateQuantity(quantity) {
  if (isNaN(quantity) || quantity < MIN_QUANTITY || quantity > MAX_QUANTITY || quantity % 2 !== 0) {
    return false;
  }
  return true;
}

function updateTotalAmount(quantity) {
  const total = quantity * PRICE_PER_PAGE;
  totalAmount.textContent = `${total.toLocaleString()} VND`; // format as currency
}

function updateQuantity(newQuantity) {
  if (newQuantity < MIN_QUANTITY) {
    newQuantity = MIN_QUANTITY;
  } else if (newQuantity > MAX_QUANTITY) {
    newQuantity = MAX_QUANTITY;
  }
  newQuantity = makeEven(newQuantity);
  quantityInput.value = newQuantity;
  updateTotalAmount(newQuantity);
}

paymentForm.addEventListener("submit", (e) => {
  e.preventDefault(); // Prevent form submission
  const currentValue = parseInt(quantityInput.value);
  const isValid = validateQuantity(currentValue);
  handleErrorMessage(isValid);
  paymentForm.submit();
});

minusButton.addEventListener("click", () => {
  const currentValue = parseInt(quantityInput.value) || MIN_QUANTITY;
  updateQuantity(currentValue - 2);
});

plusButton.addEventListener("click", () => {
  const currentValue = parseInt(quantityInput.value) || MIN_QUANTITY;
  updateQuantity(currentValue + 2);
});

quantityInput.addEventListener("blur", () => {
  const currentValue = parseInt(quantityInput.value);
  const isValid = validateQuantity(currentValue);
  handleErrorMessage(isValid); // Show error message if invalid
  if (isValid) {
    updateQuantity(currentValue); // Validate, adjust to even, and update total
  }
});


updateTotalAmount(50); // when page load
