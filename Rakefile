desc "Generate all data sets"
task :data => ["data/kinds.pck", "data/ngrams.pck", "data/synonyms.pck", "data/anagrams.pck"]

file "data/ngrams.pck" => ["data_generators/generate_ngrams.py", "utils/ngrams.py"] do
	sh "python data_generators/generate_ngrams.py"
end

file "data/synonyms.pck" => ["data_generators/generate_synonyms.py", "utils/synonyms.py"] do
	sh "python data_generators/generate_synonyms.py"
end

file "data/anagrams.pck" => ["data_generators/generate_anagrams.py", "utils/anagrams.py"] do
	sh "python data_generators/generate_anagrams.py"
end

file "data/kinds.pck" => ["data_generators/generate_kinds.py", "utils/kinds.py"] do
	sh "python data_generators/generate_kinds.py"
end
