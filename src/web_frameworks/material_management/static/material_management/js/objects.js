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
function handleObjectClick( event ) {
    // check if
    var element = $( this );
    if ( !(element.hasClass( "active" )) ) {
        $('#dataTable > tbody').empty();
        getRequirements( element );
        element.attr( "aria-current", "true" );
        $( ".object" ).removeClass( "active" );
        element.addClass( "active" );
    }
}

function showRequirements( requirements ) {
    $.each( requirements, function( index ) {
        var item = requirements[index]
        //$( ".data_show" ).append( "<li>list item ${item['name']} </li>" );
        $('#dataTable > tbody:last-child').append(`<tr>
        <td><input class="form-check-input" type="checkbox" hidden></td>
        <td>${item["name"]}</td>
        <td>${item["code_string"]}</td>
        <td>${item["unit"]}</td>
        <td>${item["amount"]}</td>
        </tr>`);
    });
}

function getRequirements ( element ) {

    if ( element.data( "requirements" ) ) {
        showRequirements( element.data( "requirements" ) );
    } else {
        console.log('request');
        $.getJSON( "http://127.0.0.1:8000/api/requirements", {
        object: element.attr('id')
        })
        .done( function( json )  {
            element.data( "requirements", json );
            showRequirements( json );
        })
    }
}
function switchQueryMode ( event ) {
    console.log("switch called")
    var element = $( this );
    if ( element.is( ":checked" ) ) {
        console.log("checked")
        $("#rowCheckbox").show();
    }+
}

$( document ).ready( function() {
    $( ".object-tree" ).on( "click", showChild );
    $( ".object").on("click", handleObjectClick );
    $( "#initQuery").on("click", switchQueryMode );
    $("#textSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#dataTable tbody > tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});
