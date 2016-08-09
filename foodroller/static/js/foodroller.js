/**
 * Created by stefanperndl on 29/02/16.
 */

var man_day;

$(document).ready(function() {
    $('.datepicker').datepicker();

    $('#confirm-delete').on('show.bs.modal', function(e) {
        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    });
});

function openDateModal() {
    $("#change-date-modal").modal('show');
}

function openSearchModal(id) {
    man_day = id;
    console.log(man_day);
    $("#search-modal").modal();
}

function openSummaryModal() {
    $.get("/summary/", function(data){
        if (data == -1)
            $(".alert").show();
        $("#email").html(data);
        $("#accept-modal").modal('show');

    });
}

/// Autocomplete function for "search food"
$(function() {
    $("#txtSearch").autocomplete({
        source: "/search/"
    });
});

/// Sets received data into the resulting food div of the selected day
function setFoodInDiv(day, data) {
    var divId = "#day-res-".concat(day);
    console.log(divId);
    $(divId).html(data);
}

/// Get food object from server, depending on the entered value in searchText textfield
function getFood() {
    var name=$("#txtSearch").val();
    $.get("/search-food/", {name: name, day: man_day}, function(data){
        setFood(man_day, data);
    });
}

function setFood() {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    var name=$("#txtSearch").val();
    $.post("/search/", {name: name, day: man_day}, function(data){
        setFoodInDiv(man_day, data);
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
        console.log(data);
        setFoodInDiv(man_day, data);
    });
}

$(".nav a").on("click", function(){
    $(".nav").find(".active").removeClass("active");
    $(this).parent().addClass("active");
});

function cloneMore(selector, type) {
    console.log(selector, type);
    var newElement = $(selector).clone(true);
    console.log("inCLONE");
    var total = $('#id_ingredient-TOTAL_FORMS').val();
    console.log(total);
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_ingredient-TOTAL_FORMS').val(total);
    console.log(newElement);
    $(selector).after(newElement);
}