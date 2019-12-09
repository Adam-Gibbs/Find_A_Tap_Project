function LoadSearch() {
    var search = document.getElementById('SearchInput').value
    url = window.location.href;
    var split_url = url.split('!');
    var post_coords = split_url[1]
    var url = ("/home/taps/search=£" + search + "£/page=$0$/!" + post_coords)

    window.location.href = url
}