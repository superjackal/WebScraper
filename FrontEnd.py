from tkinter import *
from tkinter import ttk
import scraper_both

def create_table(container):
    canvas = Canvas(container)
    yscrollbar = ttk.Scrollbar(canvas, orient='vertical')
    tree = ttk.Treeview(canvas, yscrollcommand=yscrollbar.set, columns=("c0","c1","c2","c3"), height= 18)
    tree.grid(row=4,column=0,columnspan=5)

    tree.column("#0",width=50,anchor=CENTER, stretch=NO)
    tree.column("#1",anchor=CENTER, stretch=NO)
    tree.column("#2",anchor=CENTER, stretch=NO)
    tree.column("#3",anchor=CENTER, stretch=NO)
    tree.column("#4",anchor=CENTER, stretch=NO)

    tree.heading("#0",text="Sr. No.")
    tree.heading("#1",text="Name")
    tree.heading("#2",text="Price")
    tree.heading("#3",text="Review")
    tree.heading("#4",text="No of Reviews")
    
    for i in range(len(scraped)):
        tree.insert('','end',text=str(i+1), values=(scraped[i]['name'], scraped[i]['price'], scraped[i]['review'], scraped[i]['review_number']))
    
    yscrollbar.configure(command=tree.yview)
    yscrollbar.grid(row=4,column=5, sticky=NS)

    return canvas

def submitted():
    global search
    search = subcategory_dropdown.get()
    global category
    category = category_dropdown.get()
    global scraped
    try:
        scraped = scraper_both.FlipkartScraper(search=search)
    except:
        end.set('No Results Found')
        return
    end.set(f"{len(scraped)} Items Found \n Data has been stored in MongoDB Cloud")
    
    table = create_table(window)
    table.grid(row=4,column=0,columnspan=4)
    min_price = int(scraped[0]['price'].replace(",","")[1:])
    min_item = scraped[0]['name']
    for item in scraped:
        item['price'] = int(item['price'].replace(",","")[1:])
        if(item['price'] < min_price):
            min_price = item['price']
            min_item = item['name']

        # if(item['price'] > max_price):
        #     max_price = item['price']
        #     max_item = item['name']

    Label(window, text=f"Minimum Price is ₹{min_price} for {min_item}").grid(row=3, column=3)

def show_subcategories(e):
    if category_dropdown.get() == "Electronics":
        subcategory_dropdown.config(value = electronics)
    if category_dropdown.get() == "Furniture":
        subcategory_dropdown.config(value = furniture)
    if category_dropdown.get() == "Appliances":
        subcategory_dropdown.config(value = appliances)
    if category_dropdown.get() == "Toys":
        subcategory_dropdown.config(value = toys)
    if category_dropdown.get() == "Other":
        subcategory_dropdown.config(value = other)


window = Tk()
window.title("Web Scraper")
window.state('zoomed')

categories= ['Electronics','Appliances','Furniture','Toys','Other']

electronics = ['Camera', 'Monitors', 'TV', 'Laptops', 'Mobile','Tablet']
furniture = ['Bed', 'Sofa', 'Shoe Racks']
appliances = ['Juicer', 'Vacuum Cleaner', 'Fans', 'Air Conditioner', 'Refrigerator','Washing Machine']
toys=['Puzzles', 'Soft toys', 'Remote Control Cars']
other=[]

# Creating category drop down menu
Label(window, text = "Select Category").grid(row=0,column=0)
category_dropdown = ttk.Combobox(window, value = categories)
category_dropdown.grid(row=0,column=1,padx=30,pady=30)
category_dropdown.set('None')

# Binding categories with subcategories
category_dropdown.bind("<<ComboboxSelected>>", show_subcategories)

# Creating subcategory drop down menu
Label(window, text = "Select Sub Category").grid(row=1,column=0)
subcategory_dropdown = ttk.Combobox(window, value ="")
subcategory_dropdown.grid(row=1,column=1,padx=30,pady=30)
subcategory_dropdown.set('None')


btn = Button(window, text="Submit",command=submitted, bg = "White")
btn.grid(row=2, columnspan=2,padx=30,pady=30)

end = StringVar()
end.set("")


text = Label(window, textvariable=end, bg="White").grid(row=3,columnspan=2 )#,padx = 30, pady = 30)

window.mainloop()