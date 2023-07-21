import datetime
import pprint
import pymongo

try:
    client = pymongo.MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@<CLUSTER_URL>/test?retryWrites=true&w=majority")
    db = client.test
    posts = db.posts
except pymongo.errors.ConnectionFailure:
    print("Erro ao conectar ao MongoDB.")
    exit()

post = {
    "author": "Fernanda", 
    "text": "My first MongoDB application based on Python",
    "tags": ["mongodb", "python3", "pymongo"],
    "date": datetime.datetime.utcnow()
}

post_id = posts.insert_one(post).inserted_id
print("ID do post inserido:", post_id)

print("\nDocumento recuperado:")
pprint.pprint(posts.find_one())

new_posts = [
    {
        "author": "Fernanda",  
        "text": "Another post",
        "tags": ["bulk", "post", "insert"],
        "date": datetime.datetime.utcnow()
    },
    {
        "author": "Joao",
        "text": "Post from Joao. New post available",
        "title": "Mongo is fun",
        "date": datetime.datetime(2011, 18, 46, 06, 45)
    }
]

result = posts.insert_many(new_posts)
print("\nIDs dos posts inseridos em massa:", result.inserted_ids)


print("\nRecuperação por autor (Joao):")
pprint.pprint(posts.find_one({"author": "Joao"}))

print("\nDocumentos presentes na coleção posts:")
for post in posts.find():
    pprint.pprint(post)
