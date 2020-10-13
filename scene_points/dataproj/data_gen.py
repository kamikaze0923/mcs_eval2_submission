import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Image -> Point cloud conversion
"""

def convert_scenes(env, paths):
    for scene_idx, scene_path in enumerate(paths):
        for frame_idx, obs in enumerate(env.run_scene(scene_path)):
            pts, obj_mask = convert_output(obs)
            plot_scene(scene_idx, frame_idx, pts, obj_mask)


def convert_output(o):
    objs = o.object_list
    structs = o.structural_object_list
    img = o.image_list[-1]
    obj_mask = convert_obj_mask(o.object_mask_list[-1], objs).flatten()
    depth_mask = np.array(o.depth_mask_list[-1])
    camera_desc = [o.camera_aspect_ratio, o.camera_clipping_planes,
                   o.camera_field_of_view, o.position]
    pts = convert_depth_mask(depth_mask, *camera_desc)
    return pts, obj_mask


def convert_obj_mask(mask, objs):
    col_to_tuple = lambda col: (col['r'], col['g'], col['b'])
    color_map = {col_to_tuple(o.color):i for i, o in enumerate(objs)}
    arr_mask = np.array(mask)
    out_mask = -np.ones(arr_mask.shape[0:2], dtype=np.int8)
    for x in range(arr_mask.shape[0]):
        for y in range(arr_mask.shape[1]):
            idx = color_map.get(tuple(arr_mask[x, y]), -1)
            out_mask[x, y] = idx
    return out_mask


def convert_depth_mask(depth, camera_aspect_ratio, camera_clipping_planes,
                       camera_field_of_view, position):
    sz = depth.shape
    px_grid = np.stack(np.meshgrid(np.arange(sz[1]), np.arange(sz[0])), axis=-1)
    world_pos = px_to_pos(px_grid, depth, camera_aspect_ratio,
                          camera_clipping_planes, camera_field_of_view,
                          position)
    pts = world_pos.reshape(-1, world_pos.shape[-1])
    return pts


def px_to_pos(px_arr, depth_arr, aspect_ratio, clip_planes, fov_deg, camera_pos):
    uv_arr = px_arr*[2/w for w in aspect_ratio]-1
    uv_arr[:, :, 1] *= -1
    depth_mix = depth_arr/255
    depth = clip_planes[0] + (clip_planes[1]-clip_planes[0])*depth_mix
    vfov = np.radians(fov_deg)
    hfov = np.radians(fov_deg*aspect_ratio[0]/aspect_ratio[1])
    tans = np.array([np.tan(x/2) for x in (hfov, vfov)])
    dir_arr = uv_arr * tans
    zs = np.ones((dir_arr.shape[0:2])+(1,))
    dir_arr = np.concatenate((dir_arr, zs), axis=-1)
    camera_offsets = dir_arr * np.expand_dims(depth, axis=-1)
    pos_to_list = lambda x: [x['x'], x['y'], x['z']]
    return camera_offsets + pos_to_list(camera_pos)


"""
Plotting
"""

def plot_pts(ax, pts):
    ax.scatter(*zip(*pts), zdir='y', s=0.1, alpha=0.5)

def plot_scene(scene_idx, frame_idx, pts, obj_mask):
    fig = plt.figure(figsize=(10, 10), dpi=100)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    for obj_id in np.unique(obj_mask):
        print(obj_id)
        obj_pts = pts[obj_mask==obj_id]
        plot_pts(ax, obj_pts)
    bound = 8
    ax.set_xlim([-bound/2, bound/2])
    ax.set_ylim([0, bound])
    ax.set_zlim([0, bound])
    fig.savefig(f'{scene_idx}_{frame_idx}_points.png')
    plt.close(fig)
