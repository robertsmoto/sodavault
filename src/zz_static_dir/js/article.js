// metadata
$(document).attr("title", pageTitle);

// recipe ingredient rows 
// select the target container to hold the duplicated rows
var $container = $('.ingredient-container');

// the starting index
var index = 1;

// select the button that triggers the duplication
$('#add-ingredient').click(function() {

  // makes the window scroll
  $("html, body").animate({
    scrollTop: $("#ingredients").offset().top - 100
  }, 500);

  // clone the first row
  var $row = $('#recipe-ingredient-0').clone();
  
  // update the id and name of the cloned row
  $row.attr('id', 'recipe-ingredient-' + index);
  $row.find('.recipe-ingredient-name').attr(
      'id', 'id_recipe_ingredient_' + index + '_name').attr(
          'name', 'recipe_ingredient_' + index + '_name');
  $row.find('.recipe-ingredient-quantity').attr(
      'id', 'recipe_ingredient_' + index + '_quantity').attr(
          'name', 'recipe_ingredient_' + index + '_quantity');
  $row.find('.recipe-ingredient-unit').attr(
      'id', 'recipe_ingredient_' + index + '_unit').attr(
          'name', 'recipe_ingredient_' + index + '_unit');
  $row.find('.recipe-ingredient-note').attr(
      'id', 'recipe_ingredient_' + index + '_note').attr(
          'name', 'recipe_ingredient_' + index + '_notes');
  $row.find('.delete-link a').removeClass("d-none").addClass("d-inline");

  // append the cloned row to the container
  $container.append($row);
  
  // increment the index for the next row
  index++;
});

// deletes ingredient row
$(document).on('click', '.delete-link a', function(e){
  e.preventDefault();
  $(this).closest('.ingredient-row').remove();
});

if(action === "edit") {
  // add existing ingredients
  // Populate the first row with existing data
  $('#id_recipe_ingredient_0_name').val(ingredientData['0'].name);
  $('#id_recipe_ingredient_0_quantity').val(ingredientData['0'].quantity);
  $('#id_recipe_ingredient_0_unit').val(ingredientData['0'].unit);
  $('#id_recipe_ingredient_0_note').val(ingredientData['0'].note);
  // add remaining ingredients to additional rows
  $.each(ingredientData, function(i, ingredient) {
    if (i==0) {
      return;
    };
    var $row = $('#recipe-ingredient-0').clone();
    $row.attr('id', 'id_recipe_ingredient_' + i);
    $row.find('.recipe-ingredient-name').attr(
      'id', 'id_recipe_ingredient_' + i + '_name').attr(
        'name', 'recipe_ingredient_' + i + '_name').val(ingredient.name);
    $row.find('.recipe-ingredient-quantity').attr(
      'id', 'id_recipe_ingredient_' + i + '_quantity').attr(
        'name', 'recipe_ingredient_' + i + '_quantity').val(ingredient.quantity);
    $row.find('.recipe-ingredient-unit').attr(
      'id', 'id_recipe_ingredient_' + i + '_unit').attr(
        'name', 'recipe_ingredient_' + i + '_unit').val(ingredient.unit);
    $row.find('.recipe-ingredient-note').attr(
      'id', 'id_recipe_ingredient_' + i + '_note').attr(
        'name', 'recipe_ingredient_' + i + '_note').val(ingredient.notes);
    $row.find('.delete-link a').removeClass("d-none").addClass("d-inline");
    $container.append($row);
    });
  };

// populate fields
// article fileds
$("#headline").val(obj.headline);
$("#subHeadline").val(obj.subHeadline);
$("#status").val(obj.status);
$("#highlight").val(obj.highlight);
$("#recipe-name").val(obj.recipe.name);
$("#recipe-nutrition-servingSize").val(
    obj.recipe.nutrition.servingSize);
$("#recipe-nutrition-calories").val(obj.recipe.nutrition.calories);
$("#recipe-nutrition-fatContent").val(obj.recipe.nutrition.fatContent);
$("#recipe-nutrition-saturatedFat").val(
    obj.recipe.nutrition.saturatedFat);
$("#recipe-nutrition-unsaturatedFat").val(
    obj.recipe.nutrition.unsaturatedFat);
$("#recipe-nutrition-transFat").val(obj.recipe.nutrition.transFat);
$("#recipe-nutrition-cholesterolContent").val(
    obj.recipe.nutrition.cholesterolContent);
$("#recipe-nutrition-sodiumContent").val(
    obj.recipe.nutrition.sodiumContent);
$("#recipe-nutrition-carbohydrateContent").val(
    obj.recipe.nutrition.carbohydrateContent);
$("#recipe-nutrition-fiberContent").val(
    obj.recipe.nutrition.fiberContent);
$("#recipe-nutrition-sugarContent").val(
    obj.recipe.nutrition.sugarContent);
$("#recipe-nutrition-proteinContent").val(
    obj.recipe.nutrition.proteinContent);
$("#recipe-yield-quantity").val( obj.recipe.yield.quantity);
$("#recipe-yield-description").val(
    obj.recipe.yield.description);
$("#recipe-yield-notes").val(
    obj.recipe.yield.notes);
$("#recipe-prepTime-hours").val(
    obj.recipe.prepTime.hours);
$("#recipe-prepTime-minutes").val(
    obj.recipe.prepTime.minutes);
$("#recipe-cookTime-hours").val(
    obj.recipe.cookTime.hours);
$("#recipe-cookTime-minutes").val(
    obj.recipe.cookTime.minutes);
$("#recipe-instructions").val(
    obj.recipe.instructions);
