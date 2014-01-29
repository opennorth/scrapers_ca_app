expectNone('memberships', 'links.url');
expectNone('organizations', 'links.url');
expectNone('memberships', 'links.note');
expectNone('organizations', 'links.note');

matches('people', 'links.note', {
  'links.note': {
    $ne: null,
  },
});

matches('people', 'links.url', {
  $where: function () {
    var count = 0;
    for (var i = 0, l = this.links.length; i < l; i++) {
      if (!/facebook\.com/.test(this.links[i].url) && !/twitter\.com/.test(this.links[i].url) && !/youtube\.com/.test(this.links[i].url)) {
        count += 1;
      }
      if (count > 1) {
        return true;
      }
    }
  },
}, 'people: multiple links with a non-social media url');

matches('people', 'links.url', {
  $where: function () {
    var urls = [/facebook\.com/, /twitter\.com/, /youtube\.com/];
    for (var j = 0, m = urls.length; j < m; j++) {
      var count = 0;
      for (var i = 0, l = this.links.length; i < l; i++) {
        if (urls[j].test(this.links[i].url)) {
          count += 1;
        }
        if (count > 1) {
          return true;
        }
      }
    }
  },
}, 'people: multiple links with the same social media url');

// print('\nDistinct people links.url domains for manual review:');
// mapReduce('people', function () {
//   this.links.forEach(function (link) {
//     emit(link.url.match('^(?:[a-z]+://)?(?:www\\.)?([^/]+)')[1], 1);
//   })
// });
