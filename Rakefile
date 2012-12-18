desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/ngrams.gob"]

file "data/synonyms.pck" => ["en"] do
	sh "mkdir -p data"
	sh "python data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" do
	sh "python data_generators/generate_anagrams.py"
end

file "data/ngrams.gob" do
	sh "go install data_gen"
	sh "data_gen"
end

file "en" do
	sh "curl -o /tmp/en.zip http://nodebox.net/code/data/media/linguistics.zip"
	sh "unzip /tmp/en.zip"
end

task :server => [:data, :go] do
	sh "python crypticweb/server.py"
end

task :test => [:data, :go] do
	sh "nosetests --nocapture"
end

task :go do
	sh "go install cryptics"
end