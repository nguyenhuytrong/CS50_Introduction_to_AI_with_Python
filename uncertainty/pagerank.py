import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a prob distribution over which page to visit next,
    given a current page.

    With prob `damping_factor`, choose a link at random
    linked to by `page`. With prob `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages= len(corpus)
    if total_pages == 0: return {}
    
    # If the current page has no outgoing links
    if page not in corpus or len(corpus[page])==0:
        prob = 1/total_pages
        return {p: prob for p in corpus}
    
    # Calculate the prob of choosing a link from the current page
    # Calculate the prob of choosing any page with equal prob
    link_prob = damping_factor/len(corpus[page]) # Vd: 0.15/3 = 0.05
    equal_prob = (1-damping_factor)/total_pages # Vd: 0.85/2 = 0.425

    # Initialize the transition model dictionary
    transition_dict = {p: equal_prob for p in corpus}

    # Update the transition model dictionary with link probs
    for p in corpus[page]:
        transition_dict[p] += link_prob
    
    return transition_dict


def sample_pagerank(corpus, damping_factor, n):
    # Initialize PageRank values
    pagerank = {page: 0 for page in corpus}

    # Start with a random page
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[current_page] += 1 # Update the PageRank count for the current page
        transition_probs = transition_model(corpus, current_page, damping_factor) # Get the transition probs for the current page
        # Randomly choose the next page based on transition probs
        next_page = random.choices(
            list(transition_probs.keys()),
            weights=transition_probs.values(),
            k=1
        )[0]
        current_page = next_page # Update 

    # Normalize the PageRank values
    total_samples = sum(pagerank.values())
    pagerank = {page: count / total_samples for page, count in pagerank.items()}

    return pagerank




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    initial_rank = 1 / total_pages

    pagerank = {page: initial_rank for page in corpus} # Initialize each pagerank 

    rank_d = {page: 1 for page in corpus} # Dictionary to store the difference between old and new ranks

    # PageRank formula 
    epsilon = 0.001  # Threshold for stopping the iteration
    while any(diff > epsilon for diff in rank_d.values()):
        new_pagerank = {}
        for page in corpus:
            incoming_pagerank = 0
            for linking_page, links in corpus.items():
                if page in links or not links:
                    if len(links) > 0:
                        incoming_pagerank += pagerank.get(linking_page, 0) / len(links)
                    else:
                        # Handling Pages with No Links
                        incoming_pagerank += 0 
            new_pagerank[page] = (1 - damping_factor) / total_pages + damping_factor * incoming_pagerank
        rank_d = {page: abs(new_pagerank[page] - pagerank[page]) for page in corpus}
        pagerank = new_pagerank

    return pagerank



if __name__ == "__main__":
    main()
