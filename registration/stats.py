import requests
from string import Template
from bs4 import BeautifulSoup


def leetcode_solved_problems(username):
    url = "https://leetcode.com/graphql"
    body = """
    { 
        matchedUser(username: "${username}") 
        {
            username
            submitStats: submitStatsGlobal 
            {
                acSubmissionNum 
                {
                    count
                    difficulty
                    submissions
                }
            }
        }
    }
    """

    t = Template(body)
    body = t.substitute(username=username)
    
    response = requests.post(url=url, json={"query": body})

    if response.status_code == 200:
        data = response.json()
        user = data["data"]["matchedUser"]
        if user:
            return user["submitStats"]["acSubmissionNum"][0]["count"]
    return -1


def codeforces_solved_problems(username):
    url = f"https://codeforces.com/profile/{username}"
    data = {"script": "true"}
    page_content = requests.get(url=url, data=data)
    soup = BeautifulSoup(page_content.text, "html.parser")

    infos = soup.find_all('div', attrs={'class':'_UserActivityFrame_counterValue'})
    if infos:
        data = infos[0].get_text()
        if "problems" in data or "problem" in data:
            return int(data.split()[0])
    return -1

if __name__ == "__main__":
    print(leetcode_solved_problems("loftyEureka"))
    print(codeforces_solved_problems("mohaomar495"))