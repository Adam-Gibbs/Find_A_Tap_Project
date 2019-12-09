function Addcomment() {
    var comment = document.forms["commentForm"]["inputComment"].value;
    var TapID = document.getElementById('id').innerHTML;
    $.ajax({
        type : "POST",
        url : "/AddComment",
        data: JSON.stringify({'commentData': comment, 'tapID': TapID}),
        contentType: 'application/json;charset=UTF-8',
        success: function() {
            location.reload()
            TapID.innerHTML = "";
        }
    });
}
