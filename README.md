# FastApi Project
Developped  user authentication and simple crud operations with **fast api** and **mongo db** with following best practices of **SOLID** principles. **Motor** library used for mongodb connection.
- Python version ***3.10.8***
- FastApi version ***0.95.1***
- Motor version ***3.1.2***
- Mongodb version ***latest stable version***
- Using Zorin OS version **16.2** which based on ubuntu 20.04 is my development OS.

# Project setup
- create ```.env.dev``` file in project root directory. Put below variables in it:
```
DB_URL=mongodb://localhost:27017
DB_NAME=studentPortal_dev
JWT_ALGORITHM=HS256
JWT_SECRET=top-secret-key
```
- Now, follow below steps to install dependencies in correct way.
- pip install poetry
- poetry shell
- poetry install 
- and thats it! We initialized our project to our system its ready to run.

# Documentation 
Fastapi has own built-in swagger ui. So when you run project simply open this url in your browser: 
- ```localhost:5002/api/v1/docs ```

# Run project
After following above steps you can simply run the project by using main.py, Simply call below command in your terminal and thats it!
```
python main.py --env="dev"
``` 

# Further Improvements
This project created 2 years ago while i am learning fastapi framework. Now i optimized my old code base and i am trying to implement best practices of SOLID principles while optimizing the code base. In addition what we can do is:
- Dockerize project by using ```docker``` & ```docker compose```.
- Create unit tests for ```BaseService``` and ```BaseModel```. 
- Setup CI/CD using ```github actions``` and deploy project to remote ```ubuntu server```.
- May use ```nginx``` , ```redis```, ```elastic search``` or other popular services to improve project scalability, maintainability etc.
- Apply request benchmark to this project.

