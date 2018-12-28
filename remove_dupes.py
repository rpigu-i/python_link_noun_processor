with open('combined_output.txt') as f:
    unique_links = set()
    for line in f:
        line_lower = line.lower()
        unique_links.add(line_lower)
    with open('research_data.txt', 'w') as r:
        for link in unique_links:
            r.write(link)
