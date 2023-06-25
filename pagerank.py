import os
import random
import re
import sys
import numpy as np

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
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # set up initial transition probabilities as 0 for each page
    transition_probabilities = {pg: 0 for pg in corpus}
    # get total pages and the number of links from a particular page
    total_pages = len(corpus)
    total_links = len(corpus[page])

    # if a page contains links to at least one page
    if total_links != 0:
        # probability of random surfer randomly choosing one of the links from page with equal probability
        random_link_probability = (damping_factor) / (total_links)
        # probability of random surfer randomly choosing one of all pages in the corpus with equal probability
        random_page_probability = (1 - damping_factor) / (total_pages)

        # add probabilities to corresponding pages in the links and total pages
        for pg in transition_probabilities:
            if pg in corpus[page]:
                transition_probabilities[pg] += random_link_probability
            transition_probabilities[pg] += random_page_probability

    # if a page contains no links to any page
    else:
        # add equal probability to all pages in transition probabilities
        equal_probability = (1 / total_pages)
        for pg in transition_probabilities:
            transition_probabilities[pg] += equal_probability

    return transition_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initial dictionary of page visits
    visits = {page: 0 for page in corpus}

    # pick first sample page randomly
    current_page = random.choice(list(visits))
    visits[current_page] += 1

    # for remaining n-1 samples, pick based on transition model
    for _ in range(n-1):
        # get transition probabilities for the current page
        transitions = transition_model(corpus=corpus, page=current_page, damping_factor=damping_factor)

        # choose a page from the list of possible links from current page
        list_of_candidates = [page for page in transitions]
        probability_distribution = [probability for probability in transitions.values()]
        next_page = np.random.choice(a=list_of_candidates, size=1, p=probability_distribution).item()

        # set this new page as the current page and increase count
        current_page = next_page
        visits[current_page] += 1

    # normalize visits to their probability of occurrence
    page_ranks = {page: (page_visits / n) for page, page_visits in visits.items()}

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    page_ranks = {page: round((1/total_pages), 3) for page in corpus}
    max_difference = 1
    epochs = 1

    # while the difference between current page-rank and next page-rank is greater than 0.001 (until convergence)
    while max_difference > 0.001:
        next_ranks = {page: 0 for page in corpus}

        # for each page that has links going out
        for page in page_ranks:
            # get the summation term in the formula
            summation = 0

            # for every other page that has links coming into the current page
            for other_page in page_ranks:
                # get number of links on the other page
                num_links = len(corpus[other_page])

                # if the other page has no links on it then the rank is divided evenly
                if num_links == 0:
                    summation += page_ranks[other_page] / total_pages
                # if the other page has a link to the page, that the page-rank is being calculated for
                elif page in corpus[other_page]:
                    summation += page_ranks[other_page] / num_links

            # update page rank for the current page
            page_rank = ((1 - damping_factor) / total_pages) + ((damping_factor) * summation)
            next_ranks[page] = page_rank

        # calculate the differce in page-rank values from previous epoch to the current epoch
        for page in page_ranks:
            difference = abs(page_ranks[page] - next_ranks[page])
            if difference < max_difference:
                max_difference = difference

        # increase the number of epochs and update the new page-ranks
        epochs += 1
        page_ranks = next_ranks

    # just to visualize how many iterations it takes to get to the solution
    #print(f"Completed in {epochs} iteration(s).")

    return page_ranks


if __name__ == "__main__":
    main()
