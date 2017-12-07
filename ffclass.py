class ff:
    title = ""
    link = ""
    flair= ""
    date = "" #datetime
    body = ""
    #score

    def __init__(self, title, body, link, flair, date):
        self.title = title
        self.link = link
        self.flair = flair
        self.body = body
        self.date = date