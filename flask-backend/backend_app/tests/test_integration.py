# Example test case
if __name__ == "__main__":
    file_to_scan = "/app/uploads/sample.exe"  # Change to test file
    result = analyze_file(file_to_scan)
    print(json.dumps(result, indent=4)) 