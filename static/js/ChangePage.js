function ChangePage(change) {
    url = window.location.href;
    var split_url = url.split('$');
    var page_num = Number(split_url[1])
    var pre_num = split_url[0]
    var post_num = split_url[2]
    if ((page_num + change.valueOf()) < 0){
        var new_page_num = 0
    } else {
        var new_page_num = (page_num + change.valueOf())
    }
    var url = (pre_num + "$" + new_page_num + "$" + post_num)

    window.location.href = url

}
