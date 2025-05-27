from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from blog_agent import create_search_agent
import time


def load_few_shot_examples(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


FEW_SHOT_EXAMPLES = load_few_shot_examples("examples.txt")

blog_prompt_template = PromptTemplate(
    input_variables=["topic", "research_notes"],
    template=f"""{FEW_SHOT_EXAMPLES}
Now, based on the format above, write a blog post for the following with a detailed and informative content in 3000 
words including the source urls and references and use colons after each heading like Introduction:, Content:, Summary: :

Input:
Topic: {{topic}}
Research Notes: {{research_notes}}

Output: Display data in paragraphs with headings as introduction,content,summary"""
)


def create_blog_writer_llm():
    # Plain LLM (no tools) for blog writing
    llm = ChatGroq(
        temperature=0.7,
        model_name="llama3-70b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    return llm


def generate_blog(topic: str, search_agent, blog_writer_llm):
    print(f"\n🔍 Collecting research data for topic: {topic}...")
    research_wiki = search_agent.invoke(f"Search Wikipedia for: {topic}")
    time.sleep(8)
    research_web = search_agent.invoke(f"Search the web for: {topic}")

    combined_research = f"{research_wiki}\n\n{research_web}"

    print("\n✍️ Generating blog...")

    prompt = blog_prompt_template.format(
        topic=topic,
        research_notes=combined_research
    )
    blog_content = blog_writer_llm.invoke(prompt)
    cleaned_output = clean_blog_output(blog_content.content)
    print("\n✅ Blog generated successfully!\n")
    print("📰 Blog Output:\n")
    print(cleaned_output)


def clean_blog_output(text: str) -> str:
    return text.replace("**", "").replace("\\n", "\n").strip()


if __name__ == "__main__":
    print("💬 Enter a blog topic:")
    topic = input("➡️ Topic: ").strip()

    if not topic:
        print("❗ No topic provided. Exiting.")
    else:
        search_agent = create_search_agent()
        blog_writer_llm = create_blog_writer_llm()
        generate_blog(topic, search_agent, blog_writer_llm)