def construct_prompt(resume_text, job_description, sender_details, receiver_name, role):
    sender_name = sender_details.get("name", "[Your Name]")
    sender_degree = sender_details.get("degree", "[Your Degree]")
    sender_major = sender_details.get("major", "[Your Major]")
    sender_university = sender_details.get("university", "[Your University]")
    sender_graduation = sender_details.get("graduation", "[Graduation Date]")

    # Enhanced prompt template
    return f"""
    TASK: Compose a professional cold email (maximum 150 words) to express interest in the {role} position. The email should be concise, personalized, and highlight the sender's relevant skills and experiences. Use a polite and engaging tone to connect with recruiter {receiver_name}.

    ### CONTEXT:
    Below are the details of the sender's resume and the job description. Use this information to tailor the email effectively.

    #### SENDER'S RESUME DETAILS:
    {resume_text}

    #### JOB DESCRIPTION:
    {job_description}

    #### SENDER'S INFORMATION:
    - Name: {sender_name}
    - Degree: {sender_degree} in {sender_major}
    - University: {sender_university}
    - Graduation Date: {sender_graduation}

    ### REQUIREMENTS FOR THE EMAIL:
    - Start with a professional and polite greeting.
    - Clearly state the purpose of reaching out.
    - Highlight specific skills, experiences, or achievements relevant to the job description.
    - Include a brief expression of enthusiasm for the company and role.
    - End with a call-to-action, such as requesting a meeting or further discussion.

    ### BEST EXAMPLE:
    Subject: Interested in Data Scientist role at Apple

    Hello Tim Cook,

    I'm Vara Prasad, a Master's student in Computer Science at UMass Amherst, graduating in May 2025. I came across the opening for Data Scientist role at Apple and was thrilled by the opportunity to contribute to Apple HCMI group with my technical foundation.

    Recently, I completed a Data Ops Co-op at Boehringer Ingelheim, where I worked closely with IT and R&D teams to tackle Machine Learning, Data Science, and Healthcare Quality challenges. I specialize in Python (FastAPI), PyTorch, LangChain, and ML Deployments. I have solid experience in supervised and unsupervised machine learning, as well as research work in developing Gen AI solutions using LLMs, GANs, Diffusion Models, and RAG pipelines.

    I've attached my resume and would love to explore any roles you or your known ones are hiring that align with my skill set. I'd greatly appreciate any insights or connections you can share.


    ### OUTPUT:
    Write the email below:
    """
