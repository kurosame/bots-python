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

if __name__ == "__main__":
    print("aaaaaaaa")
