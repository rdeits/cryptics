desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/ngrams.pck"]

file "data/synonyms.pck" => ["en/__init__.py"] do
	sh "mkdir -p data"
	sh "python pycryptics/data_generators/generate_synonyms.py"
end

file "data/ngrams.gob" do
	sh "go install data_gen"
	sh "data_gen"
end

file "data/ngrams.pck" do
	sh "python pycryptics/data_generators/generate_ngrams.py"
end

file "en/__init__.py" do
	sh "curl -o /tmp/en.zip http://nodebox.net/code/data/media/linguistics.zip"
	sh "unzip /tmp/en.zip"
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
