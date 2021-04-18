LANGUAGE_CHOICES = (
    ("1","Igbo"),
    ("2","Hausa"),
    ("3","Yoruba"),
    ("4","Esan"),
    ("5","English"),
    ("6","Spanish"),
    ("7","German"),
    ("8","Italian"),
    ("9","French"),
    ("10","Russian"),
    ("10","Chineese"),
)

def from_label_to_value(request, field):
    if field == 'speaks':
        labels = request.user.profile.speaks
    else:
        labels = request.user.profile.is_learning
    
    if labels is not None:
        values = [value for value,label in LANGUAGE_CHOICES if label in labels]
        values = [int(i) for i in values]
    else:
        values = ''
    return values

def sort(elements,results, l_s=False, l_l=False):
    if len(elements)>1:
        for e in range(len(elements)):
            if e == 0:
                continue
            if l_s:
                results = results.filter(speaks__icontains=elements[e])
            if l_l:
                results = results.filter(speaks__icontains=elements[e])
    return results

