import os
from datetime import datetime

def get_authors():
    authors = []
    print("\nEnter author information:")
    
    while True:
        last_name = input("Enter author's last name (or press Enter to finish): ").strip()
        if not last_name:
            if not authors:
                print("Please enter at least one author.")
                continue
            break
        first_name = input("Enter author's first name: ").strip()
        if first_name:
            authors.append(f"{last_name}, {first_name[0].upper()}.")
        else:
            authors.append(f"{last_name}")

    return authors

def format_authors(authors, citation_type="reference"):
    if not authors:
        return None
    
    if citation_type == "intext":
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} and {authors[1]}"
        else:
            return f"{authors[0]} et al."
    
    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    elif len(authors) == 3:
        return f"{authors[0]}, {authors[1]} and {authors[2]}"
    else:
        return f"{authors[0]}, {authors[1]}, {authors[2]} et al."

def get_year():
    while True:
        year = input("Publication year: ").strip()
        if not year:
            return ""
        if year.isdigit() and len(year) == 4:
            return year
        print("Please enter a valid 4-digit year or press Enter to skip.")

def get_date():
    year = get_year()
    if not year:
        return ""
    month = input("Publication month: ").strip()
    day = input("Publication day: ").strip()
    return f"{day} {month} {year}" if day and month else year

