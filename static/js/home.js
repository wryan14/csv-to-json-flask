let csvForm = document.getElementById("csvForm");
if (csvForm) {
  csvForm.addEventListener("submit", function(event) {
    event.preventDefault();
    document.getElementById("spinner").style.display = "block";
    document.getElementById("success-message").style.display = "none";
    document.getElementById("error-message").style.display = "none";
    let form_data = new FormData(csvForm);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
    xhr.onload = function (e) {
      document.getElementById("spinner").style.display = "none";
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          csvForm.reset();
          document.getElementById("success-message").style.display = "block";
        } else {
          document.getElementById("error-message").style.display = "block";
          console.error(xhr.statusText);
        }
      }
    };
    xhr.send(form_data);
  });
}
