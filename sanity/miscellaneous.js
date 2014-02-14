print('\nDistinct people links.url domains for manual review:');
db.people.mapReduce(function () {
  this.links.forEach(function (link) {
    emit(link.url.match('^(?:[a-z]+://)?(?:www\\.)?([^/]+)')[1], 1);
  })
}, function (key, values) {
  return Array.sum(values);
}, {out: {inline: 1}}).results.forEach(function (result) {
  print(result._id + pad.substring(0, 40 - result._id.length) + result.value);
});
