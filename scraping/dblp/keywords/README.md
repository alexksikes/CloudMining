Run the following commands to generate the tags from the article titles. We assume the current working directory is this directory.

1) Generate the tags:

    export dbn=mysql db=dblp user=your_username passwd=your_password
    python get_tags.py stopwords.txt pub title &
    
    cut -f 1,3 tag_freqs.txt > freqs.txt
    
    python get_tags.py stopwords.txt pub title freqs.txt &
    
2) Clean up:
    
    unset dbn db user passwd
    mv *.txt /projects/data/cloudmining/dblp/keywords/