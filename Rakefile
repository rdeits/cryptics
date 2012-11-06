desc "Generate all data sets"
task :data => ["data/ngrams.pck", "data/synonyms.pck", "data/anagrams.pck"]

file "data/ngrams.pck" => ["data_generators/generate_ngrams.py", "load_utils.py"] do
	sh "python data_generators/generate_ngrams.py"
end

file "data/synonyms.pck" => ["data_generators/generate_synonyms.py", "load_utils.py"] do
	sh "python data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" => ["data_generators/generate_anagrams.py", "load_utils.py"] do
	sh "python data_generators/generate_anagrams.py"
end
