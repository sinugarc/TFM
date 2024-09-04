QA="CE";QA="${QA} IQFT";QA="${QA} BV"; mkdir "Experiment_II_Results";
python3 "Experiment_II.py" "$1";
for k in $QA; do
    cp "Experiment_II/${k}/Results_100Rep/0_results.txt" "Experiment_II_Results/${k}_100Rep.txt";
    cp "Experiment_II/${k}/Results_1024Rep/0_results.txt" "Experiment_II_Results/${k}_1024Rep.txt";
done;