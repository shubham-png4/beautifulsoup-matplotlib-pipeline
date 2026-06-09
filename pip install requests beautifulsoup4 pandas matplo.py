!pip install requests beautifulsoup4 pandas matplotlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def scrape_jobs():
    # 1. Fetch the website content
    url = "https://realpython.github.io/fake-jobs/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print({"status": "Connecting to website...", "url": url})
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve data. Status Code: {response.status_code}")
        return None

    # 2. Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the main container holding all the job postings
    results_container = soup.find(id="ResultsContainer")
    job_cards = results_container.find_all("div", class_="card-content")

    jobs_data = []

    # 3. Extract specific text strings from elements
    for card in job_cards:
        title_element = card.find("h2", class_="title")
        company_element = card.find("h3", class_="company")
        location_element = card.find("p", class_="location")

        # Clean up whitespace out of the parsed text strings
        title = title_element.text.strip()
        company = company_element.text.strip()
        location = location_element.text.strip()

        # Structure parsed records into a dictionary collection
        jobs_data.append({
            "Job Title": title,
            "Company": company,
            "Location": location
        })

    print(f"✅ Successfully scraped {len(jobs_data)} job postings.")
    return jobs_data

def visualize_data(jobs_list):
    # 4. Convert structural records directly into a Pandas DataFrame
    df = pd.DataFrame(jobs_list)

    print("\n--- First 5 Rows of Scraped Data ---")
    print(df.head())

    # Let's clean the location data to get just the city name
    # (The site formats locations as "City, State" or "City, Country")
    df['City'] = df['Location'].apply(lambda x: x.split(',')[0].strip())

    # Count the distribution occurrences of jobs across cities
    city_counts = df['City'].value_counts().head(10) # Grab the top 10 cities

    # 5. Data Visualization using Matplotlib
    plt.figure(figsize=(10, 6))

    # Create a horizontal bar chart
    city_counts.plot(kind='barh', color='#38bdf8', edgecolor='#0f172a')

    # Formatting layout styles
    plt.title('Top 10 Cities by Job Openings (Scraped Data)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Job Listings', fontsize=12)
    plt.ylabel('City Location', fontsize=12)
    plt.gca().invert_yaxis()  # Invert axis to show highest count at the top
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Render layout neatly and display the visualization window
    plt.tight_layout()
    print("\n📈 Displaying generated matplotlib chart window...")
    plt.show()

# Main Execution Routine Loop
if __name__ == "__main__":
    scraped_data = scrape_jobs()
    if scraped_data:
        visualize_data(scraped_data)