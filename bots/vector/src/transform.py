# from transformers import AutoTokenizer, AutoModel
# import torch
# import numpy as np
# from supabase_py import create_client

# # Initialize Supabase client
# url = "your-supabase-url"
# key = "your-supabase-key"
# supabase = create_client(url, key)

# # Initialize transformer model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("Supabase/gte-small")
# model = AutoModel.from_pretrained("Supabase/gte-small")

# # Define text data
# title = "First post!"
# body = "Hello world!"

# # Generate a vector using transformers
# inputs = tokenizer(body, return_tensors="pt")
# outputs = model(**inputs)

# # Pooling and normalization
# embedding = torch.mean(outputs.last_hidden_state, dim=1).detach().numpy()
# embedding = embedding / np.linalg.norm(embedding)

# # Store the vector in Postgres
# data, error = supabase.from_("posts").insert(
#     {
#         "title": title,
#         "body": body,
#         "embedding": embedding.tolist(),
#     }
# )


import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv(verbose=True)


def create_supabase_client():
    supabase = create_client(
        os.environ.get("SUPABASE_API_URL"), os.environ.get("SUPABASE_API_KEY")
    )
    auth = supabase.auth.sign_in_with_password(
        {
            "email": os.environ.get("SUPABASE_GLOSSARY_EMAIL"),
            "password": os.environ.get("SUPABASE_GLOSSARY_PASSWORD"),
        }
    )
    supabase.postgrest.auth(auth.session.access_token)

    return supabase


if __name__ == "__main__":
    supabase = create_supabase_client()

    for root, _, files in os.walk(os.environ["DIR_PATH"]):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.splitext(os.path.basename(file_path))[0]

            with open(file_path, "r") as f:
                supabase.table("raw_data").insert(
                    json={"title": file_name, "data": f.read()}, upsert=True
                ).execute()
                break

    supabase.auth.sign_out()
