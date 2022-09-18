import os 


def createAssets(paragraphs, dirr):

    for index, paragraph in enumerate(paragraphs):
        if os.name == "nt":
            command = f'magick -size 350x -font DejaVu-Sans -background none -undercolor white -gravity Center -pointsize 8 -fill black -stroke none caption:\"{paragraph}\" -bordercolor none -border 12 ^( +clone -morphology dilate disk:4 ^) +swap -composite {os.path.join(dirr, f"img{index}.png")}'
        else:
            command = f'magick -size 350x -font DejaVu-Sans -background none -undercolor white -gravity Center -pointsize 10 -fill black -stroke none caption:\"{paragraph}\" -bordercolor none -border 12 \( +clone -morphology dilate disk:5 \) +swap -composite {os.path.join(dirr, f"img{index}.png")}'

        os.system(command)          


