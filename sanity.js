var pad = '                                        ';

var expect = function (actual, expected, message) {
  if (expected != actual) {
    print(message + ': ' + actual + ' (expected: ' + expected + ')');
  }
};

var expectNone = function (collection, field) {
  var selector = {};
  selector[field] = {$exists: true};
  expect(db[collection].count(selector), 0, collection + ' ' + field + ' count');
};

var mapReduce = function (collection, map) {
  db[collection].mapReduce(map, function (key, values) {
    return Array.sum(values);
  }, {out: {inline: 1}}).results.forEach(function (result) {
    print(result._id + pad.substring(0, 40 - result._id.length) + result.value);
  });
}

// Finds documents in the given collection matching the given criteria. If any
// documents are found, prints the given message and, for each document, prints
// its ID and the value of the given field.
var matches = function (collection, field, criteria, message) {
  message = message || collection + ' with invalid ' + field;

  var count = db[collection].count(criteria);
  if (count) {
    print('\n' + message + ':');
    db[collection].find(criteria).forEach(function (obj) {
      if (field.indexOf('.') === -1) {
        print(obj._id + ': ' + obj[field]);
      }
      else {
        print(obj._id);
      }
    });
  }
};

// Contact details

expectNone('people', 'contact_details.type');
expectNone('organizations', 'contact_details.type');
expectNone('people', 'contact_details.note');
expectNone('organizations', 'contact_details.note');

matches('memberships', 'jurisdiction_id', {
  contact_details: {
    $elemMatch: {
      type: {$nin: ['address', 'cell', 'email', 'fax', 'voice']},
    },
  },
}, 'memberships: unexpected contact_details.type');

matches('memberships', 'jurisdiction_id', {
  contact_details: {
    $elemMatch: {
      type: {$ne: 'email'},
      note: {$nin: ['constituency', 'legislature', 'residence']},
    },
  },
}, 'memberships: unexpected contact_details.note');

matches('memberships', 'jurisdiction_id', {
  contact_details: {
    $elemMatch: {
      type: 'email',
      note: {$ne: null},
    },
  },
}, 'memberships: email with non-empty note');

matches('memberships', 'jurisdiction_id', {
  contact_details: {
    $elemMatch: {
      type: {$ne: 'email'},
      note: null,
    },
  },
}, 'memberships: non-email with empty note');

// Links

matches('people', 'jurisdiction_id', {
  'links.note': {
    $ne: null,
  },
});
// print('\nDistinct people links.url domains for manual review:');
// mapReduce('people', function () {
//   this.links.forEach(function (link) {
//     emit(link.url.match('^(?:[a-z]+://)?(?:www\\.)?([^/]+)')[1], 1);
//   })
// });
expectNone('memberships', 'links.url');
expectNone('organizations', 'links.url');
expectNone('memberships', 'links.note');
expectNone('organizations', 'links.note');

// print('\nDistinct memberships post_id for manual review:');
// mapReduce('memberships', function () {
//   if (this.post_id) {
//     emit(this.post_id, 1);
//   }
// });
