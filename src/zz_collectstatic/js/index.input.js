function indexInput(elementID) {
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
