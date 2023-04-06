
select2_choices(function (data) {
  // handle response data here
  $("#id_articleCategory").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "art_cat_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/article_category",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "articleCategory",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#id_articleCategory").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "articleCategory", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.articleCategory,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#id_articleTag").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "art_tag_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/articleTag",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "articleTag",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#id_articleTag").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "articleTag", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.articleTag,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#id_articleKeyword").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "art_key_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/articleKeyword",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "articleKeyword",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#id_articleKeyword").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "articleKeyword", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.articleKeyword,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#id_recipeCategory").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "rec_cat_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/recipeCategory",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipeCategory",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#id_reipeCategory").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "recipeCategory", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.recipeCategory,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#id_recipeCookingMethod").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "rec_coo_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/recipeCookingMethod",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipeCookingMethod",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#reipeCookingMethod").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "recipeCookingMethod", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.recipeCookingMethod,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#id_recipeCuisine").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "rec_cui_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/recipeCuisine",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipeCuisine",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#id_reipeCuisine").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "recipeCuisine", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.recipeCuisine,
    }
  );
  
select2_choices(function (data) {
  // handle response data here
  $("#id_recipeSuitableForDiet").select2({
    tags: true,
    tokenSeparators: [',', ' '],
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
    createTag: function (params) {
        var term = $.trim(params.term);
        var nid = generateNanoid(16);

        if (term === '') {
          return null;
        };

        return {
          id: nid,
          text: term,
          newTag: true,
        }
      },
  }).on("select2:selecting", function (e) {
  var tag = e.params.args.data;
  var lexi = "rec_sui_" + tag.text.toLowerCase().substring(0, 3);
  var indx = tag.text.toLowerCase()
  const CSRFT = document.querySelector('[name=csrfmiddlewaretoken]').value;
  if (tag.newTag) {
    console.log("new tag has been created")
    // Send an AJAX request to add the new tag to the database
    $.ajax({
      url: "/cms/document/recipeSuitableForDiet",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipeSuitableForDiet",
        "docID": tag.id, 
        "docTitle": tag.text,
        "docDescription": tag.text,
        "docLexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#id_reipeSuitableForDiet").append($('<option>', {
          value: data.id,
          text: data.text
        }));
      },
      error: function (xhr, status, error) {
        console.log("Error adding new tag: " + error);
      }
    });
    }
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "recipeSuitableForDiet", 
      sortBy: "docLexi:ASC", 
      choiceID: "docID", 
      choiceHuman: "docTitle", 
      removeID: "", 
      selectedIDs: obj.recipeSuitableForDiet,
    }
  );

