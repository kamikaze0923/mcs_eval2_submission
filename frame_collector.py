import os

class Frame_collector:

    def __init__(self, scene_dir, start_scene_number):
        self.scene_dir = scene_dir
        self.scene_number = start_scene_number
        self.step = 0
        os.makedirs(self.scene_dir, exist_ok=True)

    def save_frame(self, step_output):
        print("Save Image!")
        for j in range(len(step_output.image_list)):
            step_output.image_list[j].save(f'{self.scene_dir}/original_{self.scene_number}-{self.step}-{j}.jpg')
            step_output.object_mask_list[j].save(f'{self.scene_dir}/mask_{self.scene_number}-{self.step}-{j}.jpg')
        self.step += 1

    def reset(self):
        self.scene_number += 1
        self.step = 0
        print("Reset, Current Scene: {}".format(self.scene_number))