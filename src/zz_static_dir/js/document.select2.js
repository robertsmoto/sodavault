select2_choices(function (data) {
  // handle response data here
  $("#parentID").select2({
    placeholder: "choose ...",
    width: "100%",
    data: data.results,
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: docType, 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: obj.ID, 
      selectedIDs: obj.parentID
    }
  );
