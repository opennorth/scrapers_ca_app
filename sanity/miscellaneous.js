print('\nDistinct memberships post_id for manual review:');
var post_ids = {};
db.memberships.find().forEach(function (membership) {
  if (membership.post_id) {
    // @todo Remove the if-statement once we want to import the "municipalities" scrapers.
    if (!/\/municipalities$/.test(membership.jurisdiction_id)) {
      var division_id = division_id_from_jurisdiction_id(membership.jurisdiction_id);
      if (posts[division_id]) {
        if (posts[division_id].indexOf(membership.post_id) === -1) {
          post_ids[membership.post_id] = division_id;
        }
      }
      else if (uniqueRoles.indexOf(membership.role) === -1) {
        post_ids[membership.post_id] = (post_ids[membership.post_id] || 0) + 1;
      }
      else if (styles[division_id] && styles[division_id].indexOf(membership.role) === -1) {
        post_ids[membership.post_id] = membership.role;
      }
      else if (membership.post_id !== names[division_id]) {
        post_ids[membership.post_id] = names[division_id];
      }
    }
  }
});

pad = '                                                  ';

var keys = Object.keys(post_ids);
keys.sort();
keys.forEach(function (post_id) {
  print('"' + post_id + '"' + pad.substring(0, 50 - post_id.length) + post_ids[post_id]);
});
