import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in your .env file")


class PPTCotentGeneratorGold:
    def __init__(self):
        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3  # lower = more focused summaries
        )

        # Define a reusable summarization prompt
        self.prompt = PromptTemplate(
    input_variables=[
        "topic",
        "text",
        "num_slides",
        "style",
        "complexity",
        "audience",
        "purpose",
        "language",
        "notes"
    ],
    template="""
You are an expert presentation designer.
Generate structured slide content for a PowerPoint presentation.
Each Slide's Content should be less than 100 words.

📌 Requirements:
- Topic: {topic}
- Target Audience: {audience}
- Purpose: {purpose}
- Number of Slides: {num_slides}
- Content Complexity: {complexity}
- Style/Tone: {style}
- Language: {language}
- Additional Notes: {notes}

📌 Input Material:
{text}

📌 Output Instructions:
**Refer the Input Material and give more importance to it if the topic is irrelevent from the input material leave the topic and use input material only and if the input material is not provided then use topic but overall give most importance to input material for output generation 
1. **Title Slide (Slide 1)**:
   - Presentation title: {topic}
   - Subtitle: {purpose} or {audience} if relevant
   - Author: Amey G M
   - Date: <current date>
   - Optional tagline

2. **Content Slides (Slide 2 onwards)**:
   - Each slide should have 3–5 bullet points.
   - Bullets **may optionally have a heading** and can include subpoints if needed.
   - Suggest slide titles for each slide if appropriate.
   - Summarize input material; do not repeat verbatim.
   - Maintain style, tone, and complexity as requested.
   -content length to all point should be medium to large.
   -necessarily try to generate bullet headings

📌 Output Format:
Slide 1: Title Slide
- Title: {topic}
- Subtitle: {purpose}
- Author: Amey G M
- Date: <date>
- [Optional: Tagline]

Slide 2: [Slide Title]
- Bullet 1 Heading or Bullet 1
  - Subpoint 1 (optional)
  - Subpoint 2 (optional)
- Bullet 2 Heading or Bullet 2
...
    """
)



    def generate_content(
        self,
        text: str,
        topic: str,
        num_slides: int,
        style: str,
        complexity: str,
        audience: str,
        purpose: str,
        language: str,
        notes: str
    ) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({
            "text": text,
            "topic": topic,
            "num_slides": num_slides,
            "style": style,
            "complexity": complexity,
            "audience": audience,
            "purpose": purpose,
            "language": language,
            "notes": notes,
        })
        return response.content


if __name__ == "__main__":
    # Example usage
    text = ""

    content_generator = PPTCotentGeneratorGold()
    summary = content_generator.generate_content(
        text=text,
        topic="",
        num_slides=5,
        style="Professional, concise",
        complexity="Intermediate",
        audience="Business Executives",
        purpose="Awareness Presentation",
        language="English",
        notes="End with key takeaways and call-to-action"
    )
    print("\n✅ Generated Slide Content:\n", summary)
