#!/bin/bash -x

wget https://evaluation2-training-scenes.s3.amazonaws.com/interaction-scenes.zip
wget https://evaluation2-training-scenes.s3.amazonaws.com/intphys-scenes.zip

unzip interaction-scenes.zip
unzip intphys-scenes.zip -d intphys_scenes

mkdir intphys_scenes/gravity
mkdir intphys_scenes/object_permanence
mkdir intphys_scenes/shape_constancy
mkdir intphys_scenes/spatio_temporal_continuity

mkdir interaction_scenes/retrieval
mkdir interaction_scenes/traversal
mkdir interaction_scenes/transferral

mv intphys_scenes/gravity*.json intphys_scenes/gravity
mv intphys_scenes/object_permanence*.json intphys_scenes/object_permanence
mv intphys_scenes/shape_constancy*.json intphys_scenes/shape_constancy
mv intphys_scenes/spatio_temporal_continuity*.json intphys_scenes/spatio_temporal_continuity

mv interaction_scenes/retrieval*.json interaction_scenes/retrieval
mv interaction_scenes/traversal*.json interaction_scenes/traversal
mv interaction_scenes/transferral*.json interaction_scenes/transferral

rm interaction-scenes.zip
rm intphys-scenes.zip
