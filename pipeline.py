import Utils
from inference import inference

output_dir = "./Discac"
"""input_filename = "./Discac/DISCAC-Tarif-Cuisines-24-25.pdf"
output_dir = "./Discac"
pages_per_chunk = 50 # Adjust this to your desired chunk size

Utils.split_pdf(input_filename, output_dir+"/PDFChunks", pages_per_chunk)

Utils.pdftoImages(output_dir+"/PDFChunks",output_dir+"/images")
"""


listofdir=Utils.get_all_dirs_paths(output_dir+"/images")

for dir in listofdir:
    foldername=dir.split("\\")[-1]
    print(foldername)
    ListOfImages=Utils.deep_search_file_type(dir,".jpg")
    for image in ListOfImages:
        result = inference(image)
        Utils.draw_rectangles(image, result, output_dir+"/output/"+foldername)
