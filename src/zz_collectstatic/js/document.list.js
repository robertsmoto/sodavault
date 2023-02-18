function generateNanoid(size) {
  size = size || 21;
  var alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var allowedChars = alphabet.split('');
  var nanoid = '';
  while (nanoid.length < size) {
    var index = Math.floor(Math.random() * allowedChars.length);
    nanoid += allowedChars[index];
  }
  return nanoid;
};

function indexInput(modal) {
  modal.find("#name").on("input", function() {
    var docType = modal.find("#docType").val();
    var name = modal.find("#name").val();
    var lexi = docType.substring(0, 3) + "_" + docType.substring(
        docType.indexOf("_") + 1, 
        docType.indexOf("_") + 4) + "_" + name.toLowerCase().replace(/ /g, "_");
    lexi = lexi.replace(/[^a-zA-Z0-9_]/g, "");
    modal.find("#lexi").val(lexi);
  });
};

// new modal
$(document).on("click", "a[data-action='new']", function (event) {
  $("#attributeNewModal").modal("show");
  var nModal = $("#attributeNewModal"); 
  indexInput(nModal);
  nModal.find('.clear').removeAttr('value');
  var url = $(this).data("url"); // Extract info from data-* attributes
  var title = $(this).data("title");
  var docType = $(this).data("doc-type");
  //var title = "New {{docTypeTitle}}";
  nModal.find(".modal-title").html(title); // Update modal title
  nModal.find("#ID").val(generateNanoid(16));
  nModal.find("#docType").val(docType);
  nModal.find("#ID").val(generateNanoid(16));
  nModal.find("#docType").attr("readonly", "readonly");
  var currentDateTime = new Date();
  var formattedDateTime = currentDateTime.toISOString().slice(0, 19);
  nModal.find("#createdAt").attr("readonly", "readonly");
  nModal.find("#createdAt").val(formattedDateTime);
  nModal.find("#updatedAt").attr("readonly", "readonly");
  nModal.find("#updatedAt").val(formattedDateTime);
  nModal.find("#attributeNewForm").attr("action", url);

});

// edit modal
$(document).on("click", "a[data-action='edit']", function (event) {
  $("#attributeEditModal").modal("show");
  var eModal = $("#attributeEditModal"); 
  indexInput(eModal);
  eModal.find('.clear').removeAttr('value');
  var url = $(this).data("url"); // Extract info from data-* attributes
  var objID = $(this).data("id"); // Extract info from data-* attributes
  var name = $(this).data("name");
  var title = "Edit " + name;
  eModal.find(".modal-title").html(title);
  eModal.find("#attributeEditForm").attr("action", url);
  $.ajax({
    url: "/cms/get/document",
    data: {
      doc_id: objID
    },
    dataType: "json",
    success: function(response) {
      var doc = response;
      // set the form data
      eModal.find("#name").val(doc.name);
      eModal.find("#description").val(doc.description);
      eModal.find("#ID").val(doc.ID);

      //getParentChoices(eModal, doc.parentID);

      eModal.find("#docType").val(doc.docType);
      eModal.find("#lexi").val(doc.lexi);
      eModal.find("#indx").val(doc.indx);
      eModal.find("#createdAt").val(doc.createdAt);
      eModal.find("#createdAt").attr("readonly", "readonly");
      eModal.find("#updatedAt").val(doc.updatedAt);
      eModal.find("#schemaVersion").val(doc.schemaVersion);
    },
    error: function(xhr, status, error) {
        alert('Request was not successful');
    },
  });
});

// delete modal
$(document).on("click", "a[data-action='delete']", function (event) {
  $("#attributeDeleteModal").modal("show");
  var dModal = $("#attributeDeleteModal"); 
  var url = $(this).data("url"); // Extract info from data-* attributes
  var id = $(this).data("ID");
  var name = $(this).data("name");
  // Update the modal"s content.     
  var title = "Delete " + name;
  dModal.find(".modal-title").html(title);
  var warning = "Warning! You are about to delete " + name + ".";
  dModal.find("#formWarning").html(warning);
  // form action
  dModal.find("#attributeDeleteForm").attr("action", url);
});

