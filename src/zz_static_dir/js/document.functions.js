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

function lexiInput(prefix, elementID) {
  $(elementID).on("input", function() {
    var collection = $("#id_" + prefix + "-type").val();
    var eidVal = $(elementID).val();
    var lexi = collection.substring(0, 3) + "_" + collection.substring(
        collection.indexOf("_") + 1, 
        collection.indexOf("_") + 4) + "_" + eidVal.toLowerCase().replace(/ /g, "_");
    lexi = lexi.replace(/[^a-zA-Z0-9_]/g, "");
    $("#id_" + prefix + "-lexi").val(lexi);
  });
};
