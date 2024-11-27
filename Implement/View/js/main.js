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
