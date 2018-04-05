# TEST
Black Friday is close and companies are starting to prepare their deals and offers

Customers have many ways of informing promotions, they can be supplied on excel, csv, etc.
But they always have some data in common such as:

- product_id
- product_name
- product_description
- price
- discount (% over price)
- shipping_discount

We already have some parsers for json, csv and excel files, so what we need right now is:

 a) Design the schema for the promotions table (MySQL /SQLite)

 b) Design a Flask endpoint with the logic that coordinates the loading of promotions input,
    and stores them on the promotions table.

 c) Design another endpoint to query/list the promotions uploaded by the user


##Notes:

- More input sources can be added in the future so the design needs to be flexible enough to handle that
- No need to worry about authentication
- Its okay to mock or have dummy logic on input loaders in order to have a functional api prototype
- Its okay to assume some preconditions due to this dummy API been an isolated endpoint,
  but PLEASE include any comment or explanation of anything that you would change in the solution
  if you had access to the real API and Core modules
