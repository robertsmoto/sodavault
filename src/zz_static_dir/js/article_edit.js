function getParentChoices($, pid) {
  $.ajax({
    url: "/cms/get/select/choices",
    data: {
      docType: "article_category",
      sortby: "lexi:ASC",
      choiceID: "ID",
      choiceHuman: "name"
    },
    dataType: "json",
    success: function(response) {

      // Remove all existing options
      $("#parentID").empty();
        
      $("#parentID").append($("<option>", {
        value: "",
        text: "----",
      }));
      // Add new options
      $.each(response, function(index, value) {
        $('#parentID').append($('<option>', {
          value: value[0],
          text: value[1],
        }));
      });
      // Set selection
      if (pid.length > 0) {
          $("#parentID").val(pid).prop("seleted", true);
        } else {
          $("#parentID").val("").prop("selected", true);
        };
    },
    error: function(xhr, status, error) {
        alert('Request was not successful');
    },
  });
};
$(document).ready(function() {
  $('.clear').removeAttr('value');
  $.ajax({
    url: "/cms/get/document",
    data: {
        doc_id: "{{ docID }}",
    },
    dataType: "json",
    success: function(response) {
      var doc = response;
      // base doc
      $("#name").val(doc.name);
      $("#description").val(doc.description);
      $("#ID").val(doc.ID);
      getParentChoices($, "doc.parentID");
      $("#docType").val(doc.docType);
      $("#lexi").val(doc.lexi);
      $("#indx").val(doc.indx);
      $("#createdAt").val(doc.createdAt);
      $("#createdAt").prop("readonly", "true");
      console.log($("#createdAt").val());
      $("#updatedAt").val(doc.updatedAt);
      $("#updatedAt").prop("readonly", "true");
      $("#schemaVersion").val(doc.schemaVersion);
      // attributes
      $("#title").val(doc.title);
      $("#status").val(doc.status);
      $("#highlight").val(doc.highlight);
      $("#author").val(doc.author);
      $("#website").val(doc.website);
    },
  });
  // ckeditor controls
  ClassicEditor
    .create(document.querySelector( '#editorBody'))
    .catch( error => {
        console.error( error );
    } );
  ClassicEditor
    .create(document.querySelector( '#editorExcerpt'))
    .catch( error => {
        console.error( error );
    } );
  ClassicEditor
    .create(document.querySelector( '#editorFooter'))
    .catch( error => {
        console.error( error );
    } );
  // opens the editor menu
  $("#fourthFields").collapse("show");
  $('.chosen-select').select2({
    placeholder: 'Select an option',
    width: '100%',
    });
});

