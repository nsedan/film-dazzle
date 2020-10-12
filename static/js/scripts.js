$(document).ready(() => {
  missingInfo();
  ratingSystem();
  searchBarPosition(screenSize);
  screenSize.addListener(searchBarPosition);
  boxofficePagination();
});

// Missing information on DB
function missingInfo() {
  document.body.innerHTML = document.body.innerHTML
    .replace(/N\/A Rated \|/g, "Not yet rated |")
    .replace(/N\/A \|/g, "")
    .replace(/N\/A/g, "")
    .replace(/Unrated Rated/g, "Not yet rated")
    .replace(/Not Rated Rated/g, "Not yet rated");
}

// Rating system for reviews
function ratingSystem() {
  $(document).on("click", "#rating1", () => {
    if ($(".gem1").hasClass("filter")) {
      $(".gem1").removeClass("filter");
    } else {
      $(".gem1, .gem2, .gem3, .gem4, .gem5").addClass("filter");
      $("#rating1").prop("checked", false);
    }
  });
  $(document).on("click", "#rating2", () => {
    if ($(".gem2").hasClass("filter")) {
      $(".gem1, .gem2").removeClass("filter");
    } else {
      $(".gem1, .gem2, .gem3, .gem4, .gem5").addClass("filter");
      $("#rating2").prop("checked", false);
    }
  });
  $(document).on("click", "#rating3", () => {
    if ($(".gem3").hasClass("filter")) {
      $(".gem1, .gem2, .gem3").removeClass("filter");
    } else {
      $(".gem1, .gem2, .gem3, .gem4, .gem5").addClass("filter");
      $("#rating3").prop("checked", false);
    }
  });
  $(document).on("click", "#rating4", () => {
    if ($(".gem4").hasClass("filter")) {
      $(".gem1, .gem2, .gem3, .gem4").removeClass("filter");
    } else {
      $(".gem1, .gem2, .gem3, .gem4, .gem5").addClass("filter");
      $("#rating4").prop("checked", false);
    }
  });
  $(document).on("click", "#rating5", () => {
    if ($(".gem5").hasClass("filter")) {
      $(".gem1, .gem2, .gem3, .gem4, .gem5").removeClass("filter");
    } else {
      $(".gem1, .gem2, .gem3, .gem4, .gem5").addClass("filter");
      $("#rating5").prop("checked", false);
    }
  });
}

// Search bar
const screenSize = window.matchMedia("(max-width: 992px)");
function searchBarPosition(screenSize) {
  if (screenSize.matches) {
    $(".search-bar").removeClass("dropleft");
  } else {
    $(".search-bar").addClass("dropleft");
  }
}

$(document).on("click", ".btn-search", () => {
  $("#search").focus();
});

// Boxoffice active page
function boxofficePagination() {
  let pathname = window.location.search;
  if ((pathname === "?page=1&offset=0") | (pathname === "")) {
    $("#pag1").addClass("btn-outline-secondary");
    $("#pag1").removeClass("btn-secondary");
  }
  if (pathname === "?page=2&offset=25") {
    $("#pag2").addClass("btn-outline-secondary");
    $("#pag2").removeClass("btn-secondary");
  }
  if (pathname === "?page=3&offset=50") {
    $("#pag3").addClass("btn-outline-secondary");
    $("#pag3").removeClass("btn-secondary");
  }
  if (pathname === "?page=4&offset=75") {
    $("#pag4").addClass("btn-outline-secondary");
    $("#pag4").removeClass("btn-secondary");
  }
}
