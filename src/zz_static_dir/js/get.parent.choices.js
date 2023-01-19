function getParentChoices($, pid) {
  $.ajax({
    url: "/cms/get/select/choices",
    data: {
      docType: "article",
      sortby: "lexi:ASC",
      choiceID: "ID",
      choiceHuman: "title"
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
      console.log($("#parentID").val())
    },
    error: function(xhr, status, error) {
        alert('Request was not successful');
    },
  });
};
