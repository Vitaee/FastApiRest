# FastApi Project
- Making user authentication and crud application with **fast api** and **mongo db**.
- Python version ***3.9.6***
- FastApi version ***0.68.0***
- Mongodb version ***v5.0.2***

# Documentation 

**Show User**
----
  Returns json data about a single user.

* **URL**

  /user/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `No params required but user need to be logged in`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
```
{ 
_id:"61166b2baac13dbba6ffde32"
first_name: "Can"
last_name: "Ilgu"
bio: "user bio"
email:"can@gmail.com"
password:"$2b$12$NRNSiaPt3Bt5Hwbdva7Db./yOo66dM4AYNli7skJsMiKeiCcVZ2C6" 
}
```
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/user/",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```


# Run project

```
git clone https://github.com/Vitaee/FastApiRest.git 

cd FastApiRest

pip install -r requirements.txt

py main.py 

``` 

