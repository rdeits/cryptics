desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/clue_structures.pck", "data/ngrams.gob"]

file "data/synonyms.pck" do
	sh "mkdir -p data"
	sh "python data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" do
	sh "python data_generators/generate_anagrams.py"
end

file "data/ngrams.gob" => [:go] do
	sh "data_gen"
end

file "data/clue_structures.pck" do
	sh "python data_generators/generate_clues.py"
end

task :server => [:go] do
	sh "python crypticweb/server.py"
end

task :test => [:data, :go] do
	sh "nosetests --nocapture"
end

task :go do
	sh "go install cryptics"
	sh "go install data_gen"
end