var req;


function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/socialnetwork/getposts", true);
    req.send();
}


function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    var list = document.getElementById("letter");

    // add new posts!
    var idvalue = $('.getid:first').val();
    var user = $("#getuser").val();
    var profileurl = $("#profileurl").val();
    // Parses the response to get a list of JavaScript objects for 
    // the items.
    var items = JSON.parse(req.responseText);

    // Adds new post
    for (var i = 0; i < items.length; i++) {
        // Extracts the item id and text from the response
        var id = items[i]["pk"];  // pk is "primary key", the id
        if (id > idvalue) {
            var itemmessage = items[i]["message"];
            var itemdate = items[i]["date"];
            var date = new Date(itemdate);
            var itemusername = items[i]["username"];
            var url = items[i]["url"];
            var newItem = document.createElement("div");
            var CSRF_TOKEN = Cookies.get('csrftoken');
            if (profileurl == undefined) {
                console.log("hi!");
            }
            if (url == "") {
                if (profileurl == undefined) {
                    newItem.innerHTML =
               "<form action='/socialnetwork/check-profile' method='post'> \
<div class='message'>\
<div class='face_content'>\
<div class='face_picture'></div>\
</div>\
<div class='message_content' >\
<input type='hidden' name='user' value='"+ itemusername + "' />\
<input class='getid' type='hidden' name='idval' value='"+ id + "' />\
<input type='hidden' value='"+ CSRF_TOKEN + "' name='csrfmiddlewaretoken'>\
<input  class='username' type='submit' value='"+ itemusername + "' />\
<span class='date'>"+ date + "</span></p>\
<p class='record'>"+ itemmessage + "</p>\
</div>\
</div >\
</form>\
<div class='commentarea'>\
<div class='mypro'>\
 <div class='mypro_picture'> </div>\
</div>\
<form action='/socialnetwork/add-contents' method='post' id='commentform'>\
<input type='button' class='button' name='submitButton' value='send' />\
<input class='commentc_content' type='text' name='comment' />\
<input type='hidden' name='userid' value='"+ id + "' />\
<input type='hidden' name='username' value='"+ user + "' />\
</form>\
</div>";
                }
                else {
                    newItem.innerHTML =
               "<form action='/socialnetwork/check-profile' method='post'> \
<div class='message'>\
<div class='face_content'>\
<div class='face_picture'></div>\
</div>\
<div class='message_content' >\
<input type='hidden' name='user' value='"+ itemusername + "' />\
<input class='getid' type='hidden' name='idval' value='"+ id + "' />\
<input type='hidden' value='"+ CSRF_TOKEN + "' name='csrfmiddlewaretoken'>\
<input  class='username' type='submit' value='"+ itemusername + "' />\
<span class='date'>"+ date + "</span></p>\
<p class='record'>"+ itemmessage + "</p>\
</div>\
</div >\
</form>\
<div class='commentarea'>\
<div class='mypro'>\
 <img class='mypro_picture' src='/static"+ profileurl + "'>\
</div>\
<form action='/socialnetwork/add-contents' method='post' id='commentform'>\
<input type='button' class='button' name='submitButton' value='send' />\
<input class='commentc_content' type='text' name='comment' />\
<input type='hidden' name='userid' value='"+ id + "' />\
<input type='hidden' name='username' value='"+ user + "' />\
</form>\
</div>";

                }
 }
            else {
                if (profileurl == undefined) {
                    newItem.innerHTML = "<form action='/socialnetwork/check-profile' method='post'> \
<div class='message'>\
<div class='face_content'>\
<img class='face_picture' src='/static"+ url + " '>\
</div>\
<div class='message_content' >\
<input type='hidden' name='user' value='"+ itemusername + "' />\
<input class='getid' type='hidden' name='idval' value='"+ id + "' />\
<input type='hidden' value='"+ CSRF_TOKEN + "' name='csrfmiddlewaretoken'>\
<input  class='username' type='submit' value='"+ itemusername + "' />\
<span class='date'>"+ date + "</span></p>\
<p class='record'>"+ itemmessage + "</p>\
</div>\
</div > \
</form>\
<div class='commentarea'>\
<div class='mypro'>\
 <div class='mypro_picture'></div>\
</div>\
<form action='/socialnetwork/add-contents' method='post' id='commentform'>\
<input type='button' class='button' name='submitButton' value='send' />\
<input class='commentc_content' type='text' name='comment' />\
<input type='hidden' name='userid' value='"+ id + "' />\
<input type='hidden' name='username' value='"+ user + "' />\
</form>\
</div>";
                }
                else {
                    newItem.innerHTML =
                   "<form action='/socialnetwork/check-profile' method='post'> \
<div class='message'>\
<div class='face_content'>\
<img class='face_picture' src='/static"+ url + " '>\
</div>\
<div class='message_content' >\
<input type='hidden' name='user' value='"+ itemusername + "' />\
<input class='getid' type='hidden' name='idval' value='"+ id + "' />\
<input type='hidden' value='"+ CSRF_TOKEN + "' name='csrfmiddlewaretoken'>\
<input  class='username' type='submit' value='"+ itemusername + "' />\
<span class='date'>"+ date + "</span></p>\
<p class='record'>"+ itemmessage + "</p>\
</div>\
</div > \
</form>\
<div class='commentarea'>\
<div class='mypro'>\
 <img class='mypro_picture' src='/static"+ profileurl + "'>\
</div>\
<form action='/socialnetwork/add-contents' method='post' id='commentform'>\
<input type='button' class='button' name='submitButton' value='send' />\
<input class='commentc_content' type='text' name='comment' />\
<input type='hidden' name='userid' value='"+ id + "' />\
<input type='hidden' name='username' value='"+ user + "' />\
</form>\
</div>";
                }
            }

            //list.Prepend(newItem);
            $("#letter form:first-child").before(newItem);
        }
        else {
            return;
        }

    }
}

//$( ".button" ).click(function() { 

function create_post() {
    var contantdata = $('#commentform').find("input[name='comment']").val();
    var id = $('#commentform').find("input[name='userid']").val();
    var csrfmiddlewaretoken = $('#commentform').find("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: "/socialnetwork/add-contents", // the endpoint
        type: "POST", // http method
        data: { content: contantdata, userid: id, csrfmiddlewaretoken: csrfmiddlewaretoken }, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success: function (json) {
            var items = json[0];
            var content = items.comment;
            var id = items.itemid;
            var newItem = document.createElement("div");
            newItem.innerHTML = content + id;
            $("#letter").before(newItem);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


// causes the sendRequest function to run every 5 seconds
window.setInterval(sendRequest, 5000);