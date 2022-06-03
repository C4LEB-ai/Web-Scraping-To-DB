from bs4 import BeautifulSoup as soup
import requests
import pandas as pd

url_link = "https://www.jumia.com.ng/catalog/?q=iphone&page=0#catalog-listing"

# to srcape multiple pages we say
all_urls = []
rpc_value = url_link[-17]
for page in range(0, 50):
    # print(page)
    next_url = url_link.replace(rpc_value,str(page))
    # print(next_url)
    all_urls.append(next_url)
# print(all_urls)

for url in all_urls:
    render = requests.get(url)
    html_page = soup(render.content, "html.parser")
    # print(html_page)
    phones = html_page.find_all("a", class_ = "core")
    
    
    name =  []
    orig_price = []
    dsc_price = []
    percentage_off = []
    starRatings = []

    for phone in phones:
        name1 = phone.find("h3", {"class" : "name"}).text
        name.append(name1)
        dsc_price1 = phone.find("div", class_ = "prc").text
        dsc_price.append(dsc_price1)
        
        # codition for the orignal price 
        orig_price1 = phone.find("div", {"class" : "old"})
        if orig_price1 != None:
            orig_price.append(orig_price1.text)
        else:
            orig_price.append(dsc_price1) # takes the old price if there is no discount attarched to the product
            
            
        #scraping the percentage off, and if they is no discout therefore there will be zero percentage off
        percentage_off1 = phone.find("div", class_ = "s-prc-w")
        if percentage_off1 != None:
            percentage_off.append(percentage_off1.text[-3:])
        else:
            percentage_off.append("0%")
        # print(percentage_off)
        
        
        
# the condiction below is becaues some of the items in the website dosent have a star rating, therby throwing error on execution
        starRatings1 = phone.find(class_ = "stars _s")
        if starRatings1 != None:
            starRatings1 = starRatings1.text
            starRatings.append(starRatings1[0])
        else:
            starRatings.append(0)
    
        #  now i have the names of the phoen and the price attarched to it 

    # print(len(name))
    # print(len(dsc_price))
    # print(len(orig_price))
    # print(len(starRatings))
    # print(len(percentage_off))
    # all the scraped details are now in the same length.
    #lets now creat a dictionary object to store the values/details
    data_dict = {
        "phone_name": name[:40],
        "original_price": orig_price[:40],
        "percentage_off": percentage_off[:40],
        "discount_price": dsc_price[:40],
        "star_ratings": starRatings[:40]
                  }
    # print(data_dict)
    data1 = pd.DataFrame(data = data_dict)
    data = data1.iloc[1:]
    # data.to_csv("jumia phone scrape.csv", mode= "a", index=False)
    print(data)

        