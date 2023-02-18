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

function lexiInput(elementID) {
  eid = "#"+elementID
  $(eid).on("input", function() {
    var docType = $("#docType").val();
    var name = $(eid).val();
    var lexi = docType.substring(0, 3) + "_" + docType.substring(
        docType.indexOf("_") + 1, 
        docType.indexOf("_") + 4) + "_" + name.toLowerCase().replace(/ /g, "_");
    lexi = lexi.replace(/[^a-zA-Z0-9_]/g, "");
    $("#lexi").val(lexi);
  });
};

function select2_choices(callback, args) {
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