def save_citation(reference, intext, source_type):
    filename = "harvard_citations.txt"
    file_exists = os.path.exists(filename)
    
    with open(filename, "a", encoding="utf-8") as file:
        if not file_exists:
            file.write("Harvard Style Citations\n")
            file.write("=" * 50 + "\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 50 + "\n\n")
        
        file.write(f"Type: {source_type}\n")
        file.write(f"Reference: {reference}\n")
        file.write(f"In-text: {intext}\n")
        file.write("-" * 80 + "\n\n")
    
    return filename

def build_citation(authors, year, title, *parts):
    citation_parts = []
    
    if authors and year:
        citation_parts.append(f"{format_authors(authors)} ({year})")
    elif authors:
        citation_parts.append(f"{format_authors(authors)}")
    elif year:
        citation_parts.append(f"({year})")
    
    if title:
        citation_parts.append(f"'{title}'")
    
    citation_parts.extend(part for part in parts if part)
    
    citation = " ".join(citation_parts)
    if not citation.endswith('.'):
        citation += '.'
    
    if authors and year:
        intext = f"({format_authors(authors, 'intext')}, {year})"
    elif authors:
        intext = f"({format_authors(authors, 'intext')})"
    elif year:
        intext = f"({year})"
    else:
        intext = "(n.d.)"
    
    return citation, intext

def create_book_citation():
    print("\n📚 Book")
    authors = get_authors()
    year = get_year()
    title = input("Book title: ").strip()
    edition = input("Edition: ").strip()
    city = input("City: ").strip()
    publisher = input("Publisher: ").strip()

    edition_part = f"{edition} edn" if edition else ""
    pub_part = f"{city}: {publisher}" if city and publisher else city or publisher
    
    citation, intext = build_citation(authors, year, title, edition_part, pub_part)
    return citation, intext, "Book"

def create_article_citation():
    print("\n📄 Journal Article")
    authors = get_authors()
    year = get_year()
    title = input("Article title: ").strip()
    journal = input("Journal: ").strip()
    volume = input("Volume: ").strip()
    issue = input("Issue: ").strip()
    pages = input("Pages: ").strip()
    doi = input("DOI: ").strip()

    journal_part = f"'{journal}'," if journal else ""
    volume_issue = f"{volume}({issue})," if volume and issue else f"{volume}," if volume else f"({issue})," if issue else ""
    pages_part = f"pp. {pages}" if pages else ""
    doi_part = f", doi: {doi}" if doi else ""

    full_parts = [journal_part, volume_issue, pages_part + doi_part]
    citation, intext = build_citation(authors, year, title + ",", *full_parts)
    return citation, intext, "Journal Article"

def create_website_citation():
    print("\n🌐 Website")
    authors = get_authors()
    if not authors:
        org_author = input("Organization: ").strip()
        authors = [org_author] if org_author else []
    
    year = get_year()
    title = input("Page title: ").strip()
    site_name = input("Website: ").strip()
    url = input("URL: ").strip()
    accessed = input("Accessed date: ").strip()

    site_part = f"'{site_name}'." if site_name else ""
    url_part = f"Available at: {url}" if url else ""
    access_part = f"(Accessed: {accessed})" if accessed else ""
    
    citation, intext = build_citation(authors, year, title + ",", site_part, url_part, access_part)
    return citation, intext, "Website"

def create_newspaper_citation():
    print("\n📰 Newspaper")
    authors = get_authors()
    if not authors:
        authors = ["Anon"]
    
    date = get_date()
    title = input("Article title: ").strip()
    newspaper = input("Newspaper: ").strip()
    edition = input("Edition: ").strip()
    pages = input("Pages: ").strip()

    newspaper_part = f"'{newspaper}'" if newspaper else ""
    edition_part = f", {edition}" if edition else ""
    pages_part = f", p. {pages}" if pages else ""
    
    year = date.split()[-1] if date else ""
    citation_parts = []
    
    if authors and date:
        citation_parts.append(f"{format_authors(authors)} ({date})")
    elif authors:
        citation_parts.append(f"{format_authors(authors)}")
    elif date:
        citation_parts.append(f"({date})")
    
    if title:
        citation_parts.append(f"'{title}',")
    
    citation_parts.extend(part for part in [newspaper_part + edition_part + pages_part] if part.strip())
    
    citation = " ".join(citation_parts).rstrip(',') + '.'
    
    if authors and year:
        intext = f"({format_authors(authors, 'intext')}, {year})"
    elif authors:
        intext = f"({format_authors(authors, 'intext')})"
    elif year:
        intext = f"({year})"
    else:
        intext = "(n.d.)"
    
    return citation, intext, "Newspaper"

def create_conference_citation():
    print("\n🎤 Conference")
    authors = get_authors()
    year = get_year()
    title = input("Paper title: ").strip()
    conference = input("Conference: ").strip()
    location = input("Location: ").strip()
    date = input("Dates: ").strip()
    pages = input("Pages: ").strip()

    conf_info = [conference, location, date]
    conf_part = f"paper presented at {', '.join(filter(None, conf_info))}" if any(conf_info) else ""
    pages_part = f", pp. {pages}" if pages else ""
    
    citation, intext = build_citation(authors, year, title + ",", conf_part + pages_part)
    return citation, intext, "Conference"

def create_thesis_citation():
    print("\n🎓 Thesis")
    authors = get_authors()
    year = get_year()
    title = input("Thesis title: ").strip()
    degree = input("Degree: ").strip()
    institution = input("Institution: ").strip()

    degree_part = ", ".join(filter(None, [degree, institution]))
    citation, intext = build_citation(authors, year, title + ",", degree_part)
    return citation, intext, "Thesis"

def create_report_citation():
    print("\n📊 Report")
    authors = get_authors()
    if not authors:
        org_author = input("Organization: ").strip()
        authors = [org_author] if org_author else []
    
    year = get_year()
    title = input("Report title: ").strip()
    report_no = input("Report number: ").strip()
    institution = input("Institution: ").strip()
    location = input("Location: ").strip()

    number_part = f", {report_no}" if report_no else ""
    pub_part = ", ".join(filter(None, [institution, location]))
    
    citation, intext = build_citation(authors, year, title + number_part, pub_part)
    return citation, intext, "Report"

def create_chapter_citation():
    print("\n📖 Book Chapter")
    chapter_authors = get_authors()
    year = get_year()
    chapter_title = input("Chapter title: ").strip()
    
    print("\nBook editor information:")
    editors = get_authors()
    book_title = input("Book title: ").strip()
    edition = input("Edition: ").strip()
    city = input("City: ").strip()
    publisher = input("Publisher: ").strip()
    pages = input("Pages: ").strip()

    editors_part = ""
    if editors:
        if len(editors) == 1:
            editors_part = editors[0].replace(".,", " (ed.),")
        else:
            editors_part = format_authors(editors) + " (eds.)"
    
    edition_part = f", {edition} edn" if edition else ""
    pub_part = f"{city}: {publisher}" if city and publisher else city or publisher
    pages_part = f", pp. {pages}" if pages else ""
    
    citation_parts = []
    if chapter_authors and year:
        citation_parts.append(f"{format_authors(chapter_authors)} ({year})")
    elif chapter_authors:
        citation_parts.append(f"{format_authors(chapter_authors)}")
    elif year:
        citation_parts.append(f"({year})")
    
    if chapter_title:
        citation_parts.append(f"'{chapter_title}', in")
    
    if editors_part:
        citation_parts.append(editors_part)
    
    if book_title:
        citation_parts.append(f"'{book_title.title()}'{edition_part}")
    
    if pub_part:
        citation_parts.append(pub_part)
    
    citation_parts.append(pages_part)
    
    citation = " ".join(filter(None, citation_parts)).rstrip(',') + '.'
    
    if chapter_authors and year:
        intext = f"({format_authors(chapter_authors, 'intext')}, {year})"
    elif chapter_authors:
        intext = f"({format_authors(chapter_authors, 'intext')})"
    elif year:
        intext = f"({year})"
    else:
        intext = "(n.d.)"
    
    return citation, intext, "Book Chapter"

def main():
    print("Harvard Citation Generator")
    print("=" * 40)

    citations = []
    functions = {
        '1': create_book_citation,
        '2': create_article_citation,
        '3': create_website_citation,
        '4': create_newspaper_citation,
        '5': create_conference_citation,
        '6': create_thesis_citation,
        '7': create_report_citation,
        '8': create_chapter_citation
    }

    while True:
        print("\nSource types:")
        print("1. Book")
        print("2. Journal Article")
        print("3. Website")
        print("4. Newspaper")
        print("5. Conference")
        print("6. Thesis")
        print("7. Report")
        print("8. Book Chapter")
        print("9. View All")
        print("10. Exit")

        choice = input("\nChoose: ").strip()

        if choice in functions:
            try:
                reference, intext, source_type = functions[choice]()
                citations.append((reference, intext, source_type))
                filename = save_citation(reference, intext, source_type)
                
                print("\n" + "="*40)
                print("REFERENCE:")
                print(reference)
                print("\nIN-TEXT:")
                print(intext)
                print(f"\nSaved to {filename}")
                
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == '9':
            if not citations:
                print("\nNo citations yet.")
            else:
                print("\n" + "="*50)
                print("ALL CITATIONS")
                for i, (ref, intext, source_type) in enumerate(citations, 1):
                    print(f"\n{i}. {source_type}:")
                    print(f"   {ref}")
                    print(f"   {intext}")
                    
        elif choice == '10':
            if citations:
                print(f"\nGenerated {len(citations)} citations")
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()