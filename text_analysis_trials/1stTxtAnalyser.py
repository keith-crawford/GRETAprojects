import io
import string

report_text = io.open("/home/ubuntu/source/project-williamsville/data/earningreports/collectedreports.txt", "r", encoding="utf-8")
contents = report_text.read()
report_text.close()

contents = contents.lower()
contents = contents.split(" ")

# print (contents) # Debugging

f = open("/home/ubuntu/source/project-williamsville/data/stop_words.txt", "r", encoding="utf-8")
stoppers = f.read()
stop_list = stoppers.split("\n")

#Remove punctiation and and linebreaks from contents
punctuation = '''!()-—[]{};:"’\,<>./?@#$%^&*_~'''
linebreak = "\n"


output_content=list()

for element in contents:
    if element in punctuation:
        continue
    elif element == linebreak:
        continue
    elif len(element)<4:
        continue
    elif element in stop_list:
        continue
    else: 
        output_content.append(element) 

print (f"Length of content: {len(contents)}")
print (f"Length of output: {len(output_content)}")


#Create a set from the list. A set cannot have duplicate words, so it returns the individual words.
content_set=set(output_content)
print(f"There are {len(content_set)} individual words")

#Count words and assign quantities to set words, then print in order of
word_count= {}
for element in content_set:
    if element not in word_count and element != '':
        total = output_content.count(element)
        word_count[element]=total
        
sorted_word_count = sorted(word_count.items(), key= lambda x:x[1], reverse=True)[:10]

for w in range(len(sorted_word_count)):
    print (w+1, sorted_word_count[w], sep="\t")