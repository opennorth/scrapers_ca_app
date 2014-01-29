require 'csv'
require 'open-uri'

def escape(header)
  header.downcase.gsub(' ', '_')
end

headers = ['Leader', 'Member', 'Member At Large']

File.open('styles.js', 'w') do |f|
  f.write "var styles = {}\n"

  [0, 1].each do |gid|
    CSV.parse(open("https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdFJrVTdaV1h5XzRpTkxBdVROX3FNelE&single=true&gid=#{gid}&output=csv"), headers: true) do |row|
      if headers.any?{|header| row[header]}
        f.write "styles['#{row['Identifier']}'] = []\n"
        headers.each do |header|
          f.write %(styles['#{row['Identifier']}'].push("#{row[header]}")\n) if row[header]
        end
      end
    end
  end
end
