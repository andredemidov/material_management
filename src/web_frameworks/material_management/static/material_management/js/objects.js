function getHighLevelObjects() {
    $.ajax({
        // The URL for the request
        url: "http://127.0.0.1:8000/api/objects",

        // The data to send (will be converted to a query string
        data: {
            parent: "null"
        },

        // Whether this is a POST or GET request
        type: "GET",

        // The type of data we expect back
        dataType : "json",
    })
};

function getChildObjects( element ) {
    //var element = $( this );
    var object_id = element.attr("id");
// Get JSON-formatted data from the server
    $.getJSON( "http://127.0.0.1:8000/api/objects", {
        parent: object_id
    })
    .done( function( json ) {
        console.log(json);
        element.data( "child", json )
    })

};

function getHighObjects() {
// Get JSON-formatted data from the server
$.getJSON( "http://127.0.0.1:8000/api/objects", {
        parent: "null"
    }, function( resp ) {
    // Log each key in the response data
    $.each( resp, function( key, value ) {
        console.log( key + " : " + value );
    });
})
};

function showChild( event ) {
    var element = $( this );
    if ( element.data( "child" ) ) {
        console.log("There is child!");
        console.log( element.data( "child" ) );
    } else {
        console.log("get child...");
        getChildObjects( element );
        console.log("Complete!");
        console.log( element.data( "child" ) );
    }
    console.log("Continue...");
    for (item in element.data( "child" )) {
        var new_element = element.clone(true);
        new_element.attr({
            id: item['id']
        });
        element.after(new_element)
    }

}
$( document ).ready( function() {
    $( ".object-tree" ).on( "click", showChild );
});


//$( document ).ready( getHighObjects );
