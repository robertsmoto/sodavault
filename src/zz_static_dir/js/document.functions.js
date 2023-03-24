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
  $(elementID).on("input", function() {
    var collection = $("#id_type").val();
    var eidVal = $(elementID).val();
    var lexi = collection.substring(0, 3) + "_" + collection.substring(
        collection.indexOf("_") + 1, 
        collection.indexOf("_") + 4) + "_" + eidVal.toLowerCase().replace(/ /g, "_");
    lexi = lexi.replace(/[^a-zA-Z0-9_]/g, "");
    $("#id_lexi").val(lexi);
  });
};

//function select2_choices(callback, args) {
  //$.ajax({
    //async: true,
    //dataType: "json",
    //url: args.url,
    //data: { 
        //collection: args.collection,
        //sortBy: args.sortBy,
        //choiceID: args.choiceID,
        //choiceHuman: args.choiceHuman,
        //removeID: args.removeID,
        //selectedIDs: args.selectedIDs
      //},
    //success: function (response) {
        //callback(response);
    //}
  //});
//};
