def compare_license_plates(file_path):
    """
    Reads license plates from a file and returns them as a list.
    """
    license_plates = []  # List to store the license plates
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split()
                    if len(parts) > 0:
                        license_plate = parts[0]
                        license_plates.append(license_plate)  # Add license plate to the list
        return license_plates  # Return the list of license plates
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage (provide the path to your file)
# plates = compare_license_plates('home/car_plate_data.txt')
# print(plates)  # This will print the list of license plates




