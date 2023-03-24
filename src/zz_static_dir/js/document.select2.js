select2_choices(function (data) {
  // handle response data here
  $("#id_parentID").select2({
    theme: 'bootstrap-5',
    width: "100%",
    data: data.results,
  });
  },{ 
      url: "/cms/get/select/choices", 
      collection: DOC.collection, 
      sortBy: "docLexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: DOC.ID, 
      selectedIDs: DOC.docParentID
    }
  );
