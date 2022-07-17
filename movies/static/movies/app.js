var display = "less";
function toggleElems(element, id) {
    var hidden = document.getElementById(id);

    if (display == "less") {
        element.innerHTML = "Show less"
        hidden.style.display = "block";
        display = "more"
    } else if (display == "more") {
        element.innerHTML = "See all reviews"; 
        hidden.style.display = "none";
        display = "less";
    }
}

var show = "not";
function toggleMovies(element, id) {
    var hiddenElem = document.getElementById(id);

    if (show == "not") {
        element.innerHTML = "Show less";
        hiddenElem.style.display = "flex";
        show = "yes";
    } else if (show == "yes") {
        element.innerHTML = "See all favourites";
        hiddenElem.style.display = "none";
        show = "not";
    }
}

var view = "hidden";
function toggleWatchlist(element, id) {
    var hiddenElem = document.getElementById(id);

    if (view == "hidden") {
        element.innerHTML = "Show less";
        hiddenElem.style.display = "flex";
        view = "display";
    } else if (view == "display") {
        element.innerHTML = "See full watchlist";
        hiddenElem.style.display = "none";
        view = "hidden";
    }
}