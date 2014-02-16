$(function () {
  $('.tablesorter').tablesorter({
    textExtraction: function (node) {
      if (node.textContent) {
        return node.textContent;
      } else {
        if (node.childNodes[1] && node.childNodes[1].title) {
          return node.childNodes[1].title;
        }
        else if (node.childNodes[0] && node.childNodes[0].hasChildNodes()) {
          return node.childNodes[0].innerHTML;
        } else {
          return node.innerHTML;
        }
      }
    }
  });
  $('abbr.timeago').timeago();
});
