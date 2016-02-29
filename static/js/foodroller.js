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

  $(function() {
    $("#txtSearch").autocomplete({
      source: "/search"
    });
  });

  function getFood() {
    var name=$("#txtSearch").val();
    $.get("/search-food/", {name: name}, function(data){
      var divId = "#day-res-".concat(man_day);
      $(divId).html(data);
    });
  }