/**
 * Created by stefanperndl on 6/12/15.
 */
$(document).ready(function() {
    jQuery("#confirm").click(function(){
        $("<div></div>").appendTo('body')
           .html('<div><h3> write your message for confirm dialog</h3></div>')
           .dialog({
                title: "Confotm Dialog" ,
                width:500, height:300,
                modal:true,
                resizable: false,
                show: { effect: 'drop', direction: "left" },
                hide:{effect:'blind'},
                buttons: {
                    Yes: function() {
                          jQuery.ajax({
                              type:"POST", //post data
                              url:'/edit/{{ dish.slug }}/' // your url that u write in action in form tag
                          }).done(function(result){
                               alert("am done") //this will executes after your view executed
                          })
                     },
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    }
               }
           });
    });
});

