from PIL import Image, ImageDraw, ImageFont
import os

def write_centered_text_on_image(input_image_path, output_image_path, text_to_write):
    # Open the image file
    img = Image.open(input_image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Choose a system font (adjust the size as needed)
    font = ImageFont.load_default(20)
    print(font.size)

    # Calculate text width and height
    # text_width, text_height = draw.textbbox((0, 0), text_to_write, font=font)
    left, top, right, bottom = draw.textbbox((0, 0), text_to_write, font=font)
    text_width = right - left
    text_height = bottom - top


    # Center the text horizontally and vertically
    # text_position = ((img.width - text_width) / 2, (img.height - text_height) / 2)
    text_position_to_inv_no = (180, 380)
    text_position_to_name = (100, 410)
    text_position_date = (658, 335)
    
    text_position_price_currency = ( 400, 620)
    text_position_price_1 = ( 400, 650)
    text_position_price_2 = ((img.width - text_width) / 2, 680)
    text_position_price_3 = ((img.width - text_width) / 2, 710)
    text_position_price_4 = ((img.width - text_width) / 2, 740)
    text_position_des_1 = (100, 650)
    text_position_des_2 = (100, 680)
    text_position_des_3 = (100, 710)
    text_position_des_4 = (100, 740)
    text_position_des_5 = (100, 770)
    text_position_qt_1 = (600, 650)
    text_position_qt_2 = (600, 680)
    text_position_qt_3 = (600, 710)
    text_position_qt_4 = (600, 740)
    text_position_qt_5 = (600, 770)
    text_position_sub_total_currancy = (680, 620)
    text_position_sub_total_1 = (680, 650)
    text_position_sub_total_2 = (680, 680)
    text_position_sub_total_3 = (680, 710)
    text_position_sub_total_4 = (680, 740)
    text_position_sub_total_5 = (680, 770)


    text_position_5 = (550, 940)
    # text_position_qt_1 = ()

    print((img.width - text_width) / 2, (img.height - text_height) / 2)
    # Choose the color of the text (white in this case)
    text_color = '#000'
    #  Create a filled rectangle with the desired background color
    bg_color = '#fff'  # Adjust the color as needed
    rectangle_width = text_width + 20  # Add some padding around the text
    rectangle_height = text_height + 10
    rectangle_position = (text_position_5[0] - 10, text_position_5[1] - 5)
    # draw.rectangle(rectangle_position + (rectangle_position[0] + rectangle_width, rectangle_position[1] + rectangle_height), fill=bg_color)

    # Write the text on the image 
    # 14 Koowulu St. Laterbiokorshie, Accra
    draw.text(text_position_to_inv_no, "1103/24-A1", font=font, fill=text_color)
    draw.text(text_position_to_name, "Mr. Kweku Amoa-Buahin ", font=font, fill=text_color)
    draw.text(text_position_date, "March 11th 2024", font=ImageFont.load_default(22), fill=text_color)

    draw.text(text_position_price_currency, "GHs", font=font, fill=text_color) 
    draw.text(text_position_sub_total_currancy, "GHs", font=font, fill=text_color)  
 
    draw.text(text_position_des_1, "Sanctuary flowers", font=font, fill=text_color)
    draw.text(text_position_price_1, "700.00", font=font, fill=text_color)
    draw.text(text_position_qt_1, "2", font=font, fill=text_color)
    draw.text(text_position_sub_total_1, "1,400.00", font=font, fill=text_color)

    draw.text(text_position_des_2, "Floral and fabric pew deco", font=font, fill=text_color)
    draw.text(text_position_price_2, "60.00", font=font, fill=text_color)
    draw.text(text_position_qt_2, "12", font=font, fill=text_color)
    draw.text(text_position_sub_total_2, "720.00", font=font, fill=text_color)

    draw.text(text_position_des_3, "Entrance flowers", font=font, fill=text_color)
    draw.text(text_position_price_3, "500.00", font=font, fill=text_color)
    draw.text(text_position_qt_3, "2", font=font, fill=text_color)
    draw.text(text_position_sub_total_3, "1,000.00", font=font, fill=text_color)

    draw.text(text_position_des_4, "Rental of stand", font=font, fill=text_color)
    draw.text(text_position_price_4, "25.00", font=font, fill=text_color)
    draw.text(text_position_qt_4, "2", font=font, fill=text_color)
    draw.text(text_position_sub_total_4, "50.00", font=font, fill=text_color)

    draw.text(text_position_des_5, "Cash discount", font=font, fill=text_color)
    draw.text(text_position_sub_total_5, "(70.00)", font=font, fill=text_color)

    draw.text(text_position_5, "GHs 3,100.00", font=ImageFont.load_default(40), fill=text_color)
    # draw.text(text_position, text_to_write, font=font, fill=text_color)

    # Save the modified image
    # img.save(output_image_path)
    img.save(output_image_path, "JPEG")


if __name__ == "__main__":
    input_image_path = "./inv001.jpg"  # Change this to the path of your input image
    output_image_path = "./inv/image_with_text.jpg"  # Change this to the desired output path
    text_to_write = "hello world"

    write_centered_text_on_image(input_image_path, output_image_path, text_to_write)
