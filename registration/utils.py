def username_adjust(student):
    codeforces_username = student.codeforces_username
    if "https://codeforces.com/profile/" in codeforces_username:
        codeforces_username = codeforces_username.replace("https://codeforces.com/profile/", "").replace("/", "")
    if "Codeforces.com/profile/" in codeforces_username:
        codeforces_username = codeforces_username.replace("Codeforces.com/profile/", "").replace("/", "")
    if "codeforces.com/profile/" in codeforces_username:
        codeforces_username = codeforces_username.replace("codeforces.com/profile/", "").replace("/", "")
    if "@" in codeforces_username:
        codeforces_username = codeforces_username.replace("@", "")

    leetcode_username = student.leetcode_username
    if "https://leetcode.com/" in leetcode_username:
        leetcode_username = leetcode_username.replace("https://leetcode.com/", "").replace("/", "")
    if "Leetcode.com/" in leetcode_username:
        leetcode_username = leetcode_username.replace("Leetcode.com/", "").replace("/", "")
    if "@" in leetcode_username:
        leetcode_username = leetcode_username.replace("@", "")
    
    return leetcode_username, codeforces_username