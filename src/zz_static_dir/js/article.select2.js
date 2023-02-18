select2_choices(function (data) {
  // handle response data here
  $("#author").select2({
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "author", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.author,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#website").select2({
    data: data.results,
    placeholder: "choose ...",
    width: "100%",
  });
  },{ 
      url: "/cms/get/select/choices", 
      docType: "website", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.website,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#article_category").select2({
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
        "docType": "article_category",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#article_category").append($('<option>', {
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
      docType: "article_category", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.article_category,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#article_tag").select2({
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
      url: "/cms/document/article_tag",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "article_tag",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#article_tag").append($('<option>', {
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
      docType: "article_tag", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.article_tag,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#article_keyword").select2({
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
      url: "/cms/document/article_keyword",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "article_keyword",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#article_keyword").append($('<option>', {
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
      docType: "article_keyword", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.article_keyword,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#recipeCategory").select2({
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
      url: "/cms/document/recipe_category",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipe_category",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#reipeCategory").append($('<option>', {
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
      docType: "recipe_category", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.recipeCategory,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#recipeCookingMethod").select2({
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
      url: "/cms/document/recipe_cook",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipe_cook",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
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
      docType: "recipe_cook", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.recipeCookingMethod,
    }
  );

select2_choices(function (data) {
  // handle response data here
  $("#recipeCuisine").select2({
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
      url: "/cms/document/recipe_cuisine",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipe_cuisine",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#reipeCuisine").append($('<option>', {
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
      docType: "recipe_cuisine", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.recipeCuisine,
    }
  );
  
select2_choices(function (data) {
  // handle response data here
  $("#recipeSuitableForDiet").select2({
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
      url: "/cms/document/recipe_suitable",
      method: "POST",
      //headers: {'X-CSRFToken': CSRFT},
      data: { 
        "csrfmiddlewaretoken": CSRFT,
        "docType": "recipe_suitable",
        "ID": tag.id, 
        "title": tag.text,
        "description": tag.text,
        "lexi": lexi,
      },
      success: function (data) {
        // If the AJAX request was successful, refresh the list of options
        // to include the newly created tag
        $("#reipeSuitableForDiet").append($('<option>', {
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
      docType: "recipe_suitable", 
      sortBy: "lexi:ASC", 
      choiceID: "ID", 
      choiceHuman: "title", 
      removeID: "", 
      selectedIDs: obj.recipeSuitableForDiet,
    }
  );
