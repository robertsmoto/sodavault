// custom function for using select2 in various conditions
var select2_choices = function (callback, args) {
  $.ajax({
    async: true,
    dataType: "json",
    url: args.url,
    data: { 
        docType: args.docType,
        sortBy: args.sortBy,
        choiceID: args.choiceID,
        choiceHuman: args.choiceHuman,
        removeID: args.removeID,
        selectedIDs: args.selectedIDs
      },
    success: function (response) {
        callback(response);
    }
  });
};
