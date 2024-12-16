# Flask REST API Project

Following the tutorial https://www.youtube.com/playlist?list=PLYPlvTh05MsxJja9bzQCSTDu4hnEv5N_u, I created a Python 
Flask App for a grocery store called "Healthy Bites". 

**It contains the following pages:**

**Homepage**: Displays all the products
<img width="1486" alt="image" src="https://github.com/user-attachments/assets/860c32cd-d4c1-4917-b334-88583cb4d9a6" />

* Filter by brand
  * Click on an item in the Brand dropdown menu from the navbar, and it will show all the products of that brand
* Filter by category
  * Click on an item in the Category dropdown menu from the navbar, and it will show all the products of that brand

**Product details page**: Displays all the details related to a specific product
<img width="1507" alt="image" src="https://github.com/user-attachments/assets/66768595-4b60-45ef-92d2-be0e7cf5eb53" />

**Shopping cart page**: Displays all the products in the shopping cart and the options to update or delete items
<img width="1507" alt="image" src="https://github.com/user-attachments/assets/5f7b9a13-27f5-4670-b5e0-54d0a77a89d7" />

**It supports the following functions:**

Brand: 
- `/addbrand`
- `/updatebrand/<int:id>`


Category:
- `/addcat`
- `/updatecat/<int:id>`
- `/deletecat/<int:id>`

Product:
- `/addproduct`
- `/deleteproduct/<int:id>`

Cart:
- `/cart`
- `/addtocart`
- `/updatecart/<int:code>`
- `/deleteitem/<int:id>`
- `/clearcart`


