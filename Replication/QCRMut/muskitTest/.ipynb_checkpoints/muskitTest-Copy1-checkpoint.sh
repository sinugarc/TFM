QA="CE";QA="${QA} IQFT"
for k in $QA; do
    cp "Results/${k}/Results_100Rep/0_results.txt" "Results/${k}_100Rep";
    cp "Results/${k}/Results_1024Rep/0_results.txt" "Results/${k}_1024Rep";
done;