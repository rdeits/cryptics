desc "Generate all data sets"
task :data => ["data/synonyms.pck", "data/ngrams.pck"]

file "data/synonyms.pck" => ["en/__init__.py"] do
	sh "mkdir -p data"
	sh "python pycryptics/data_generators/generate_synonyms.py"
end

file "data/ngrams.pck" do
	sh "python pycryptics/data_generators/generate_ngrams.py"
end

file "en/__init__.py" do
	sh "curl -o /tmp/en.zip http://nodebox.net/code/data/media/linguistics.zip"
	sh "unzip /tmp/en.zip"
end

task :server => [:data] do
	sh "python pycryptics/crypticweb/server.py"
end

task :test => [:data] do
	sh "nosetests --nocapture pycryptics"
end

# task :go do
# 	sh "go install cryptics"
# end

task :puz => [:data] do
	sh "python pycryptics/solve_puz.py sample_puzzles/kegler_cryptic_1.puz"
end

task :download_corpus do
	if ENV['OS'] == 'Windows_NT'
		sh "python -m nltk.downloader -d C:\\nltk_data wordnet"
	else
		sh "sudo python -m nltk.downloader -d /usr/share/nltk_data wordnet"
	end
end

task :download => [:download_corpus, "en/__init__.py"]

