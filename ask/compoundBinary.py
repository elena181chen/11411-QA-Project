import nltk
import spacy 

# should only enter this function if the root of the syntax
# tree is a VP (verb phrase)
def ask_compound_bin_question(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    # uncomment the next three lines for debugging
    #print('\ndoc: ', doc)
    #for token in doc:
    #    print(token.text, token.pos_, token.dep_, spacy.explain(token.tag_), token.lemma_)
    
    lemma = ''
    correct_do = ''
    subject_explained = ''
    # lemmatize verb
    for token in doc:

        # TODO: account for all types of subjects
        if 'subj' in token.dep_:
            subj = token.text.lower() 
            subject_explained = spacy.explain(token.tag_)
  
        if token.pos_ == "VERB":
            verb_explained = spacy.explain(token.tag_)

            # TODO: need some way to account for they
            if 'present' in verb_explained:
                if subj == 'they': 
                    correct_do = 'Do'
                elif 'plural' in subject_explained:
                    correct_do = 'Do'
                elif 'personal' in subject_explained:
                    correct_do = 'Do'
                elif 'singular' in verb_explained: 
                    correct_do = 'Does'
            # use past tense inflection
            else:
                correct_do = 'Did'
            lemma = token.lemma_

            break

    # construct question
    question = correct_do

    # add in subject
    for token in doc: 

        if 'subj' in token.dep_:
            if token.pos_ == 'PRON' and token.text != 'I':
                question += ' ' + token.text.lower()
            else:
                question += ' ' + token.text
        # account for case of gerund/present participle
        # go + verb-ing
        elif token.pos_ == 'VERB' and 'gerund' not in spacy.explain(token.tag_):
            question += ' ' + lemma 
        elif token.pos_ == 'DET': 
            question += ' ' + token.text.lower() 
        
      # end question at punctuation
        elif token.pos_ == 'PUNCT':
            question += '?'
            break
        else:
            question += ' ' + token.text

    return question