desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/ngrams.gob"]

file "data/synonyms.pck" => ["python/en"] do
	sh "mkdir -p data"
	sh "python python/data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" do
	sh "python python/data_generators/generate_anagrams.py"
end

file "data/ngrams.gob" do
	sh "go install data_gen"
	sh "data_gen"
end

file "python/en" do
	sh "curl -o /tmp/en.zip http://nodebox.net/code/data/media/linguistics.zip"
	sh "cd python"
	sh "unzip /tmp/en.zip"
	sh "cd .."
end

task :server => [:data, :go] do
	sh "python python/crypticweb/server.py"
end

task :test => [:data, :go] do
	sh "nosetests --nocapture python"
end

task :go do
	sh "go install cryptics"
end

task :puz => [:data, :go] do
	sh "python python/solve_puz.py /Users/rdeits/downloads/rss0112.puz"
end
