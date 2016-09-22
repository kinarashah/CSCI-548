# Move to example directory of crfsuite-0.12 by using cd
# Just for example, 
#cd crfsuite-0.12/example
mkdir -p results 

# Next, change chunking.py to include more features/attributes 
# Updated file can be found in source folder 

cat training.txt | ./chunking.py > train.crfsuite.txt
crfsuite learn -m crf.model train.crfsuite.txt > results/train_details.txt

cat testing_high.txt | ./chunking.py > test1.crfsuite.txt
crfsuite tag -qt -m crf.model test1.crfsuite.txt > results/test1_details.txt 

cat testing_low.txt | ./chunking.py > test2.crfsuite.txt
crfsuite tag -qt -m crf.model test2.crfsuite.txt > results/test2_details.txt 

cat testing_high.txt testing_low.txt > testing_combined.txt
cp testing_combined.txt ../testing/

cat testing_combined.txt | ./chunking.py > testc.crfsuite.txt
crfsuite tag -qt -m crf.model testc.crfsuite.txt > results/test_combined_details.txt 

# optional
crfsuite dump crf.model > results/crf.model.txt
