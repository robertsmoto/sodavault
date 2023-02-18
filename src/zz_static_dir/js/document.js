// creates the lexi field from title
lexiInput("title");

// document data
if (action === "edit") {
    $("#ID").val(obj.ID)
    $("#createdAt").val(obj.createdAt);
    $("#articleBody").val(obj.body);
    $("#articleExcerpt").val(obj.excerpt);
    $("#articleFooter").val(obj.footer);
    } else {
      $("#ID").val(generateNanoid(16))
      $("#createdAt").val(formattedDateTime);
    };

$("#docType").val(docType);
$("#title").val(obj.title)
$("#description").val(obj.description)
$("#lexi").val(obj.lexi);
$("#indx").val(obj.indx);
$("#updatedAt").val(formattedDateTime);

// readonly fields
$("#lexi").attr("readonly", "readonly");
$("#docType").attr("readonly", true);
$("#ID").attr("readonly", true);
$("#createdAt").attr("readonly", "readonly");
$("#updatedAt").attr("readonly", "readonly");

