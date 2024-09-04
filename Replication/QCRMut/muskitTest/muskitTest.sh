QA="CE";QA="${QA} IQFT";QA="${QA} BV"; QF="${QA} QRAM";
python3 "muskitAdapt.py"; mkdir "Errors"; mkdir "Results";
for k in $QF; do
    for f in "${k}/${k}MutantsAdapted"/*.py; do
	python3 "$f" >> "Errors/${k}.txt" 2>&1
    done;
done;
for k in $QA; do
    mkdir "Results/$k"
done;
python3 "execution.py";
for k in $QA; do
    cp "Results/${k}/Results_100Rep/0_results.txt" "Results/${k}_100Rep";
done;
cp "Results/IQFT/Results_1024Rep/0_results.txt" "Results/IQFT_1024Rep";