import os

from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import SupabaseVectorStore
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
    embeddings = OpenAIEmbeddings(
        model=os.environ.get("OPENAI_EMBEDDINGS_MODEL"),
        deployment=os.environ.get("OPENAI_EMBEDDINGS_DEPLOYMENT"),
        chunk_size=1,
    )

    docs = []

    for root, _, files in os.walk(os.environ["DIR_PATH"]):
        for file in files:
            file_path = os.path.join(root, file)

            with open(os.path.join(root, file), "r") as f:
                lines = f.readlines()

                category = ""
                titles = []
                is_titles = False
                description = ""
                is_description = False

                for i in range(len(lines)):
                    if lines[i].strip() == "## category":
                        category = lines[i + 2].strip()
                    if is_titles:
                        if lines[i].strip() == "## description":
                            is_titles = False
                        elif lines[i].strip() != "":
                            titles.append(lines[i].strip())
                    if lines[i].strip() == "## titles":
                        is_titles = True
                    if is_description:
                        description += lines[i].strip()
                    if lines[i].strip() == "## description":
                        is_description = True

                docs.append(
                    Document(
                        page_content=description,
                        metadata={
                            "category": category,
                            "titles": titles,
                        },
                    )
                )
            break

    # Delete all rows of a table
    supabase.table("documents").delete().neq("content", None).execute()

    store = SupabaseVectorStore.from_documents(
        docs,
        embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
    )
    print(store)

    supabase.auth.sign_out()
