require 'csv'
require 'open-uri'

File.open('constants.py', 'w') do |f|
  f.write "names = {}\n"
  f.write "posts = {}\n"
  f.write "styles = {}\n"

  %w(ca_provinces_and_territories ca_census_divisions ca_census_subdivisions).each do |filename|
    CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv")) do |row|
      f.write %(names['#{row[0]}'] = "#{row[1]}"\n)
    end
  end

  %w(pe ns nb qc on mb sk ab bc).each do |type_id|
    f.write %(posts['ocd-division/country:ca/province:#{type_id}'] = []\n)
    CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/province-#{type_id}-electoral_districts.csv")) do |row|
      f.write %(posts['ocd-division/country:ca/province:#{type_id}'].append("#{row[1]}")\n)
    end
  end

  CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv')) do |row|
    f.write %(posts['#{row[0]}'] = ["#{row[1]}"]\n)
  end

  CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_municipal_subdivisions.csv')) do |row|
    identifier, _, pair = row[0].rpartition('/')
    f.write %(posts['#{identifier}'].append("#{row[1]}")\n)
    if pair[/:\d+\z/]
      alternative_name = pair.capitalize.sub(':', ' ')
      f.write %(posts['#{identifier}'].append("#{alternative_name}")\n) unless row[1] == alternative_name
    end
  end

  headers = ['Leader', 'Member', 'Member At Large']

  [0, 1].each do |gid|
    CSV.parse(open("https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdFJrVTdaV1h5XzRpTkxBdVROX3FNelE&single=true&gid=#{gid}&output=csv"), headers: true) do |row|
      if headers.any?{|header| row[header]}
        f.write "styles['#{row['Identifier']}'] = []\n"
        headers.each do |header|
          f.write %(styles['#{row['Identifier']}'].append("#{row[header]}")\n) if row[header]
        end
      end
    end
  end
end
