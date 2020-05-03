# !/bin/bash
Name_vec="output_good"
Number_good=300
Number_bad=500

Name_good_description="/Users/antonivanov/Downloads/Open_CV/Version_1/Good_desc.dat"
Name_bad_description="/Users/antonivanov/Downloads/Open_CV/Version_1/Bad_desc.dat"
Width_image=241
Height_image=241

Name_folder_data="data"
Num_stages=10
Num_memory=256

mkdir $Name_folder_data

opencv_createsamples \
-vec $Name_vec \
-info $Name_good_description \
-w $Width_image \
-h $Height_image

echo hi


#echo $Name_vec $Name_bad_description $Num_stages
#echo $Number_good $Number_bad $Width_image $Height_image $Num_memory

opencv_traincascade \
-data $Name_folder_data \
-vec $Name_vec \
-bg $Name_bad_description \
-numStages $Num_Stages \
-minhitrate 0.990 \
-maxFalseAlarmRate 0.5 \
-numPos $Number_good \
-numNeg $Number_bad  \
-w $Width_image \
-h $Height_image \
-featureType HAAR \
-mode ALL \
-precalcValBufSize $Num_memory \
-precalcIdxBufSize $Num_memory \



