QA="CE";QA="${QA} IQFT";QA="${QA} BV"; python3 "Experiment_I.py";
mkdir "Experiment_I_Results";
for k in $QA; do
    cp "Experiment_I/${k}/${k}_100/0infoMutants.txt" "Experiment_I_Results/${k}_100Mutants.txt";
    cp "Experiment_I/${k}/${k}_1000/0infoMutants.txt" "Experiment_I_Results/${k}_1000Mutants.txt";
    cp "Experiment_I/${k}/${k}_10000/0infoMutants.txt" "Experiment_I_Results/${k}_10000Mutants.txt";
done;