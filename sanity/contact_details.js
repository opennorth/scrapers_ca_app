// @todo Move into models?
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
