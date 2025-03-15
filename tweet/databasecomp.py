def compare_license_plates(file_path):
    license_plates = []  
    try:
        with open(file_path, 'r') as file:
            for line in file:
                
                line = line.strip()
                if line:  
                    parts = line.split()
                    if len(parts) > 0:
                        license_plate = parts[0]
                        license_plates.append(license_plate)  
        return license_plates  
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")






