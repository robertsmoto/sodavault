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
      'id', 'recipe-ingredient-' + index + '-name').attr(
          'name', 'recipe-ingredient-' + index + '-name');
  $row.find('.recipe-ingredient-quantity').attr(
      'id', 'recipe-ingredient-' + index + '-quantity').attr(
          'name', 'recipe-ingredient-' + index + '-quantity');
  $row.find('.recipe-ingredient-unit').attr(
      'id', 'recipe-ingredient-' + index + '-unit').attr(
          'name', 'recipe-ingredient-' + index + '-unit');
  $row.find('.recipe-ingredient-notes').attr(
      'id', 'recipe-ingredient-' + index + '-notes').attr(
          'name', 'recipe-ingredient-' + index + '-notes');
  $row.find('.delete-link a').removeClass("d-none").addClass("d-inline");

  // append the cloned row to the container
  $container.append($row);
  
  // increment the index for the next row
  index++;
});

// add existing ingredients
var ingredientData = "{{ obj.recipe.ingredient|safe }}"
// Populate the first row with existing data
$('#recipe-ingredient-0-name').val(ingredientData['0'].name);
$('#recipe-ingredient-0-quantity').val(ingredientData['0'].quantity);
$('#recipe-ingredient-0-unit').val(ingredientData['0'].unit);
$('#recipe-ingredient-0-notes').val(ingredientData['0'].notes);
// add remaining ingredients to additional rows
$.each(ingredientData, function(i, ingredient) {
  if (i==0) {
    return;
  };
  var $row = $('#recipe-ingredient-0').clone();
  $row.attr('id', 'recipe-ingredient-' + i);
  $row.find('.recipe-ingredient-name').attr(
    'id', 'recipe-ingredient-' + i + '-name').attr(
      'name', 'recipe-ingredient-' + i + '-name').val(ingredient.name);
  $row.find('.recipe-ingredient-quantity').attr(
    'id', 'recipe-ingredient-' + i + '-quantity').attr(
      'name', 'recipe-ingredient-' + i + '-quantity').val(ingredient.quantity);
  $row.find('.recipe-ingredient-unit').attr(
    'id', 'recipe-ingredient-' + i + '-unit').attr(
      'name', 'recipe-ingredient-' + i + '-unit').val(ingredient.unit);
  $row.find('.recipe-ingredient-notes').attr(
    'id', 'recipe-ingredient-' + i + '-notes').attr(
      'name', 'recipe-ingredient-' + i + '-notes').val(ingredient.notes);
  $row.find('.delete-link a').removeClass("d-none").addClass("d-inline");

  $container.append($row);
  });

// deletes ingredient row
$(document).on('click', '.delete-link a', function(e){
  e.preventDefault();
  $(this).closest('.ingredient-row').remove();
});

