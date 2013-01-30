desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/ngrams.gob"]

file "data/synonyms.pck" => ["pycryptics/en"] do
	sh "mkdir -p data"
	sh "python pycryptics/data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" do
	sh "python pycryptics/data_generators/generate_anagrams.py"
end

file "data/ngrams.gob" do
	sh "go install data_gen"
	sh "data_gen"
end

file "pycryptics/en" do
	sh "curl -o /tmp/en.zip http://nodebox.net/code/data/media/linguistics.zip"
	sh "cd pycryptics"
	sh "unzip /tmp/en.zip"
	sh "cd .."
end

task :server => [:data, :go] do
	sh "python pycryptics/crypticweb/server.py"
end

task :test => [:data, :go] do
	sh "nosetests --nocapture pycryptics"
end

task :go do
	sh "go install cryptics"
end

task :puz => [:data, :go] do
	sh "python pycryptics/solve_puz.py sample_puzzles/kegler_cryptic_1.puz"
end
