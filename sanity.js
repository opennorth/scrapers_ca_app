var pad = '                                        ';

var expect = function (actual, expected, message) {
  if (toString.call(expected) === '[object Array]') {
    if (expected.indexOf(actual) === -1) {
      print(message + ': ' + actual + ' (expected in [' + expected + '])');
    }
  }
  else if (expected !== actual) {
    print(message + ': ' + actual + ' (expected == ' + expected + ')');
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



// Role

// @todo Check that the hardcoded roles in scrapers-ca are correct.

roles = [
  // Provincial
  'MLA',
  // Municipal
  'Alderman',
  'City Councillor',
  'Councillor',
  'Regional Councillor',
]

uniqueRoles = [
  // Municipal
  'Acting Chief Administrative Officer',
  'Chairperson',
  'Chief Administrative Officer',
  'Chief Executive Officer',
  'City Manager',
  'Mayor', 'Deputy Mayor',
  'Municipal Administrator',
  'Reeve', 'Deputy Reeve',
  'Warden', 'Deputy Warden',
]

matches('memberships', 'role', {
  role: {$nin: roles.concat(uniqueRoles)},
});

// db.memberships.ensureIndex({organization_id: 1, role: 1})
print('\nOrganizations without any unique roles:');
db.organizations.find().forEach(function (organization) {
  if (!/\/legislature$/.test(organization.jurisdiction_id)) {
    expect(db.memberships.count({organization_id: organization._id, role: {$in: uniqueRoles}}), [1, 2],
      [organization.jurisdiction_id, organization._id].join(' '));
  }
});

print('\nOrganizations with multiple unique roles:');
db.organizations.find().forEach(function (organization) {
  uniqueRoles.forEach(function (role) {
    expect(db.memberships.count({organization_id: organization._id, role: role}), [0, 1],
      [organization.jurisdiction_id, organization._id, role].join(' '));
  });
});



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
      note: {$nin: ['constituency', 'legislature', 'office', 'residence', null]},
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

matches('memberships', 'jurisdiction_id', {
  $where: function () {
    var count = 0;
    for (var i = 0, l = this.contact_details.length; i < l; i++) {
      if (this.contact_details[i].type === 'email') {
        count += 1;
      }
      if (count > 1) {
        return true;
      }
    }
  },
}, 'memberships: multiple contact_details with the same type: email');

matches('memberships', 'jurisdiction_id', {
  $where: function () {
    var types = ['address', 'cell', 'fax', 'voice'];
    var notes = ['constituency', 'legislature', 'residence'];
    for (var k = 0, n = types.length; k < n; k++) {
      for (var j = 0, m = notes.length; j < m; j++) {
        var count = 0;
        for (var i = 0, l = this.contact_details.length; i < l; i++) {
          var contact_detail = this.contact_details[i];
          if (contact_detail.type === types[k] && contact_detail.note === notes[j]) {
            count += 1;
          }
          if (count > 1) {
            return true;
          }
        }
      }
    }
  },
}, 'memberships: multiple contact_details with the same type and note');



// Links

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



// Relationships

var pad = '                                                                                                         ';

print('\nJurisdictions without exactly one organization:');
db.organizations.distinct('jurisdiction_id').forEach(function (jurisdiction_id) {
  if (!/\/municipalities$/.test(jurisdiction_id)) {
    expect(db.organizations.count({jurisdiction_id: jurisdiction_id}), 1, jurisdiction_id);
  }
});

// db.memberships.ensureIndex({person_id: 1})
print('\nPeople without exactly one membership:');
db.people.find().forEach(function (person) {
  expect(db.memberships.count({person_id: person._id}), 1, person._id + ' memberships: ' + person.sources[0].url);
});



// Miscellaneous

print('\nDistinct memberships post_id for manual review:');
mapReduce('memberships', function () {
  if (this.post_id) {
    emit(this.post_id, 1);
  }
});
