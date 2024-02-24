from langchain.llms import GooglePalm
llm= GooglePalm(google_api_key="AIzaSyATg2P9z5r2nOQg29F0ChNBTIWmmLQlFag")
llm.temperature=0
prompts=['hi how are you?']
llm_result=llm._generate(prompts)
print(llm_result.generations[0][0].text)