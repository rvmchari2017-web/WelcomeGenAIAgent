import streamlit as st
from agentai import AgenticAI  # Assuming this is your agent library.  May need adjustment.
from Gemini_ai import Gemini

st.set_page_config(page_title="Content Researcher & Writer",page_icon=" ",layout="wide")


def product_analyzer():
    st.title("Product Analyzer Agent for Best Brand Finding")
    st.markdown("generate blog posts about any topic using AI Agents")
    

    with st.sidebar:
        st.header("Content setting")
        topic = st.text_area('Enter your Topic', height=100,placeholder='Enter your Topic')        
        st.markdown('###LLM Settings')
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.01)
        st.markdown("-----------")
        model_selection = st.radio(
                "Select Code Generation Model:",
                ("AgentAI Content writer","GenAI")
            )
        
        Genrate_button = st.button("Generate Content",type="primary",use_container_width=True)
        with st.expander("! How to use"):
            st.markdown("""
                        1.Enter your desired content topic
                        2. Play with the temperature
                        3.click 'Generate content' to start
                        4.wait for the AI to generate  your article
                        5.Download the results as markdown file
                        """)
        
         
        

    if Genrate_button:
        with st.spinner("Generating Content ... This may take movement..."):
            try:
                if model_selection == "AgentAI Content writer": 
                            
                    agent = AgenticAI(Product=topic,Temperature=temperature)
                    # Replace this with your actual agent interaction.  The following is a placeholder.
                    result = agent.Agent_Crew()  #  Agentai interaction (replace with your actual call)

                # Placeholder agent response simulation:
                # if "laptop" in user_input.lower():
                #     result = "Based on your input, I recommend checking out brands like Apple, Dell, and Lenovo.  Consider factors like screen size, processor, and RAM."
                # elif "phone" in user_input.lower():
                #     result = "Top phone brands to consider include Apple (iPhone), Samsung (Galaxy), and Google (Pixel).  Think about camera quality, battery life, and operating system."
                # else:
                #     result = "I need more information to recommend specific brands. Please provide more details about the product you are looking for."
                
                    
                    st.markdown("Generated conetent")
                    
                    st.markdown(result)
                    st.download_button(
                        label='Download Content',
                        data = result.raw,
                        file_name=f"{topic.lower().replace(' ','_')}_article.md",
                        mime = "text/markdown"                        
                    )
                elif model_selection == "GenAI":
                    result = Gemini(input = topic + "Genrate output in markdown format")
                    st.markdown("Generated conetent")
                    
                    st.markdown(result)
                    st.download_button(
                        label='Download Content',
                        data = result,
                        file_name=f"{topic.lower().replace(' ','_')}_article.md",
                        mime = "text/markdown"                        
                    )
                

            except Exception as e:  #Catch potential errors from agentai or other parts of the code
                st.error(f"An error occurred: {e}")
                st.info("Please check your input or try again later.")

    else:
        st.info("Enter product details in the left column to see the analysis.")


if __name__ == "__main__":
    product_analyzer()