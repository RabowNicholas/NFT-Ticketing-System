from PIL import Image
import random
import json


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

overlay = ["base","silver","gold", "holofoil"]
overlay_weights = [100, 120, 130, 131]
logo = ["current", "city", "96"]
logo_weights = [100, 110, 111]
player = ["Mitchell", "Gobert", "Clarkson", "Conley", "O'Neale", "Stockton", "Malone"]
player_weights = [5, 10, 15, 20, 25, 26, 27 ]

#Generate traits

total_images = 50
all_images = []

def create_new_image():
    new_image = {}

    #For each trait category, select a random trait based on the ratings
    new_image["overlay"] = random.choices(overlay, cum_weights=overlay_weights, k=1)[0]
    new_image["logo"] = random.choices(logo, cum_weights=logo_weights, k=1)[0]
    new_image["player"] = random.choices(player, cum_weights=player_weights, k=1)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image

#Generate the unique combinations based on trait weightings
for i in range(total_images):
    new_trait_image = create_new_image()

    all_images.append(new_trait_image)

def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

#Add token id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i += 1


#Get Trait Counts

overlay_count = {}
for item in overlay:
    overlay_count[item] = 0

logo_count = {}
for item in logo:
    logo_count[item] = 0

player_count = {}
for item in player:
    player_count[item] = 0

for image in all_images:
    overlay_count[image["overlay"]] += 1
    logo_count[image["logo"]] += 1
    player_count[image["player"]] += 1

print(overlay_count)
print(logo_count)
print(player_count)

#Generate metadata for all traits
metadata_file_name = "./Nft_example/metadata/all-traits.json"
with open(metadata_file_name, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

#generate images
for item in all_images:
    background = Image.open('./Nft_example/traits/base.png')
    im1 = Image.open(f'./Nft_example/traits/{item["overlay"]}.png').convert('RGBA')
    im2 = Image.open(f'./Nft_example/traits/{item["logo"]}.png').convert('RGBA')
    im3 = Image.open(f'./Nft_example/traits/{item["player"]}.png').convert('RGBA')

    com1 = Image.alpha_composite(background, im2)
    com2 = Image.alpha_composite(com1, im3)
    if item["overlay"] != "base":
        com2 = Image.blend(com2, im1,0.5)

    rgb_im = com2.convert('RGB')
    file_name = str(item["tokenId"])
    rgb_im.save("./Nft_example/images/" + file_name + '.png')

#### Generate Metadata for each Image

f = open('./Nft_example/metadata/all-traits.json',)
data = json.load(f)

# Changes this IMAGES_BASE_URL to yours
IMAGES_BASE_URL = "https://gateway.pinata.cloud/ipfs/Qmb86L8mUphwJGzLPwXNTRiK1S4scBdj9cc2Sev3s8uLiB/"
PROJECT_NAME = "Jazz_ticket"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URL + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("overlay", i["overlay"]))
    token["attributes"].append(getAttribute("logo", i["logo"]))
    token["attributes"].append(getAttribute("player", i["player"]))

    with open('./Nft_example/metadata/' + str(token_id) + ".json", 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()
