from machine_common_sense.mcs import MCS

controller = MCS.create_controller('./unity_app/MCS-AI2-THOR-Unity-App-v0.0.10.x86_64')

config_file_path = 'interaction_scenes/retrieval/retrieval_goal-0001.json'

config_data, status = MCS.load_config_json_file(config_file_path)

config_file_name = config_file_path[config_file_path.rfind('/')+1:]

if 'name' not in config_data.keys():

    config_data['name'] = config_file_name[0:config_file_name.find('.')]

output = controller.start_scene(config_data)

for i in range(1, 12):

    output = controller.step('RotateLook', rotation=30)

    for j in range(len(output.image_list)):

        output.image_list[j].save(f'{i}-{j}.jpg')
