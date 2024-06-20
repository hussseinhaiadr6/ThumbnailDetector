import os
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
poppler_path = "./poppler/poppler-24.02.0/Library/bin"

import cv2
def split_pdf(input_filename, output_dir, pages_per_chunk):
  """
  Splits a PDF file into chunks of a specified number of pages.

  Args:
      input_filename (str): Path to the input PDF file.
      output_dir (str): Path to the directory where the split PDFs will be saved.
      pages_per_chunk (int): The number of pages per chunk.
  """

  # Ensure output directory exists
  os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

  with open(input_filename, 'rb') as input_file:
    pdf_reader = PdfReader(input_file)
    num_pages = len(pdf_reader.pages)


    # Calculate the total number of chunks
    num_chunks = num_pages // pages_per_chunk + (num_pages % pages_per_chunk > 0)

    for chunk_number in range(num_chunks):
      start_page = chunk_number * pages_per_chunk
      end_page = min(start_page + pages_per_chunk, num_pages)  # Handle last chunk

      pdf_writer = PdfWriter()
      for page_num in range(start_page, end_page):
        pdf_writer.add_page(pdf_reader.pages[page_num])

      output_filename = os.path.join(output_dir, f"chunk_{chunk_number+1}.pdf")  # 1-based indexing
      with open(output_filename, 'wb') as output_file:
        pdf_writer.write(output_file)

  print(f"PDF split into {num_chunks} chunks in directory: {output_dir}")


def pdftoImages(Source_dir, Save_folder="./"):
    os.makedirs(Save_folder, exist_ok=True)  # Create directory if it doesn't exist
    try:
        for root, dirs, files in os.walk(Source_dir):
            for filename in files:
                if filename.endswith(".pdf"):
                    os.mkdir(Save_folder + "/" + filename.split('.')[0])
                    print(filename)
                    images = convert_from_path(root+"/"+filename, poppler_path=poppler_path)
                    for i in range(len(images)):

                        images[i].save(Save_folder+'/'+filename.split('.')[0]+'/page' + str(i + 1) + '.jpg', 'JPEG')

    except FileNotFoundError:
        print("ERROR: Create a folder Called Images to continue in Task 1 Directory")

def get_all_file_paths(directory):
  file_paths = []
  for filename in os.listdir(directory):
    # Construct the full path by joining the directory path and filename
    full_path = os.path.join(directory, filename)

    # Check if it's a file (not a directory) using os.path.isfile
    if os.path.isfile(full_path):
      file_paths.append(full_path)

  return file_paths




def get_all_dirs_paths(directory):
  dir_paths = []
  for filename in os.listdir(directory):
    # Construct the full path by joining the directory path and filename
    full_path = os.path.join(directory, filename)

    # Check if it's a file (not a directory) using os.path.isfile
    if os.path.isdir(full_path):
      dir_paths.append(full_path)

  return dir_paths




def deep_search_file_type(Source_dir, extension):
  list_of_files=[]
  for root, dirs, files in os.walk(Source_dir):
    for filename in files:
      if filename.endswith(extension):
        list_of_files.append(root+"/"+filename)
  return list_of_files



def draw_rectangles(image_dir, results,output, color=(0, 255, 0), thickness=2):
  """
  Draws rectangles on an image using a list of xyxy coordinates.

  Args:
      image: The image on which to draw the rectangles (NumPy array).
      xyxy_list: A list of lists, where each inner list represents the
                 coordinates of a bounding box in xyxy format: [x_min, y_min, x_max, y_max].
      color: The color of the rectangle (BGR format, default is green).
      thickness: The thickness of the rectangle lines (default is 2).

  Returns:
      The modified image with rectangles drawn on it (NumPy array).
  """
  filename=image_dir.split("/")[-1].split(".")[0]
  print(filename)
  os.makedirs(output+"/"+filename)
  output= output + "/" + filename
  image = cv2.imread(image_dir)
  xyxy_list = results[0].boxes.xyxy  # Example bounding boxes
  i=0
  # Loop through each bounding box in the list
  for box in xyxy_list:
    i=i+1
    x_min, y_min, x_max, y_max = box

    # Ensure coordinates are within image bounds (avoid potential errors)
    x_min = int(max(0, x_min))  # Clamp x_min to 0 to avoid going outside the image
    y_min = int(max(0, y_min))  # Clamp y_min to 0 to avoid going outside the image
    x_max = int(min(image.shape[1] - 1, x_max))  # Clamp x_max to image width - 1
    y_max = int(min(image.shape[0] - 1, y_max))  # Clamp y_max to image height - 1
    cv2.imwrite(output+"/"+str(i)+".jpg", image[y_min:y_max, x_min:x_max])
    cropped_image = image[y_min:y_max, x_min:x_max]
    cv2.imwrite(f"{output}/{i}.jpg", cropped_image)
    # Draw the rectangle
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
  cv2.imwrite( f"{output}/final.jpg", image)