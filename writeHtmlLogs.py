import markdown
import datetime

absolutePath = ""
outPath = "result.html"
nDays = 10

now = datetime.datetime.now()
out = ""

for i in range(nDays):
    thisDate = now - datetime.timedelta(days=i)
    logPath = absolutePath + "logs/" + thisDate.strftime("%Y-%m-%d") + "_log.md"
    try:
        with open(logPath, 'r') as md_file:
            md_content = md_file.read()
        out = out + markdown.markdown(md_content, extensions=['tables'])
    except FileNotFoundError:
        out = out + "<h3 style='color: red;'>Missing Log for " + thisDate.strftime("%A, %B %d, %Y") + " !!!</h3>"

# CSS for the page
css = """
<style>
    body {
        background-color: #2f2f2f;
        color: #e8e8e8;
    }
    table {
        border-collapse: collapse;
        width: 70%;
    }
    th, td {
        padding: 15px;
        text-align: left;
    }
</style>
"""

# Write the HTML content to a file
with open(outPath, 'w') as html_file:
    html_file.write(css + out)
