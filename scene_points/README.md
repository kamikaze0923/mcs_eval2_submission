Usage:

```
python -m dataproj --thor PATH_TO_THOR_EXECUTABLE --data PATH_TO_SCENE_DESCS --filter SCENE_TYPE
```

This just processes each depth image + object mask from the THOR observations, uses the depth+camera info to calculate point locations, and uses the object mask+point locations to plot a 3D view of the scene.

Most of the important stuff is in data_gen.py: the relevant trig is in the px_to_pos function, everything else is just plumbing to get the input/output to the right place or in the right format.

If filter is omitted it will only process the object_permanence scenes.

Example:

```
python -m dataproj --thor ./data/thor --data ./data/thor/scenes --filter gravity
```
