function selectChoices(docType, sortBy, choiceID, choiceHuman, elementID, removeID) {
  var eid = "#"+elementID;
  $.ajax({
    url: "/cms/get/select/choices",
    data: {
      docType: docType,
      sortby: sortBy,
      choiceID: choiceID,
      choiceHuman: choiceHuman
    },
    dataType: "json",
    success: function(response) {
      // Remove all existing options
      $(eid).empty();
      $(eid).append($("<option>", {
        value: "",
        text: "----",
      }));
      // Add new options
      $.each(response, function(index, value) {
        if(value[0] == removeID) {
          return;
        };
        $(eid).append($('<option>', {
          value: value[0],
          text: value[1],
        }));
      });
    },
    error: function(xhr, status, error) {
        alert('Request was not successful');
    },
  });
};
