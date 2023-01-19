// function generateNanoid(size)
// function indexInput(modal, elementID)
// function selectChoices(pid, docType, sortBy, choiceID, choiceHuman, elementID)
 
// edit modal
$(document).on(
"click", "a[data-action='edit'], a[data-action='new']", function (event) {
  $("#postModal").modal("show");
  var url = $(this).data("url"); // Extract info from data-* attributes
  var objID = $(this).data("id"); // Extract info from data-* attributes
  var name = $(this).data("name");
  var title = $(this).data("title");
  var action = $(this).data("action"); // use to switch between 'new' 'edit'
  var doc_type = $(this).data("doc-type");
  // need to switch between new and edit
  $(".modal-title").empty().html(title);
  $("#postForm").attr("action", url);
  indexInput("domain");
  // set dates
  var currentDateTime = new Date();
  var formattedDateTime = currentDateTime.toISOString().slice(0, 19);
  $("#ID").attr("readonly", true);
  $("#docType").val(doc_type);
  $("#docType").attr("readonly", true);
  $("#createdAt").attr("readonly", "readonly");
  $("#createdAt").val(formattedDateTime);
  $("#updatedAt").attr("readonly", "readonly");
  $("#updatedAt").val(formattedDateTime);
  if(action=="edit") {
    $.ajax({
      url: "/cms/get/document",
      data: {
        doc_id: objID
      },
      dataType: "json",
      success: function(response) {
        var doc = response;
        // set the form data
        $("#domain").val(doc.domain);
        $("#url").val(doc.url);
        $("#description").val(doc.description);
        $("#ID").val(doc.ID);
        selectChoices(docType=doc_type, sortBy="lexi:ASC", choiceID="ID", 
          choiceHuman="domain", elementID="parentID", removeID=doc.ID);
        // Set #parentID selection
        if (doc.parentID.length > 0) {
            $("#parentID").val(doc.parentID);
          } else {
            $("#parentID").val("");
          };
        $("#docType").val(doc.docType);
        $("#lexi").val(doc.lexi);
        $("#indx").val(doc.indx);
        $("#createdAt").val(doc.createdAt);
        $("#schemaVersion").val(doc.schemaVersion);
      },
      error: function(xhr, status, error) {
          alert('Request was not successful');
      },
    });
  } else {
    // clear all elements with class="clear"
    $('.clear').val('');
    selectChoices(docType=doc_type, sortBy="lexi:ASC", choiceID="ID", 
      choiceHuman="domain", elementID="parentID", removeID="");
    $("#ID").val(generateNanoid(16))
  };
});

// delete modal
$(document).on("click", "a[data-action='delete']", function (event) {
  $("#deleteModal").modal("show");
  var dModal = $("#deleteModal"); 
  var url = $(this).data("url"); // Extract info from data-* attributes
  var id = $(this).data("ID");
  var name = $(this).data("name");
  // Update the modal"s content.     
  var title = "Delete " + name;
  dModal.find(".modal-title").html(title);
  var warning = "Warning! You are about to delete " + name + ".";
  dModal.find("#formWarning").html(warning);
  // form action
  dModal.find("#deleteForm").attr("action", url);
});
