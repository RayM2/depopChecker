This project intends to accomplish the following:

1. Scrape product names and descriptions from Depop.
2. Search up these product names on Duck Duck Go.
3. Find pages with either product names or searches on traditional retailers.
4. When possible, return prices on these retailers so the user can compare to the prices on Depop without having to leave the app.

Here are some of the limitations of my present approach:

1. Sometimes user descriptions are not accurate or in-depth enough to be used in a search to accurately identify the product on retailers, however, I have returned very high rates of accuracy in finding descriptions that match the product.
2. Two of the best sources for finding retail pricing data are inaccessible for this project. The best place to find aggregated data of prices across various retailers is Google Shopping, and the largest online retailer is Amazon. Both do not provide high compatibility for web scraping tools and often block them.
3. Given that every website's html layout of a product page looks different, navigating to the product page of every website requires separate logic for each website which has a different layout, which is infeasible under my scope. This means that I have shortlisted a group of common retailers such as Nike, eBay, Marshalls, TJMaxx, etc. and developed logic for their websites, but this still provides a lower degree of price values. However, the tool still provides ready-made links for the user to navigate to in about 2 seconds, which is faster than they might look it up.

Future improvements could be to add support for more retailers, or to add paid service of the serp API.
