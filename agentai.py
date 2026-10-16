from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from crewai_tools import SerperDevTool
# from decouple import config
from dotenv import load_dotenv

load_dotenv()

from crewai import LLM

# Tool 1
# Basic configuration


# llm = LLM(
#     model="azure/gpthelpdeskchat",
#     api_version="2023-05-15"
# )


# Tool 2

# Search_Tool = SerperDevTool(n_results=1,)

class AgenticAI:
    def __init__(self,Product,Temperature):
        self.product = Product
        self.temperature = Temperature
        self.llm = LLM(
                    model="gemini/gemini-1.5-pro-latest",
                    temperature=0.7
                )
        # self.llm = LLM(
        #             model="azure/gpthelpdeskchat",
        #             api_version="2023-05-15",
        #             max_tokens = 1200,
        #             temperature = self.temperature
        #         )
        

        # Agent 1

        self.Senior_Reasearch_Analyst  = Agent(
            role = 'You are a Brand and Product Finding Senior Research Analyst',
            goal = f'Research analyze and synthesize comprehensive information on {Product} from reliable web source',
            backstory = "you're an expert research analyst with advanced web research skills."
                        "you excel at finding, analyzing, and synthesizing information from "
                        "across the internet using search tools. you're skilled at"
                        "distinguishing reliable source from unreliable ones, "
                        "fact-checking, cross-referencing information, and"
                        "identifying key pattern and insights. you provide"
                        "well-organized research briefs with proper citations"
                        "and source verification. your analysis include both"
                        "raw data and interpreted insights,making complex"
                        "* **Demand Forecasting & Planning:** Agentic AI enhances accuracy by processing real-time data on consumer behavior and historical patterns to make precise demand forecasts. This allows for optimized inventory levels by anticipating demand spikes or drops, reducing overstocking or stockouts."
                        "* **Procurement and Supply Chain Optimization:** AI manages vendor relationships, optimizes inventory, and automates reordering, reducing costs and ensuring supply continuity."
                        "information accessible and actionable.",
            allow_delegation= False,
            verbose= True,
            # tools= [],
            llm =self.llm   
        )

        # Agent 2 Content writer

        self.Content_writer = Agent(
            role= "content writer",
            goal = "Transform Research findings into engaging blog posts while maintaining accuracy",
            backstory="You're Skilled Content writer specialized in creating"
                        "engaging, accessible content from technical research. "
                        "you work closely with the Senior Research Analyst and excel at maintaining the perfect "
                        "balance between informative and entertaining writing,"
                        "while ensuring all facts and citations from the research "
                        "are properly incorporated. you have a talent for making"
                        "Return No brands found if no relevant brands are discovered"
                        "complex topics approachable without oversimplifying them. ",
                        
            allow_delegation= False,
            verbose= True,
            llm = self.llm             
        )


        # Research tasks

        self.research_tasks = Task(
            description=("""
                        1.conduct comprehensive research on {Product} including :
                            - Recent developments and news
                            - Key Industry trends and innovations
                            - Expert opinions and analysis
                            - Statistical data and market insights
                            - Average rating (on a scale of 1-5 or equivalent)
                            - Number of positive and negative reviews
                            - Key features frequently mentioned in reviews (both positive and negative)
                            - Overall sentiment towards the brand
                        2. Evaluate source credibility and fact-check all information
                        3. organize findings into a structured research brief
                        4. include all relevant citations and sources
                        """),
            expected_output=""" You are a Filter Top 5 Brands Agent
                            - A detailed research report containing
                            - Executive summary of key findings
                            - Comprehensive analysis of current trends and developments
                            - List of verified facts and statistics
                            - All citations and links to original sources
                            - Clear categorization of main themes and patterns
                            Please format with clear sections and bullets points for easy reference.
                            """,
            agent= self.Senior_Reasearch_Analyst
        )

        # Task 2 Content Writer

        self.writing_task = Task(
            description=("""Using the research brief provided , create an engaging blog post that:
                        1. Transforms technical information into accessible content
                        2. Maintain all factual accuracy and citations from the research 
                        3. Includes:
                            - Attention- grabbing introduction 
                            - Well- structured body section with clear handlings
                            - Compelling conclusion
                        4. Preserves all source citations in [Source : URL]format
                        5. Includes a reference section at the end
                        6. The **Brand or Product Finding Agent** identifies relevant brands.
                        7. The **Review Analyzer Agent** processes reviews for those brands.
                        8. The **Comparison Agent** compares and ranks the brands based on the review analysis.
                        9. The **Filter Top 5 Brands Agent** selects the top 5 brands from the ranked list.
                        """  ),
            expected_output="""A Polished blog post in markdown format that:
                            - Engages readers while maintaining accuracy
                            - contains properly structured sections
                            - Includes inline citations hyperlinked to the original source url
                            - Presents information in an accessible yet informative way
                            - follows proper markdown formatting, use H1 for the title and H3 for the subsections
                            """,
            agent=self.Content_writer
            
        )

    def Agent_Crew(self):
        crew = Crew(
            agents=[self.Senior_Reasearch_Analyst, self.Content_writer],
            tasks=[self.research_tasks, self.writing_task],
            verbose=True,
        )
        result = crew.kickoff(inputs = {"Product":self.product})


        return result


