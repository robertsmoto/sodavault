// update textarea to ckeditor interface
$(document).ready(function() {
  // ckeditor controls
  const selectors = ['#body', '#excerpt', '#footer'];
  for (const selector of selectors) {
    ClassicEditor
      .create(document.querySelector(selector))
      .catch(error => {
        console.error(error);
      });
    };
  // opens the editor menu
  $("#editFields").collapse("show");
  });
