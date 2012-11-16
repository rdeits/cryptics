desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/ngrams.pck"]

file "data/ngrams.pck" do
	sh "python data_generators/generate_ngrams.py"
end

file "data/synonyms.pck" do
	sh "mkdir -p data"
	sh "python data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" do
	sh "python data_generators/generate_anagrams.py"
end

task :server => [:data] do
	sh "python crypticweb/server.py"
end

task :test => [:data] do
	sh "nosetests --nocapture"
end
