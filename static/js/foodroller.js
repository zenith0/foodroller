/**
 * Created by stefanperndl on 29/02/16.
 */

var man_day;

function openDateModal() {
    $("#change-date-modal").modal('show');
}

function openSearchModal(id) {
    man_day = id;
    console.log(man_day);
    $("#search-modal").modal();
}

function openSummaryModal() {
    $("#accept-modal").modal('show');
}

/// Autocomplete function for "search food"
$(function() {
    $("#txtSearch").autocomplete({
        source: "/search"
    });
});

/// Sets received data into the resulting food div of the selected day
function setFood(day, data) {
    var divId = "#day-res-".concat(man_day);
    $(divId).html(data);
}

/// Get food object from server, depending on the entered value in searchText textfield
function getFood() {
    var name=$("#txtSearch").val();
    $.get("/search-food/", {name: name, day: man_day}, function(data){
        setFood(man_day, data);
    });
}

/// Roll food for a specific day
function roll(id) {
    man_day = id;
    var categoryId = "category-".concat(id);
    var catSelects = document.getElementById(categoryId);
    var cat = catSelects.options[catSelects.selectedIndex].value;

    var cookingTimeId = "cooking-time-".concat(id);
    var timeSelects = document.getElementById(cookingTimeId);
    var time = timeSelects.options[timeSelects.selectedIndex].value;

    $.get("/roll-food/", {day: man_day, cat: cat, time: time}, function(data) {
        setFood(man_day, data);
    });
}
