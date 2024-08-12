# To create a new account for a user :
url = '/auth/register'
method = 'post'
input = {
  "username": "string",
  "password": "string",
  "user_type": 0,
  "profile_picture": "string",
  "name": "string",
  "about": "string"
}
output = {
  "created_at": "2024-08-12T18:03:45",
  "id": 5,
  "user_type": 0,
  "username": "string"
}

# To create a new account for a company :
url = '/auth/register'
method = 'post'
input = {
  "username": "string",
  "password": "string",
  "user_type": 1,
  "logo": "string",
  "address": "string",
  "name": "string",
  "about": "string"
}
output = {
  "created_at": "2024-08-12T18:03:45",
  "id": 5,
  "user_type": 0,
  "username": "string"
}

# To update the profile
url = '/auth/update_profile'
method = 'put'
input = new data as a json file
output = informatins about user/company

# To search for companies
url = "/companies?search='comany_name'"
method = 'get'
output = companies

# To view the profile of a specific company
url = "/companies/company_id"
method = 'get'
output = company's info

# To search for products
## Tou can filter by category and price(price_min & price_max)
url = "/products?search='comany_name'&category='category_name'&price_min=float&price_max=float" 
method = 'get'
output = products

# To view the informations of a specific product
url = "/products/product_id"
method = 'get'
output = product's info

# To add a new produt
## Only the company has this permission
url = "/products"
method = 'post'
input = {
  "name": "string",
  "category": "string",
  "main_image": "string",
  "additional_images": [
    "string"
  ],
  "price": 0
}
output = product's info

# How the user can rate a product!
## Only the user has this permission
url = "/ratings"
method = 'post'
input = {
  "rating": 0,
  "comment": "string",
  "product_id": 0
}
output = rating's info

# How the user can update a rating
## Only the user has this permission
url = "/ratings/rating_id"
method = 'put'
input = {
  "rating": 0,
  "comment": "string"
}
output = rating's info

# How the user can delete a rating
## Only the user has this permission
url = "/ratings/rating_id"
method = 'delete'
output = message of the status

# To view the informations of a specific rating
url = "/ratings/rating_id"
method = 'get'
output = rating's info

# To view users'info
url = "/users"
method = 'get'
output = users'info

# To view the profile of a specific user
url = "/users/user_id"
method = 'get'
output = user's info

#