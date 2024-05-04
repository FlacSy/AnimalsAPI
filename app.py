import os
import random
from config import ConfigManager
from quart import Quart, request, jsonify, send_from_directory

app = Quart(__name__)

config = ConfigManager()

IMAGES_FOLDER = config.get_config_value('path', 'animals')

support_animals = config.get_config_value('animals', 'support')

def get_random_image(animal):
    animal_folder = os.path.join(IMAGES_FOLDER, animal)
    images = os.listdir(animal_folder)
    random_image = random.choice(images)
    return random_image

@app.route('/random_image', methods=['GET'])
async def random_image():
    animal = request.args.get('animal')

    if animal == "":
        animal == random.choice(support_animals)

    if animal not in support_animals:
        return jsonify({'error': f'Параметр {animal} указан неверно или не существует. Список поддерживаемых параметров {support_animals}', 'status_code': 400, 'request_type': 'GET'}), 400
    
    additional_data = request.args.get('additional_data')
    
    image_name = get_random_image(animal)
    image_url = f"{request.host_url}{IMAGES_FOLDER}/{animal}/{image_name}" 
    
    response_data = {'image_url': image_url, 'status_code': 200, 'request_type': 'GET', 'requested_animal': animal}
    
    if additional_data:
        response_data['additional_data'] = additional_data
    
    status_code = request.args.get('status_code', 200)
    response_data['status_code'] = int(status_code)

    return jsonify(response_data), int(status_code)

@app.route('/animals/<animal>/<image>', methods=['GET'])
async def get_image(animal, image):
    return await send_from_directory(os.path.join(IMAGES_FOLDER, animal), image)

if __name__ == '__main__':
    app.run()