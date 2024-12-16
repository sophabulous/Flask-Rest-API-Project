# Flask REST API Project

Following the tutorial https://www.youtube.com/playlist?list=PLYPlvTh05MsxJja9bzQCSTDu4hnEv5N_u, I created a Python 
Flask App for a grocery store called "Healthy Bites". 

**It contains the following pages:**

**Homepage**: Displays all the products
* Filter by brand
  * Click on an item in the Brand dropdown menu from the navbar, and it will show all the products of that brand
* Filter by category
  * Click on an item in the Brand dropdown menu from the navbar, and it will show all the products of that brand

**Product details page**: Displays all the details related to a specific product

It supports the following functions:

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


