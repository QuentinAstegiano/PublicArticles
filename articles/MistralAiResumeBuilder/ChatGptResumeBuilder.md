# Building a Resume Generator With ChatGPT and Python

Writing a resume is not always a great experience. It's something you do when necessary, and that's not often, so you're not accustomed to it.
You probably don't know how to write a good resume and won't know where to start.

So... why not ask ChatGPT to help us?

What we usually have is a LinkedIn profile that is mostly up-to-date.
What if we could get that data and transform it into a resume?

That's what we are going to explore here.

# Get Data From LinkedIn

Getting all your relevant data from LinkedIn tends to be a pain.
You can export some data about your profile from their export tool, but I've yet to find a way to export everything about you.
The best way I found is the simple one: open your LinkedIn profile in a browser and simply copy-paste everything into a text document.

*Screenshot_Quentin Astegiano LinkedIn*

I'll take my personal profile as an example here.
Notice that it's written in French, and that I want an international CV, written in English; with the tool we're building, I don't even need to do most of the translation myself!

# Extract Relevant Data With ChatGPT

To execute ChatGPT calls from a Python script, you'll need to set up some prerequisites.
It's quite easy - and you can refer to my other article on the subject for more details:  [https://medium.com/@quentin.astegiano/unlocking-the-potential-a-guide-to-using-chatgpt-from-python-1884fd7c3d7b]

The complete working source code for this tool is available on my GitHub: [https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiResumeBuilder/sources/main/ChatGptResumeBuilder.py]

As usual, I'll start by creating a helper function to encapsulate the call to ChatGPT:

```python
    def _ask_chatgpt(self, system_role: str, user_role: str) -> str:
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_role},
            ],
        )
        content = response.choices[0].message.content
        return content
```

I want to be able to extract and format data about various aspects of my LinkedIn profile.
To do that, I'm going to craft some specific prompts for each use case.

The prompts are what make or break these apps. I've found that it is much better to have a very specific prompt, even if that means repeating yourself, than to try to write a generic one.

## Extracting Profesionnal History

The first thing to extract is the professional history : 

```python
    def _extract_profesionnal_history(self, data: str) -> str:
        print("... creating section professional history")
        system_role = """
        You're a helpful assistant specialized in writing comprehensive resumes.
        Extract from the given LinkedIn data all that is relevant to the Professional History. 
        It should be grouped by company, and for each company, every role held in that company should be listed.
        For each role, detail what was done and the associated skills.

        The output must be formatted in markdown.

        The output must be exclusively written in English. Words not in English should be translated.        
        """
        return self._ask_chatgpt(system_role, data)
```

The great thing here is that we can really tailor what we want to see from ChatGPT. This is why this approach yields much nicer results than trying to generate the whole resume in only one prompt.
Here, I specify that I want my professional history to be listed by company and by role, and to specify each skill associated - and even if it's not directly listed in my LinkedIn profile, ChatGPT will oblige and infer the skills from the descriptions of the tasks.

## Extracting Educational History

The second thing to extract is the educational history, with a similar prompt:

```python
    def _extract_educational_history(self, data: str) -> str:
        print("... creating section educational history")
        system_role = """
        You're a helpful assistant specialized in writing resumes.
        Extract from the given LinkedIn data all that is relevant to the educational history. 
        The output must be formatted in markdown and detail every school attended, and every diploma received.
        It should not contain anything not related to the educational history.

        The output must be exclusively written in English. Words not in English should be translated.        
        """
        return self._ask_chatgpt(system_role, data)
```

## Extracting Technical Skills

This one is the trickier one. I didn't list my skills on LinkedIn, but that would be nice on a resume.
So I want to make ChatGPT list them all for me, and I even want to have a score associated with each.

```python
    def _extract_skills(self, data: str) -> str:
        print("... creating section Skills")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        Extract from the given LinkedIn data all that is relevant to the technical skills. 

        The output must be formatted in markdown and list every skill, with relevant grouping. 
        Each skill must be given a note from 1 to 5.

        The output must be exclusively written in English. Words not in english should be translated.
        """
        return self._ask_chatgpt(system_role, data)
```

ChatGPT is smart enough to manage to group the skills listed in the various job descriptions.
When a skill is listed multiple time, over a long period of time, it'll assign a higher score to it.

# Checking the result !

Here is the complete file generated by the script : [https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiResumeBuilder/resume_chatgpt.md]

So, what does ChatGPT have to say about me ?

> Highly experienced technical professional with 15 years of expertise in managing and leading technical teams.
> Currently, the Director of Technical Services at Fnac Darty, responsible for overseeing the technological operations and driving the implementation of innovative solutions.
> Successfully led the implementation of Elasticsearch and improved security measures.
> Proficient in project management, budgeting, and agile methodologies.
> Strong skills in team leadership, technical architecture, and continuous delivery.

Well, that's not bad at all for !

What about my work history ?

> Fnac Darty
> 
> Responsable de domaine (March 2019 - Present)
> As the Responsible for the "Front Web Darty" and "Search" domains at Fnac Darty, I manage a team of around forty individuals including developers, Business Analysts, testers, and production support. My responsibilities include overseeing the entire front-end systems of the Darty e-commerce platform, as well as the search engines of the group. I am involved in various aspects of management such as roadmap planning, budget management, project management, as well as day-to-day collaboration with technical teams in order to support them in design and implementation efforts.
> 
> Skills: Management, Roadmap Planning, Budget Management, Project Management, Technical Collaboration

And my favorite part, the technical skills : 

> Programming Languages
> - Java - 5/5
> - JavaScript - 4/5
> - Groovy - 4/5
> Build Tools and CI/CD
> - Gradle - 4/5
> - Jenkins - 3/5
> - Hudson - 3/5
> - BitBucket - 3/5
> Database
> - Oracle - 3/5
> Other Skills
> - Management - 4/5
> - Project Management - 4/5
> - Budget Management - 4/5
> - Agile Methodologies - 4/5

Again, this is kind of mind-blowing to me: I did not list my skills on LinkedIn. This is all ChatGPT inference.

Of course, the scores need to be tweaked a bit to actually be true (I haven't done anything serious in Groovy in the last 10 years, so I certainly didn't deserve a 4/5 there!) but still, this is a huge time-saver compared to doing it all by hand.
