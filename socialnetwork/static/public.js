$("#letter").on("click", ".button", function () {

    console.log("click!");  // sanity check
    var formparent = $(this).closest("form");
    var divitme = formparent.closest(".commentarea")
    var contantdata = formparent.find("input[name='comment']").val();
    var id = formparent.find("input[name='userid']").val();
    var csrfmiddlewaretoken = formparent.find("input[name='csrfmiddlewaretoken']").val();
    var name = formparent.find("input[name='username']").val();
    $.ajax({
        url: "/socialnetwork/add-contents", // the endpoint
        type: "POST", // http method
        data: { content: contantdata, userid: id, csrfmiddlewaretoken: csrfmiddlewaretoken }, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success: function (json) {
            var items = json[0];
            var content = items.comment;
            var date = new Date(items.commenttime);
            var profileurl = items.url
            //var username=items.username;
            var newItem = document.createElement("span");
            //newItem.innerHTML = content + date + profileurl;
            if (profileurl == "") {
                newItem.innerHTML = "<div class='commentarea'>\
                    <div class='mypro'>\
                        <div class='mypro_picture'></div>\
                    </div>\
                    <div class='message_content'>\
                        <div class='commentusername'>" + name + "</div>\
                        <span class='commentdate'>"+ date + "</span>\
                        <div class='record'>" + content + "</div>\
                    </div>\
                </div>";
            }
            else {
                newItem.innerHTML = "<div class='commentarea'>\
                    <div class='mypro'>\
                        <img class='mypro_picture' src='/static"+ profileurl + " ' />\
                    </div>\
                    <div class='message_content'>\
                        <div class='commentusername'>" + name + "</div>\
                        <span class='commentdate'>"+ date + "</span>\
                        <div class='record'>" + content + "</div>\
                    </div>\
                </div>";
            }

            divitme.before(newItem);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    //create_post();
});